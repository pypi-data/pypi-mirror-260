from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StructuredEventProperties(_message.Message):
    __slots__ = ("add_dashboard_event_properties", "update_dashboard_event_properties", "delete_dashboard_event_properties", "add_project_event_properties", "add_data_collection_event_properties", "add_data_split_event_properties", "add_model_event_properties", "add_model_metadata_event_properties", "add_feature_list_event_properties", "add_filter_to_rowset_event_properties", "modify_prediction_cache_event_properties", "modify_explanation_cache_event_properties", "ingest_labels_event_properties", "ingest_extra_data_event_properties", "ingest_predictions_data_event_properties", "add_feature_influences_event_properties", "add_feature_metadata_event_properties", "add_segment_group_event_properties", "modify_data_source_event_properties", "page_view_event_properties", "test_created_event_properties", "launch_quickstart_event_properties", "click_create_project_event_properties", "signup_step_personal_event_properties", "signup_step_landing_event_properties", "signup_step_workspace_event_properties", "auth_error_event_properties", "add_data_event_properties", "visited_project_leaderboard_event_properties", "visited_model_leader_board_event_properties", "contact_sales_event_properties", "trigger_intercom_product_tour_event_properties", "update_data_split_event_properties", "update_data_collection_event_properties", "update_model_event_properties", "delete_project_event_properties", "delete_data_collection_event_properties", "delete_data_split_event_properties", "delete_model_event_properties", "add_report_event_properties", "visit_report_event_properties", "delete_report_event_properties", "update_report_event_properties", "authorization_admin_event_properties", "add_user_as_admin_event_properties", "remove_user_as_admin_event_properties", "add_user_event_properties", "add_user_to_project_event_properties", "remove_user_from_project_event_properties", "grant_role_event_properties", "revoke_role_event_properties")
    ADD_DASHBOARD_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DASHBOARD_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_DASHBOARD_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_PROJECT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_DATA_COLLECTION_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_DATA_SPLIT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_MODEL_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_MODEL_METADATA_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_FEATURE_LIST_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_FILTER_TO_ROWSET_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MODIFY_PREDICTION_CACHE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MODIFY_EXPLANATION_CACHE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    INGEST_LABELS_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    INGEST_EXTRA_DATA_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    INGEST_PREDICTIONS_DATA_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_FEATURE_INFLUENCES_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_FEATURE_METADATA_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_SEGMENT_GROUP_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MODIFY_DATA_SOURCE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PAGE_VIEW_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    TEST_CREATED_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_QUICKSTART_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CLICK_CREATE_PROJECT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_STEP_PERSONAL_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_STEP_LANDING_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_STEP_WORKSPACE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    AUTH_ERROR_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_DATA_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    VISITED_PROJECT_LEADERBOARD_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    VISITED_MODEL_LEADER_BOARD_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CONTACT_SALES_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_INTERCOM_PRODUCT_TOUR_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DATA_SPLIT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DATA_COLLECTION_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MODEL_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROJECT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_DATA_COLLECTION_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_DATA_SPLIT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_MODEL_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_REPORT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    VISIT_REPORT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DELETE_REPORT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_REPORT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ADMIN_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_USER_AS_ADMIN_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    REMOVE_USER_AS_ADMIN_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_USER_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ADD_USER_TO_PROJECT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    REMOVE_USER_FROM_PROJECT_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    GRANT_ROLE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    REVOKE_ROLE_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    add_dashboard_event_properties: AddDashboardEventProperties
    update_dashboard_event_properties: UpdateDashboardEventProperties
    delete_dashboard_event_properties: DeleteDashboardEventProperties
    add_project_event_properties: AddProjectEventProperties
    add_data_collection_event_properties: AddDataCollectionEventProperties
    add_data_split_event_properties: AddDataSplitEventProperties
    add_model_event_properties: AddModelEventProperties
    add_model_metadata_event_properties: AddModelMetadataEventProperties
    add_feature_list_event_properties: AddFeatureListEventProperties
    add_filter_to_rowset_event_properties: AddFilterToRowsetEventProperties
    modify_prediction_cache_event_properties: ModifyPredictionCacheEventProperties
    modify_explanation_cache_event_properties: ModifyExplanationCacheEventProperties
    ingest_labels_event_properties: IngestLabelsEventProperties
    ingest_extra_data_event_properties: IngestExtraDataEventProperties
    ingest_predictions_data_event_properties: IngestPredictionsDataEventProperties
    add_feature_influences_event_properties: AddFeatureInfluencesEventProperties
    add_feature_metadata_event_properties: AddFeatureMetadataEventProperties
    add_segment_group_event_properties: AddSegmentGroupEventProperties
    modify_data_source_event_properties: ModifyDataSourceEventProperties
    page_view_event_properties: PageViewEventProperties
    test_created_event_properties: TestCreatedEventProperties
    launch_quickstart_event_properties: LaunchQuickstartEventProperties
    click_create_project_event_properties: ClickCreateProjectEventProperties
    signup_step_personal_event_properties: SignupStepPersonalEventProperties
    signup_step_landing_event_properties: SignupStepLandingEventProperties
    signup_step_workspace_event_properties: SignupStepWorkspaceEventProperties
    auth_error_event_properties: AuthErrorEventProperties
    add_data_event_properties: AddDataEventProperties
    visited_project_leaderboard_event_properties: VisitedProjectLeaderboardEventProperties
    visited_model_leader_board_event_properties: VisitedModelLeaderBoardEventProperties
    contact_sales_event_properties: ContactSalesEventProperties
    trigger_intercom_product_tour_event_properties: TriggerIntercomProductTourEventProperties
    update_data_split_event_properties: UpdateDataSplitEventProperties
    update_data_collection_event_properties: UpdateDataCollectionEventProperties
    update_model_event_properties: UpdateModelEventProperties
    delete_project_event_properties: DeleteProjectEventProperties
    delete_data_collection_event_properties: DeleteDataCollectionEventProperties
    delete_data_split_event_properties: DeleteDataSplitEventProperties
    delete_model_event_properties: DeleteModelEventProperties
    add_report_event_properties: AddReportEventProperties
    visit_report_event_properties: VisitReportEventProperties
    delete_report_event_properties: DeleteReportEventProperties
    update_report_event_properties: UpdateReportEventProperties
    authorization_admin_event_properties: AuthorizationEventProperties
    add_user_as_admin_event_properties: AuthorizationEventProperties
    remove_user_as_admin_event_properties: AuthorizationEventProperties
    add_user_event_properties: AuthorizationEventProperties
    add_user_to_project_event_properties: AuthorizationEventProperties
    remove_user_from_project_event_properties: AuthorizationEventProperties
    grant_role_event_properties: AuthorizationEventProperties
    revoke_role_event_properties: AuthorizationEventProperties
    def __init__(self, add_dashboard_event_properties: _Optional[_Union[AddDashboardEventProperties, _Mapping]] = ..., update_dashboard_event_properties: _Optional[_Union[UpdateDashboardEventProperties, _Mapping]] = ..., delete_dashboard_event_properties: _Optional[_Union[DeleteDashboardEventProperties, _Mapping]] = ..., add_project_event_properties: _Optional[_Union[AddProjectEventProperties, _Mapping]] = ..., add_data_collection_event_properties: _Optional[_Union[AddDataCollectionEventProperties, _Mapping]] = ..., add_data_split_event_properties: _Optional[_Union[AddDataSplitEventProperties, _Mapping]] = ..., add_model_event_properties: _Optional[_Union[AddModelEventProperties, _Mapping]] = ..., add_model_metadata_event_properties: _Optional[_Union[AddModelMetadataEventProperties, _Mapping]] = ..., add_feature_list_event_properties: _Optional[_Union[AddFeatureListEventProperties, _Mapping]] = ..., add_filter_to_rowset_event_properties: _Optional[_Union[AddFilterToRowsetEventProperties, _Mapping]] = ..., modify_prediction_cache_event_properties: _Optional[_Union[ModifyPredictionCacheEventProperties, _Mapping]] = ..., modify_explanation_cache_event_properties: _Optional[_Union[ModifyExplanationCacheEventProperties, _Mapping]] = ..., ingest_labels_event_properties: _Optional[_Union[IngestLabelsEventProperties, _Mapping]] = ..., ingest_extra_data_event_properties: _Optional[_Union[IngestExtraDataEventProperties, _Mapping]] = ..., ingest_predictions_data_event_properties: _Optional[_Union[IngestPredictionsDataEventProperties, _Mapping]] = ..., add_feature_influences_event_properties: _Optional[_Union[AddFeatureInfluencesEventProperties, _Mapping]] = ..., add_feature_metadata_event_properties: _Optional[_Union[AddFeatureMetadataEventProperties, _Mapping]] = ..., add_segment_group_event_properties: _Optional[_Union[AddSegmentGroupEventProperties, _Mapping]] = ..., modify_data_source_event_properties: _Optional[_Union[ModifyDataSourceEventProperties, _Mapping]] = ..., page_view_event_properties: _Optional[_Union[PageViewEventProperties, _Mapping]] = ..., test_created_event_properties: _Optional[_Union[TestCreatedEventProperties, _Mapping]] = ..., launch_quickstart_event_properties: _Optional[_Union[LaunchQuickstartEventProperties, _Mapping]] = ..., click_create_project_event_properties: _Optional[_Union[ClickCreateProjectEventProperties, _Mapping]] = ..., signup_step_personal_event_properties: _Optional[_Union[SignupStepPersonalEventProperties, _Mapping]] = ..., signup_step_landing_event_properties: _Optional[_Union[SignupStepLandingEventProperties, _Mapping]] = ..., signup_step_workspace_event_properties: _Optional[_Union[SignupStepWorkspaceEventProperties, _Mapping]] = ..., auth_error_event_properties: _Optional[_Union[AuthErrorEventProperties, _Mapping]] = ..., add_data_event_properties: _Optional[_Union[AddDataEventProperties, _Mapping]] = ..., visited_project_leaderboard_event_properties: _Optional[_Union[VisitedProjectLeaderboardEventProperties, _Mapping]] = ..., visited_model_leader_board_event_properties: _Optional[_Union[VisitedModelLeaderBoardEventProperties, _Mapping]] = ..., contact_sales_event_properties: _Optional[_Union[ContactSalesEventProperties, _Mapping]] = ..., trigger_intercom_product_tour_event_properties: _Optional[_Union[TriggerIntercomProductTourEventProperties, _Mapping]] = ..., update_data_split_event_properties: _Optional[_Union[UpdateDataSplitEventProperties, _Mapping]] = ..., update_data_collection_event_properties: _Optional[_Union[UpdateDataCollectionEventProperties, _Mapping]] = ..., update_model_event_properties: _Optional[_Union[UpdateModelEventProperties, _Mapping]] = ..., delete_project_event_properties: _Optional[_Union[DeleteProjectEventProperties, _Mapping]] = ..., delete_data_collection_event_properties: _Optional[_Union[DeleteDataCollectionEventProperties, _Mapping]] = ..., delete_data_split_event_properties: _Optional[_Union[DeleteDataSplitEventProperties, _Mapping]] = ..., delete_model_event_properties: _Optional[_Union[DeleteModelEventProperties, _Mapping]] = ..., add_report_event_properties: _Optional[_Union[AddReportEventProperties, _Mapping]] = ..., visit_report_event_properties: _Optional[_Union[VisitReportEventProperties, _Mapping]] = ..., delete_report_event_properties: _Optional[_Union[DeleteReportEventProperties, _Mapping]] = ..., update_report_event_properties: _Optional[_Union[UpdateReportEventProperties, _Mapping]] = ..., authorization_admin_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., add_user_as_admin_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., remove_user_as_admin_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., add_user_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., add_user_to_project_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., remove_user_from_project_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., grant_role_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ..., revoke_role_event_properties: _Optional[_Union[AuthorizationEventProperties, _Mapping]] = ...) -> None: ...

class AddDashboardEventProperties(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class UpdateDashboardEventProperties(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class DeleteDashboardEventProperties(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class AddProjectEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...

class AddDataCollectionEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ...) -> None: ...

class AddDataSplitEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name", "predictions_ingested", "labels_ingested", "extra_data_ingested")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    LABELS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    predictions_ingested: str
    labels_ingested: str
    extra_data_ingested: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., predictions_ingested: _Optional[str] = ..., labels_ingested: _Optional[str] = ..., extra_data_ingested: _Optional[str] = ...) -> None: ...

class AddModelEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "model_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    model_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class AddModelMetadataEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "model_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    model_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class AddFeatureListEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_collection_name", "feature_list_id")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_LIST_ID_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_collection_name: str
    feature_list_id: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., feature_list_id: _Optional[str] = ...) -> None: ...

class AddFilterToRowsetEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_source_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_source_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_source_name: _Optional[str] = ...) -> None: ...

class ModifyPredictionCacheEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_collection_name", "data_split_name", "command", "data_source_name", "score_type")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_collection_name: str
    data_split_name: str
    command: str
    data_source_name: str
    score_type: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., command: _Optional[str] = ..., data_source_name: _Optional[str] = ..., score_type: _Optional[str] = ...) -> None: ...

class ModifyExplanationCacheEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_collection_name", "data_split_name", "command", "data_source_name", "score_type")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_collection_name: str
    data_split_name: str
    command: str
    data_source_name: str
    score_type: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., command: _Optional[str] = ..., data_source_name: _Optional[str] = ..., score_type: _Optional[str] = ...) -> None: ...

class IngestLabelsEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_collection_name", "data_split_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_collection_name: str
    data_split_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ...) -> None: ...

class IngestExtraDataEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "data_collection_name", "data_split_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    data_collection_name: str
    data_split_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ...) -> None: ...

class IngestPredictionsDataEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ...) -> None: ...

class AddFeatureInfluencesEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ...) -> None: ...

class AddFeatureMetadataEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ...) -> None: ...

class AddSegmentGroupEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ...) -> None: ...

class ModifyDataSourceEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_source_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_source_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_source_name: _Optional[str] = ...) -> None: ...

class PageViewEventProperties(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: str
    def __init__(self, location: _Optional[str] = ...) -> None: ...

class TestCreatedEventProperties(_message.Message):
    __slots__ = ("test_definition",)
    TEST_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    test_definition: str
    def __init__(self, test_definition: _Optional[str] = ...) -> None: ...

class LaunchQuickstartEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClickCreateProjectEventProperties(_message.Message):
    __slots__ = ("new_project_name",)
    NEW_PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    new_project_name: str
    def __init__(self, new_project_name: _Optional[str] = ...) -> None: ...

class SignupStepPersonalEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignupStepLandingEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignupStepWorkspaceEventProperties(_message.Message):
    __slots__ = ("workspace_name",)
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ...) -> None: ...

class AuthErrorEventProperties(_message.Message):
    __slots__ = ("auth_error_type", "auth_error_desc")
    AUTH_ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTH_ERROR_DESC_FIELD_NUMBER: _ClassVar[int]
    auth_error_type: str
    auth_error_desc: str
    def __init__(self, auth_error_type: _Optional[str] = ..., auth_error_desc: _Optional[str] = ...) -> None: ...

class AddDataEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name", "predictions_ingested", "labels_ingested", "extra_data_ingested", "pre_data_ingested", "post_data_ingested", "feature_influences_ingested")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    LABELS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    PRE_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    POST_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCES_INGESTED_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    predictions_ingested: str
    labels_ingested: str
    extra_data_ingested: str
    pre_data_ingested: str
    post_data_ingested: str
    feature_influences_ingested: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., predictions_ingested: _Optional[str] = ..., labels_ingested: _Optional[str] = ..., extra_data_ingested: _Optional[str] = ..., pre_data_ingested: _Optional[str] = ..., post_data_ingested: _Optional[str] = ..., feature_influences_ingested: _Optional[str] = ...) -> None: ...

class VisitedProjectLeaderboardEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VisitedModelLeaderBoardEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ContactSalesEventProperties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TriggerIntercomProductTourEventProperties(_message.Message):
    __slots__ = ("tour_name",)
    TOUR_NAME_FIELD_NUMBER: _ClassVar[int]
    tour_name: str
    def __init__(self, tour_name: _Optional[str] = ...) -> None: ...

class UpdateDataCollectionEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ...) -> None: ...

class UpdateDataSplitEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name", "predictions_ingested", "labels_ingested", "extra_data_ingested")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    LABELS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    predictions_ingested: str
    labels_ingested: str
    extra_data_ingested: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., predictions_ingested: _Optional[str] = ..., labels_ingested: _Optional[str] = ..., extra_data_ingested: _Optional[str] = ...) -> None: ...

class UpdateModelEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "model_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    model_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class DeleteProjectEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "is_recursive")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    IS_RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    is_recursive: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., is_recursive: _Optional[str] = ...) -> None: ...

class DeleteDataCollectionEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ...) -> None: ...

class DeleteDataSplitEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "data_split_name", "predictions_ingested", "labels_ingested", "extra_data_ingested")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    LABELS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_INGESTED_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    data_split_name: str
    predictions_ingested: str
    labels_ingested: str
    extra_data_ingested: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., data_split_name: _Optional[str] = ..., predictions_ingested: _Optional[str] = ..., labels_ingested: _Optional[str] = ..., extra_data_ingested: _Optional[str] = ...) -> None: ...

class DeleteModelEventProperties(_message.Message):
    __slots__ = ("workspace", "project_name", "command", "data_collection_name", "model_name")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    project_name: str
    command: str
    data_collection_name: str
    model_name: str
    def __init__(self, workspace: _Optional[str] = ..., project_name: _Optional[str] = ..., command: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class AddReportEventProperties(_message.Message):
    __slots__ = ("report_title",)
    REPORT_TITLE_FIELD_NUMBER: _ClassVar[int]
    report_title: str
    def __init__(self, report_title: _Optional[str] = ...) -> None: ...

class VisitReportEventProperties(_message.Message):
    __slots__ = ("report_title",)
    REPORT_TITLE_FIELD_NUMBER: _ClassVar[int]
    report_title: str
    def __init__(self, report_title: _Optional[str] = ...) -> None: ...

class DeleteReportEventProperties(_message.Message):
    __slots__ = ("report_title",)
    REPORT_TITLE_FIELD_NUMBER: _ClassVar[int]
    report_title: str
    def __init__(self, report_title: _Optional[str] = ...) -> None: ...

class UpdateReportEventProperties(_message.Message):
    __slots__ = ("report_title",)
    REPORT_TITLE_FIELD_NUMBER: _ClassVar[int]
    report_title: str
    def __init__(self, report_title: _Optional[str] = ...) -> None: ...

class AuthorizationEventProperties(_message.Message):
    __slots__ = ("event_type", "auth_status", "resource_id", "resource_type", "action", "subject_id", "role_id")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTH_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    auth_status: str
    resource_id: str
    resource_type: str
    action: str
    subject_id: str
    role_id: str
    def __init__(self, event_type: _Optional[str] = ..., auth_status: _Optional[str] = ..., resource_id: _Optional[str] = ..., resource_type: _Optional[str] = ..., action: _Optional[str] = ..., subject_id: _Optional[str] = ..., role_id: _Optional[str] = ...) -> None: ...
