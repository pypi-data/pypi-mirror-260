from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Iterator
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.model import Model
from fiddler.schemas.custom_metric import (
    CustomExpressionResp,
    CustomMetricResp,
    SegmentResp,
)
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.utils.helpers import raise_not_found


class CustomExpression(BaseEntity):
    def __init__(
        self,
        name: str,
        model_id: UUID,
        definition: str,
        description: str | None = None,
    ) -> None:
        """Construct a custom expression instance."""
        self.name = name
        self.model_id = model_id
        self.definition = definition
        self.description = description

        self.id: UUID | None = None
        self.created_at: datetime | None = None

        # Deserialized response object
        self._resp: CustomExpressionResp | None = None

    @staticmethod
    @abstractmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get custom expression resource/item url."""

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = CustomMetricResp(**data)
        assert self.model_id
        fields = [
            'id',
            'name',
            'definition',
            'description',
            'created_at',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @classmethod
    def _from_dict(cls, data: dict) -> CustomExpression:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = CustomMetricResp(**data)
        model = Model.from_name(
            name=resp_obj.model_name, project_name=resp_obj.project_name
        )
        assert model.id
        # Initialize
        instance = cls(
            name=resp_obj.name,
            model_id=model.id,
            definition=resp_obj.definition,
            description=resp_obj.description,
        )

        # Add remaining fields
        fields = [
            'id',
            'created_at',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj

        return instance

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> CustomExpression:
        """
        Get the CustomMetric instance using custom metric id.

        :param id_: unique uuid format identifier for custom metric
        :return: CustomMetric instance
        """
        response = cls._client().get(url=cls._get_url(id_=id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(
        cls, name: str, model_name: str, project_name: str
    ) -> CustomExpression:
        """
        Get the custom metric instance using custom metric name, model name and project name.

        :param name: Custom metric name
        :param model_name: Name of the model associated with the custom metric
        :param project_name: Name of the project associated with the custom metric

        :return: CustomMetric instance for the provided params
        """

        _filter = QueryCondition(
            rules=[
                QueryRule(field='name', operator=OperatorType.EQUAL, value=name),
            ]
        )
        params: dict[str, Any] = {
            'filter': _filter.json(),
            'organization_name': cls.get_organization_name(),
            'project_name': project_name,
            'model_name': model_name,
        }

        response = cls._client().get(
            url=cls._get_url(),
            params=params,
        )
        if response.json()['data']['total'] == 0:
            raise_not_found('Custom metric not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(
        cls,
        model_id: UUID,
    ) -> Iterator[CustomExpression]:
        """Get a list of all custom metrics in the organization."""

        model = Model.get(id_=model_id)
        params: dict[str, Any] = {
            'organization_name': cls.get_organization_name(),
            'project_name': model.project.name,
            'model_name': model.name,
        }

        for custom_metric in cls._paginate(
            url=cls._get_url(),
            params=params,
        ):
            yield cls._from_dict(data=custom_metric)

    @handle_api_error
    def create(self) -> CustomExpression:
        """Create a new custom metric."""
        model = Model.get(id_=self.model_id)
        payload = {
            'name': self.name,
            'organization_name': self.get_organization_name(),
            'project_name': model.project.name,
            'model_name': model.name,
            'definition': self.definition,
        }

        if self.description:
            payload['description'] = self.description

        response = self._client().post(
            url=self._get_url(),
            data=payload,
        )
        self._refresh_from_response(response=response)
        return self

    @handle_api_error
    def delete(self) -> None:
        """Delete a custom metric."""
        assert self.id is not None

        self._client().delete(url=self._get_url(id_=self.id))


class CustomMetric(CustomExpression):
    def __init__(
        self, name: str, model_id: UUID, definition: str, description: str | None = None
    ) -> None:
        """Construct a custom metric instance."""
        super().__init__(name, model_id, definition, description)

        # Deserialized response object
        self._resp: CustomMetricResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get custom metric resource/item url."""
        url = '/v2/custom-metrics'
        return url if not id_ else f'{url}/{id_}'


class Segment(CustomExpression):
    def __init__(
        self, name: str, model_id: UUID, definition: str, description: str | None = None
    ) -> None:
        """Construct a segment instance."""
        super().__init__(name, model_id, definition, description)

        # Deserialized response object
        self._resp: SegmentResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get segment resource/item url."""
        url = '/v2/segments'
        return url if not id_ else f'{url}/{id_}'
