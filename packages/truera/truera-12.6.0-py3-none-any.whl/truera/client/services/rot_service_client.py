import logging
from typing import Optional, Union

from truera.client.private.communicator.rot_service_communicator import \
    RotServiceCommunicator
from truera.client.private.communicator.rot_service_http_communicator import \
    HttpRotServiceCommunicator
from truera.client.public.auth_details import AuthDetails
from truera.protobuf.public.read_optimized_table_service import \
    read_optimized_table_messages_pb2 as rot_messages_pb
from truera.protobuf.public.read_optimized_table_service import \
    read_optimized_table_service_pb2 as rot_pb


class RotServiceClient:

    def __init__(
        self, communicator: RotServiceCommunicator, logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpRotServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.rot_service_grpc_communicator import \
                GrpcRotServiceCommunicator
            communicator = GrpcRotServiceCommunicator(
                connection_string, auth_details, logger
            )
        return RotServiceClient(communicator, logger)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def create_rot(
        self, project_id: str, data_collection_id: str, split_id: str,
        model_id: str
    ) -> rot_pb.CreateRotResponse:
        req = rot_pb.CreateRotRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=split_id,
            model_id=model_id
        )
        return self.communicator.create_rot(req)

    def get_rot_metadata(
        self, project_id: str, data_collection_id: str, split_id: str,
        model_id: str
    ) -> rot_pb.GetRotMetadataResponse:
        req = rot_pb.GetRotMetadataRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=split_id,
            model_id=model_id
        )
        return self.communicator.get_rot_metadata(req)

    def get_latest_rot_operation(
        self, project_id: str, data_collection_id: str, split_id: str,
        model_id: str
    ) -> rot_pb.GetLatestRotOperationResponse:
        req = rot_pb.GetLatestRotOperationRequest(
            query_metadata=rot_messages_pb.RotQueryMetadata(
                project_id=project_id,
                data_collection_id=data_collection_id,
                split_id=split_id,
                model_id=model_id
            )
        )
        return self.communicator.get_latest_rot_operation(req)

    def update_rot(
        self,
        project_id: Optional[str] = None,
        data_collection_id: Optional[str] = None,
        split_id: Optional[str] = None,
        model_id: Optional[str] = None,
        rot_id: Optional[str] = None
    ) -> rot_pb.UpdateRotResponse:
        req = rot_pb.UpdateRotRequest(
            rot_id=rot_id
        ) if rot_id else rot_pb.UpdateRotRequest(
            query_metadata=rot_messages_pb.RotQueryMetadata(
                project_id=project_id,
                data_collection_id=data_collection_id,
                split_id=split_id,
                model_id=model_id
            )
        )
        return self.communicator.update_rot(req)
