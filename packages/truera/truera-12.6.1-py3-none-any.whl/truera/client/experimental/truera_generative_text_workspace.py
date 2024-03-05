try:
    import trulens_eval
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing module for TrueraGenerativeTextWorkspace. "
        "Please install additional modules with `pip install truera[llm]`"
    ) from exc

from dataclasses import dataclass
import logging
import os
import sys
from typing import (
    Any, Callable, Mapping, Optional, Sequence, Tuple, Type, Union
)
from uuid import uuid1

# pylint: disable=no-name-in-module
from google.protobuf.struct_pb2 import Value
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import DoubleValue
from google.protobuf.wrappers_pb2 import Int32Value
import pandas as pd
# pylint: enable=no-name-in-module
from pydantic import BaseModel
from trulens_eval import schema as trulens_schema
from trulens_eval.app import App
from trulens_eval.tru import logger as trulens_logger
from trulens_eval.utils.serial import JSON

from truera.client.cache import invalidates_cache
from truera.client.cache import MetadataCache
from truera.client.ingestion.schema import python_val_to_pb_value
from truera.client.ingestion.temporary_file import TemporaryFile
from truera.client.remote_truera_workspace import RemoteTrueraWorkspace
from truera.client.truera_authentication import TrueraAuthentication
from truera.protobuf.public.common import generative_pb2 as gen_pb
import truera.protobuf.public.metadata_message_types_pb2 as md_pb

EXPERIMENT_SPLIT_NAME = "experiment"
PRODUCTION_SPLIT_NAME = "prod"


@dataclass
class IngestionContext:
    project_id: str
    data_collection_id: str
    app_id: str
    split_id: str
    feedback_function_name_id_map: Mapping[str, str]


@dataclass
class Production:
    pass


@dataclass
class Experiment:
    pass


@dataclass
class Evaluation:
    pass


class LLMDatasetConfig(BaseModel):
    config: Union[Production, Experiment, Evaluation]

    def _dataset_name(self) -> str:
        return


class TruApp():

    @property
    def app(self):
        return self.trulens_app.app

    def __init__(
        self,
        trulens_app: App,
        ingestion_context: IngestionContext,
        trace_handler: Callable[[trulens_schema.Record], None],
        feedback_handler: Callable[[trulens_schema.FeedbackResult], None],
    ):
        self.trulens_app = trulens_app
        self.trace_handler = trace_handler
        self.feedback_handler = feedback_handler

        self.ingestion_context = ingestion_context
        self.recorded_traces = []

    def __enter__(self):
        return self.trulens_app.__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        # ingest traces and feedbacks
        ctx = self.trulens_app.recording_contexts.get()
        self.trulens_app.__exit__(exc_type, exc_value, exc_tb)
        for trace in ctx.records:
            trace_uuid = str(uuid1())
            trace.record_id = trace_uuid
            self.trace_handler(trace)
            for feedback_future in trace.feedback_results or []:
                feedback_future.add_done_callback(
                    create_done_callback(
                        feedback_handler=self.feedback_handler,
                        trace_id=trace_uuid
                    )
                )
            self.recorded_traces.append(trace)


class TrueraGenerativeTextWorkspace:

    def __init__(
        self,
        connection_string: str,
        authentication: TrueraAuthentication,
        log_level: int = logging.INFO,
        workspace_name: str = "",
    ):
        logging.basicConfig(
        )  # Have to do this in order to enable setting log level below WARNING in jupyter
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.remote_tru = RemoteTrueraWorkspace(
            connection_string=connection_string,
            authentication=authentication,
            log_level=logging.WARNING,
            workspace_name=workspace_name
        )

        self.md_cache = MetadataCache(self.remote_tru)
        init_trulens()

    def add_project(self, project: str):
        return self.remote_tru.add_project(
            project=project,
            score_type="generative_text",
            input_type="text",
            project_type="application_project"
        )

    def get_projects(self) -> Sequence[str]:
        return self.remote_tru.get_projects()

    @invalidates_cache
    def delete_project(self, project: str):
        return self.remote_tru.delete_project(project)

    def get_apps(self, project_name: str) -> Sequence[str]:
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        return [a.name for a in self._get_apps(project_id=project_id)]

    @invalidates_cache
    def delete_app(self, app_name: str, project_name: str):
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        self.remote_tru.artifact_interaction_client.delete_model(
            project_id=project_id, model_name=app_name, recursive=True
        )
        self.remote_tru.artifact_interaction_client.delete_data_collection(
            project_id=project_id,
            data_collection_name=app_name,
            recursive=True
        )

    def _create_app(self, app_name: str, project_name: str) -> str:
        """Creates app. Returns app id.

        Data collection with the same name will be created to associate with the app.
        Additionally creates experiment and production splits.
        """
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        self.remote_tru.ar_client.create_data_collection(
            project_id=project_id,
            data_collection_name=app_name,
            feature_transform_type=md_pb.FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
        )
        data_collection_id = self.md_cache.get_data_collection_id(
            data_collection_name=app_name, project_id=project_id
        )
        self.remote_tru.data_service_client.create_empty_split(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_name=EXPERIMENT_SPLIT_NAME
        )
        self.remote_tru.data_service_client.create_empty_split(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_name=PRODUCTION_SPLIT_NAME
        )
        return self.remote_tru.ar_client.create_model_metadata(
            project_id=project_id,
            data_collection_name=app_name,
            model_id="",
            model_name=app_name,
            model_type="virtual",
            model_output_type="text_output",
            locator=""
        )

    def _get_apps(self, project_id: str) -> Sequence[md_pb.ModelMetadata]:
        return self.remote_tru.ar_client.get_all_model_metadata_in_project(
            project_id=project_id, as_json=False
        )

    def get_feedback_functions(self, project_name: str) -> Sequence[str]:
        return self.remote_tru.artifact_interaction_client.get_all_feedback_function_names_in_project(
            project_id=self.
            _get_application_project_id_from_project_name(project_name)
        )

    def add_user_feedback(
        self, project_name: str, app_name: str, feedback_function_name: str,
        trace_id: str, dataset_config: LLMDatasetConfig, result: float
    ) -> None:
        """Ingest the result of user-provided feedback.

        Args:
            project_name (str): The name of the project to ingest feedback into.
            app_name (str): The name of the application to ingest traces and feedbacks into.
            feedback_function_name (str): The name of the feedback function that the feedback is associated with.
            trace_id (str): The id of the trace that the feedback is associated with.
            dataset_config (LLMDatasetConfig): The dataset configuration. The `config` attribute must be one of {Production, Experiment, or Evaluation}.
            result (float): The result of the feedback to ingest.
        """
        ingestion_context = self._resolve_ingestion_context(
            project_name=project_name,
            app_name=app_name,
            feedback_function_names=[feedback_function_name],
            dataset_config=dataset_config,
            feedback_thresholds=None
        )
        feedback_result = trulens_schema.FeedbackResult(
            feedback_result_id=str(uuid1())
        )
        feedback_result.record_id = trace_id
        feedback_result.result = result
        feedback_result.name = feedback_function_name
        self._ingest_feedback(
            feedback_result=feedback_result,
            ingestion_context=ingestion_context
        )

    def run_feedback_functions(
        self, app: TruApp, project_name: str, app_name: str,
        trace: trulens_schema.Record,
        feedback_functions: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig
    ) -> Sequence[trulens_schema.FeedbackResult]:
        """Run feedback functions on a trace from a wrapped application and ingest results.

        Args:
            app (TruApp): Wrapped application object.
            project_name (str): The name of the project to ingest feedbacks into.
            app_name (str): The name of the application to ingest traces and feedbacks into.
            trace (trulens_schema.Record): The trace to evaluate on.
            feedback_functions (Sequence[trulens_eval.Feedback]): The feedback functions to run.
            dataset_config (LLMDatasetConfig): The dataset configuration. The `config` attribute must be one of {Production, Experiment, or Evaluation}.

        Returns:
            A list of the results from running the feedback functions on the trace.
        """
        ff_names = []
        for f in feedback_functions:
            if not f.supplied_name:
                raise ValueError(
                    "All Feedback functions must have a supplied name for ingestion!"
                )
            ff_names.append(f.supplied_name)

        ingestion_context = self._resolve_ingestion_context(
            project_name=project_name,
            app_name=app_name,
            feedback_function_names=ff_names,
            dataset_config=dataset_config,
            feedback_thresholds=None
        )

        feedback_results = []
        for feedback_function in feedback_functions:
            feedback_result = feedback_function.run(
                app=app.trulens_app, record=trace
            )
            feedback_results.append(feedback_results)
            self._ingest_feedback(
                feedback_result=feedback_result,
                ingestion_context=ingestion_context
            )
        return feedback_results

    def get_trace_data(
        self,
        app_name: str,
        project_name: str,
        dataset_config: LLMDatasetConfig,
        trace_id: Optional[str] = None,
        include_feedback_aggregations: bool = False,
        include_spans: Optional[bool] = False
    ) -> pd.DataFrame:
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        app_id = self.md_cache.get_model_id(app_name, project_id=project_id)
        split_id = self._get_dataset_id_from_dataset_config(
            project_name=project_name,
            app_name=app_name,
            dataset_config=dataset_config
        )
        return self.remote_tru.aiq_client.get_trace_data(
            project_id,
            app_id,
            data_split_id=split_id,
            trace_id=trace_id,
            include_feedback_aggregations=include_feedback_aggregations,
            include_spans=include_spans
        ).response

    def get_feedback_function_evaluations(
        self, project_name: str, app_name: str,
        dataset_config: LLMDatasetConfig, trace_id: str
    ) -> pd.DataFrame:
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        app_id = self.md_cache.get_model_id(app_name, project_id=project_id)
        split_id = self._get_dataset_id_from_dataset_config(
            project_name=project_name,
            app_name=app_name,
            dataset_config=dataset_config
        )
        return self.remote_tru.aiq_client.get_feedback_function_evaluations(
            project_id, app_id, split_id, trace_id=trace_id
        ).response

    def get_feedback_function_metadata(self, project_name: str) -> pd.DataFrame:
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        return self.remote_tru.aiq_client.get_feedback_function_metadata(
            project_id
        ).response

    def configure_feedback_functions(
        self,
        project_name: str,
        feedback_function_id: str,
        feedback_function_name: Optional[str] = None,
        threshold: Optional[float] = None
    ):
        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        return self.remote_tru.ar_client.update_feedback_function(
            feedback_function_id, project_id, feedback_function_name, threshold
        )

    def _wrap_app(
        self,
        app: Any,
        app_class: Type[App],
        project_name: str,
        app_name: str,
        feedbacks: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ):
        feedback_function_names = []
        for f in feedbacks:
            if not f.supplied_name:
                raise ValueError(
                    "All Feedback functions must have a supplied name for ingestion!"
                )
            feedback_function_names.append(str(f.supplied_name))
        ingestion_context = self._resolve_ingestion_context(
            project_name=project_name,
            app_name=app_name,
            feedback_function_names=feedback_function_names,
            dataset_config=dataset_config,
            feedback_thresholds=feedback_thresholds
        )
        return TruApp(
            trulens_app=app_class(app, app_id=app_name, feedbacks=feedbacks),
            ingestion_context=ingestion_context,
            trace_handler=lambda trace: self.
            _ingest_trace(trace, ingestion_context),
            feedback_handler=lambda feedback: self.
            _ingest_feedback(feedback, ingestion_context)
        )

    def wrap_basic_app(
        self,
        app: Any,
        project_name: str,
        app_name: str,
        feedbacks: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ) -> TruApp:
        """Wrap a basic app."""
        return self._wrap_app(
            app=app,
            app_class=trulens_eval.TruBasicApp,
            project_name=project_name,
            app_name=app_name,
            feedbacks=feedbacks,
            dataset_config=dataset_config,
            feedback_thresholds=feedback_thresholds
        )

    def wrap_llama_index_app(
        self,
        app: Any,
        project_name: str,
        app_name: str,
        feedbacks: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ) -> TruApp:
        """Wrap a LlamaIndex app."""
        return self._wrap_app(
            app=app,
            app_class=trulens_eval.TruLlama,
            project_name=project_name,
            app_name=app_name,
            feedbacks=feedbacks,
            dataset_config=dataset_config,
            feedback_thresholds=feedback_thresholds
        )

    def wrap_langchain_app(
        self,
        app: Any,
        project_name: str,
        app_name: str,
        feedbacks: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ) -> TruApp:
        """Wrap a Langchain app."""
        return self._wrap_app(
            app=app,
            app_class=trulens_eval.Langchain,
            project_name=project_name,
            app_name=app_name,
            feedbacks=feedbacks,
            dataset_config=dataset_config,
            feedback_thresholds=feedback_thresholds
        )

    def wrap_custom_app(
        self,
        app: Any,
        project_name: str,
        app_name: str,
        feedbacks: Sequence[trulens_eval.Feedback],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ) -> TruApp:
        """Wrap a custom app."""
        return self._wrap_app(
            app=app,
            app_class=trulens_eval.TruCustomApp,
            project_name=project_name,
            app_name=app_name,
            feedbacks=feedbacks,
            dataset_config=dataset_config,
            feedback_thresholds=feedback_thresholds
        )

    def _resolve_ingestion_context(
        self,
        project_name: str,
        app_name: str,
        feedback_function_names: Sequence[str],
        dataset_config: LLMDatasetConfig,
        feedback_thresholds: Optional[Mapping[str, float]] = None
    ) -> IngestionContext:

        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        if app_name not in [a.name for a in self._get_apps(project_id)]:
            self._create_app(app_name=app_name, project_name=project_name)
            self.logger.info(
                f"App '{app_name}' did not exist. Created new app '{app_name}' in project '{project_name}'."
            )
        app_id = self.md_cache.get_model_id(
            model_name=app_name, project_id=project_id
        )
        data_collection_id = self.md_cache.get_data_collection_id(
            data_collection_name=app_name,  # data collection name is app name
            project_id=project_id
        )

        split_id = self._get_dataset_id_from_dataset_config(
            project_name=project_name,
            app_name=app_name,
            dataset_config=dataset_config
        )

        existing_feedback_functions = {
            f.name: f.id for f in self.remote_tru.ar_client.
            get_all_feedback_function_names_and_ids_in_project(
                project_id=project_id
            )
        }
        for ff_name in feedback_function_names:
            if ff_name not in existing_feedback_functions:
                threshold = feedback_thresholds[
                    ff_name
                ] if feedback_thresholds and ff_name in feedback_thresholds else None
                existing_feedback_functions[
                    ff_name
                ] = self.remote_tru.artifact_interaction_client.create_feedback_function(
                    ff_name, project_id, threshold
                )
                self.logger.info(
                    f"Feedback function '{ff_name}' did not exist. Created new feedback function '{ff_name}' in project '{project_name}"
                )

        return IngestionContext(
            project_id=project_id,
            data_collection_id=data_collection_id,
            app_id=app_id,
            split_id=split_id,
            feedback_function_name_id_map=existing_feedback_functions
        )

    def _get_application_project_id_from_project_name(
        self, project_name: str
    ) -> str:
        """Get project id from project name. Raises ValueError if project is not an application project."""
        project_metadata = self.md_cache.get_project_metadata(project_name)
        if project_metadata.project_type != md_pb.APPLICATION_PROJECT:
            raise ValueError(
                f"Project '{project_name}' is not an generative application project!"
            )
        return project_metadata.id

    def _get_dataset_id_from_dataset_config(
        self, project_name: str, app_name: str, dataset_config: LLMDatasetConfig
    ) -> str:
        """Get split id from project name, app name, and dataset config."""

        project_id = self._get_application_project_id_from_project_name(
            project_name
        )
        if isinstance(dataset_config.config, Production):
            datasplit_name = PRODUCTION_SPLIT_NAME
        elif isinstance(dataset_config.config, Experiment):
            datasplit_name = EXPERIMENT_SPLIT_NAME
        else:
            raise ValueError(
                f"Dataset config '{dataset_config.config}' not supported. Please use Production or Experiment"
            )
        return self.md_cache.get_data_split_id(
            project_id=project_id,
            data_collection_name=app_name,
            data_split_name=datasplit_name
        )

    def _ingest_trace(
        self, trace: trulens_schema.Record, ingestion_context: IngestionContext
    ) -> None:
        self.remote_tru.streaming_ingress_client.ingest_trace(
            project_id=ingestion_context.project_id,
            data_collection_id=ingestion_context.data_collection_id,
            model_id=ingestion_context.app_id,
            split_id=ingestion_context.split_id,
            trace=trace_to_pb(trace)
        )

    def _ingest_feedback(
        self, feedback_result: trulens_schema.FeedbackResult,
        ingestion_context: IngestionContext
    ) -> None:
        self.remote_tru.streaming_ingress_client.ingest_feedback(
            project_id=ingestion_context.project_id,
            data_collection_id=ingestion_context.data_collection_id,
            model_id=ingestion_context.app_id,
            split_id=ingestion_context.split_id,
            feedback=feedback_result_to_pb(
                feedback_result, ingestion_context=ingestion_context
            )
        )


def record_app_call_method_to_pb(
    record_app_call_method: trulens_schema.RecordAppCallMethod
) -> Value:
    return json_to_value(
        dict(
            path=str(record_app_call_method.path),
            method=json_to_value(
                dict(
                    name=record_app_call_method.method.name,
                    obj={
                        "class": record_app_call_method.method.obj.cls.name,
                        "id": record_app_call_method.method.obj.id
                    }
                )
            )
        )
    )


def perf_to_pb(perf: Optional[trulens_schema.Perf]) -> Value:
    if perf:
        return json_to_value(
            dict(
                start_time=str(perf.start_time.isoformat()),
                end_time=str(perf.end_time.isoformat())
            )
        )
    return json_to_value(None)


def record_app_call_to_pb(
    record_app_call: trulens_schema.RecordAppCall
) -> Value:
    return json_to_value(
        dict(
            stack=[
                record_app_call_method_to_pb(v) for v in record_app_call.stack
            ],
            args=record_app_call.args,
            rets=record_app_call.rets,
            error=record_app_call.error,
            perf=perf_to_pb(record_app_call.perf),
            pid=record_app_call.pid,
            tid=record_app_call.tid
        )
    )


def trace_to_pb(trace: trulens_schema.Record) -> gen_pb.GenerativeTrace:
    if trace.perf:
        start_time = Timestamp()
        start_time.FromDatetime(trace.perf.start_time)
        end_time = Timestamp()
        end_time.FromDatetime(trace.perf.end_time)
    else:
        start_time = None
        end_time = None
    return gen_pb.GenerativeTrace(
        record_id=trace.record_id,
        meta=json_to_value(trace.meta),
        main_input=json_to_value(trace.main_input),
        main_output=json_to_value(trace.main_output),
        main_error=json_to_value(trace.main_error),
        calls=json_to_value([record_app_call_to_pb(c) for c in trace.calls]),
        prompt=json_to_value(trace.main_input
                            ),  # prompt and main_input are the same
        start_time=start_time,
        end_time=end_time,
        cost=cost_to_pb(trace.cost)
    )


def json_to_value(json_value: JSON) -> Value:
    """Turns the trulens_eval JSON into a protobuf Value"""
    # TODO: consolidate the below function into a shared library
    try:
        return python_val_to_pb_value(json_value)
    except:
        return python_val_to_pb_value(str(json_value))


def cost_to_pb(
    cost: Optional[trulens_schema.Cost]
) -> Optional[gen_pb.GenerativeCost]:
    """Turns the trulens_eval Cost into GenerativeCost protobuf"""
    if cost:
        return gen_pb.GenerativeCost(
            n_requests=Int32Value(value=cost.n_requests),
            n_successful_requests=Int32Value(value=cost.n_successful_requests),
            n_classes=Int32Value(value=cost.n_classes),
            n_tokens=Int32Value(value=cost.n_tokens),
            n_stream_chunks=Int32Value(value=cost.n_stream_chunks),
            n_prompt_tokens=Int32Value(value=cost.n_prompt_tokens),
            n_completion_tokens=Int32Value(value=cost.n_completion_tokens),
            cost=DoubleValue(value=cost.cost),
        )
    return None


def feedback_call_to_pb(feedback_call: trulens_schema.FeedbackCall) -> Value:
    return json_to_value(
        dict(
            args=json_to_value(feedback_call.args),
            ret=json_to_value(feedback_call.ret),
        )
    )


def feedback_result_to_pb(
    feedback_result: trulens_schema.FeedbackResult,
    ingestion_context: IngestionContext
) -> gen_pb.GenerativeFeedback:
    evaluation_timestamp = Timestamp()
    evaluation_timestamp.FromDatetime(feedback_result.last_ts)
    feedback_function_id = ingestion_context.feedback_function_name_id_map.get(
        feedback_result.name, feedback_result.feedback_definition_id
    )
    return gen_pb.GenerativeFeedback(
        feedback_function_id=feedback_function_id,
        feedback_result_id=feedback_result.feedback_result_id,
        record_id=feedback_result.record_id,
        result=feedback_result.result,
        meta=json_to_value([c.meta for c in feedback_result.calls]),
        cost=cost_to_pb(feedback_result.cost),
        evaluation_timestamp=evaluation_timestamp,
        calls=json_to_value(
            [feedback_call_to_pb(f) for f in feedback_result.calls]
        ),
    )


def format_feedback_result(
    future_result, trace_id: str
) -> trulens_schema.FeedbackResult:
    """We got to do some jank stuff. 
        * The result isn't actually a result, but a Tuple[Feedback, FeedbackResult]
        * Record_id should be replaced with the uuid1 one
    """
    if isinstance(future_result, Tuple):
        _, feedback_result = future_result
    else:
        feedback_result = future_result
    feedback_result.record_id = trace_id  # trulens doesn't give the right trace_id
    return feedback_result


def create_done_callback(feedback_handler, trace_id: str):
    """Need this function so variable lookup works as expected."""
    #TODO: Delete this method once formatting with uuid1 is no longer necessary
    return lambda f: feedback_handler(
        format_feedback_result(f.result(), trace_id=trace_id)
    )


def init_trulens():
    """Initialize Tru singleton, suppress initialization output, and use a temporary file as sqlite db"""

    class IgnoreOutput:
        """Class to hide print() and logger output"""

        def __enter__(self):
            self.original_stdout = sys.stdout
            self.log_level = trulens_logger.level
            sys.stdout = open(os.devnull, "w")
            trulens_logger.setLevel(logging.ERROR)

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self.original_stdout
            trulens_logger.setLevel(self.log_level)

    with IgnoreOutput():
        # We want to hide sqlite details from user
        # in-memory sqlite is not threadsafe, so we use a temporary file
        trulens_eval.Tru(
            database_url=f"sqlite:///{TemporaryFile(suffix='.sqlite').name}"
        )
