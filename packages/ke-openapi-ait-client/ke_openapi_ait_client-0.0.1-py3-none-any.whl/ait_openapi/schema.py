from datetime import datetime
from typing import Optional

import uuid
from pydantic import BaseModel, Field, root_validator
from .openapi_contexvar import trace_id_context, caller_id_context, request_url_context


class OperationLog(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: Optional[str] = Field(default_factory=lambda: trace_id_context.get(),
                            alias='requestId')
    caller_id: Optional[str] = Field(default_factory=lambda: caller_id_context.get(),
                           alias='callerId')
    request_url: Optional[str] = Field(default_factory=lambda: request_url_context.get(),
                             alias='requestUrl')
    op_log_type: str = Field(alias='opLogType')
    op_type: str = Field(alias='opType')
    is_cost_log: bool = Field(default=False, alias='isCostLog')
    operation_status: str = Field(alias='operationStatus')
    start_time_millis: int = Field(default_factory=lambda: int(datetime.now().timestamp()),
                                   alias='startTimeMillis')
    duration_millis: int = Field(default=0, alias='durationMillis')
    request: object
    response: object = Field(default=None)
    err_msg: Optional[str] = Field(default=None, alias='errMsg')
    extra_info: dict = Field(default={}, alias='extraInfo')

    @root_validator
    def validate_duration_millis(cls, values):
        if values['request_id'] is None:
            raise ValueError('request_id is required, please set trace_id_context')
        if values['caller_id'] is None:
            raise ValueError('caller_id is required, please set caller_id_context')
        if values['request_url'] is None:
            raise ValueError('request_url is required, please set request_url_context')
        return values
