#
# Copyright 2021-2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from enum import Enum
from typing import cast, List, Optional, Set

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.models.custom_jobs.custom_job import (
    CustomJob,
    CustomJobFileItem,
    CustomJobFileItemType,
)
from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.errors import ClientError
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class CustomJobRunStatus(Enum):
    """Enum of the custom job run statuses"""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RUNNING = "running"
    INTERRUPTED = "interrupted"
    CANCELING = "canceling"
    CANCELED = "canceled"


class CustomJobRun(APIObject):
    """A DataRobot custom job run.

    .. versionadded:: v2.33

    Attributes
    ----------
    id: str
        id of the custom job run
    custom_job_id: str
        id of the parent custom job
    description: str
        description of the custom job run
    created_at: str
        ISO-8601 formatted timestamp of when the version was created
    items: List[CustomJobFileItem]
        a list of file items attached to the custom job
    status: CustomJobRunStatus
        status of the custom job run
    duration: float
        duration of the custom job run
    """

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("custom_job_id"): String(),
            t.Key("description", optional=True): t.Or(
                String(max_length=10000, allow_blank=True), t.Null()
            ),
            t.Key("created") >> "created_at": String(),
            t.Key("items"): t.List(CustomJobFileItem.schema),
            t.Key("status"): t.Enum(*[e.value for e in CustomJobRunStatus]),
            t.Key("duration"): t.Float(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        custom_job_id: str,
        created_at: str,
        items: List[CustomJobFileItemType],
        status: str,
        duration: float,
        description: Optional[str] = None,
    ) -> None:
        self.id = id
        self.custom_job_id = custom_job_id
        self.description = description
        self.created_at = created_at

        # NOTE: CustomJobFileItem's __init__ instead of from_server_data is used, because at this point
        #   the data is already converted from API representation to "object" representation.
        #   In case of CustomJobFileItem it converted {"created": ..., ...} to {"created_at": ..., ...}.
        #   For type hinting, TypedDict CustomJobFileItemType is used, which reflects expected property names and types.
        self.items = [CustomJobFileItem(**data) for data in items]

        self.status = CustomJobRunStatus(status)
        self.duration = duration

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id!r})"

    def _update_values(self, new_response: CustomJobRun) -> None:
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def _custom_job_run_base_path(cls, custom_job_id: str) -> str:
        return f"customJobs/{custom_job_id}/runs/"

    @classmethod
    def _custom_job_run_path(cls, custom_job_id: str, custom_job_run_id: str) -> str:
        return f"customJobs/{custom_job_id}/runs/{custom_job_run_id}/"

    @classmethod
    def _custom_job_run_logs_path(cls, custom_job_id: str, custom_job_run_id: str) -> str:
        return f"customJobs/{custom_job_id}/runs/{custom_job_run_id}/logs/"

    @classmethod
    def create(
        cls,
        custom_job_id: str,
        max_wait: Optional[int] = DEFAULT_MAX_WAIT,
    ) -> CustomJobRun:
        """Create a custom job run.

        .. versionadded:: v2.33

        Parameters
        ----------
        custom_job_id: str
            the id of the custom job
        max_wait: int, optional
            max time to wait for a terminal status ("succeeded", "failed", "interrupted", "canceled").
            If set to None - method will return without waiting.

        Returns
        -------
        CustomJob
            created custom job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        ValueError
            if execution environment or entry point is not specified for the custom job
        """

        custom_job = CustomJob.get(custom_job_id)
        if not custom_job.environment_id:
            raise ValueError("Environment ID must be set for the custom job in order to be run")
        if not custom_job.entry_point:
            raise ValueError("Entry point must be set for the custom job in order to be run")

        path = cls._custom_job_run_base_path(custom_job_id)

        response = cls._client.post(path)

        data = response.json()

        if max_wait is None:
            return cls.from_server_data(data)

        custom_job_run_loc = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        return cls.from_location(custom_job_run_loc)

    @classmethod
    def list(cls, custom_job_id: str) -> List[CustomJobRun]:
        """List custom job runs.

        .. versionadded:: v2.33

        Parameters
        ----------
        custom_job_id: str
            the id of the custom job

        Returns
        -------
        List[CustomJob]
            a list of custom job runs

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(cls._custom_job_run_base_path(custom_job_id), None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_job_id: str, custom_job_run_id: str) -> CustomJobRun:
        """Get custom job run by id.

        .. versionadded:: v2.33

        Parameters
        ----------
        custom_job_id: str
            the id of the custom job
        custom_job_run_id: str
            the id of the custom job run

        Returns
        -------
        CustomJob
            retrieved custom job run

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._custom_job_run_path(custom_job_id, custom_job_run_id)
        return cls.from_location(path)

    def update(self, description: Optional[str] = None) -> None:
        """Update custom job run properties.

        .. versionadded:: v2.33

        Parameters
        ----------
        description: str
            new custom job run description

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {}
        if description:
            payload.update({"description": description})

        path = self._custom_job_run_path(self.custom_job_id, self.id)

        response = self._client.patch(path, data=payload)

        data = response.json()
        new_version = CustomJobRun.from_server_data(data)
        self._update_values(new_version)

    def cancel(self) -> None:
        """Cancel custom job run.

        .. versionadded:: v2.33

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        url = self._custom_job_run_path(self.custom_job_id, self.id)
        self._client.delete(url)

    def refresh(self) -> None:
        """Update custom job run with the latest data from server.

        .. versionadded:: v2.33

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        new_object = self.get(self.custom_job_id, self.id)
        self._update_values(new_object)

    def get_logs(self) -> Optional[str]:
        """Get log of the custom job run.

        .. versionadded:: v2.33

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = self._custom_job_run_logs_path(self.custom_job_id, self.id)
        try:
            response = self._client.get(path)
            return cast(str, response.text)
        except ClientError as exc:
            if exc.status_code == 404 and exc.json == {"message": "No log found"}:
                return None
            raise

    def delete_logs(self) -> None:
        """Get log of the custom job run.

        .. versionadded:: v2.33

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = self._custom_job_run_logs_path(self.custom_job_id, self.id)
        self._client.delete(path)
