from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from responses import matchers

from fiddler.entities.custom_metric import CustomMetric
from fiddler.exceptions import Conflict, NotFound
from fiddler.tests.apis.test_model import API_RESPONSE_200 as MODEL_API_RESPONSE_200
from fiddler.tests.apis.test_model import (
    API_RESPONSE_FROM_NAME as MODEL_API_RESPONSE_FROM_NAME,
)
from fiddler.tests.constants import MODEL_ID, MODEL_NAME, ORG_NAME, PROJECT_NAME, URL

CUSTOM_METRIC_ID = '7057867c-6dd8-4915-89f2-a5f253dd4a3a'
CUSTOM_METRIC_NAME = 'xyzabc'

API_RESPONSE_200 = {
    'data': {
        'description': 'meh',
        'definition': "average(\"Age\")",
        'created_by': {
            'id': 2,
            'full_name': 'Nikhil Singh',
            'email': 'nikhil@fiddler.ai',
        },
        'name': CUSTOM_METRIC_NAME,
        'id': CUSTOM_METRIC_ID,
        'organization_name': ORG_NAME,
        'model_name': MODEL_NAME,
        'project_name': PROJECT_NAME,
        'created_at': '2024-02-13T07:56:04.275549+00:00',
    },
    'api_version': '2.0',
    'kind': 'NORMAL',
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': "CustomMetric({'uuid': UUID('7057867c-6dd8-4915-89f2-a5f253dd4a3a')}) not found",
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': "CustomMetric({'uuid': UUID('7057867c-6dd8-4915-89f2-a5f253dd4a3a')}) not found",
                'help': '',
            }
        ],
    },
    'api_version': '2.0',
    'kind': 'ERROR',
}

API_RESPONSE_FROM_NAME = {
    'data': {
        'page_size': 100,
        'total': 1,
        'item_count': 1,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [API_RESPONSE_200['data']],
    }
}

EMPTY_LIST_API_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 0,
        'item_count': 0,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [],
    }
}

LIST_API_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [
            API_RESPONSE_200['data'],
            {
                'description': 'meh',
                'definition': "average(\"Age\")",
                'created_by': {
                    'id': 2,
                    'full_name': 'Nikhil Singh',
                    'email': 'nikhil@fiddler.ai',
                },
                'name': 'abcxyz',
                'id': 'a509c450-c00b-4b5c-9a96-89c43e287e5a',
                'organization_name': ORG_NAME,
                'model_name': MODEL_NAME,
                'project_name': PROJECT_NAME,
                'created_at': '2024-02-12T07:56:04.275549+00:00',
            },
        ],
    }
}

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': 'Custom metric with the same name already exists for this model',
        'errors': [
            {
                'reason': 'Conflict',
                'message': 'Custom metric with the same name already exists for this model',
                'help': '',
            }
        ],
    },
    'api_version': '2.0',
    'kind': 'ERROR',
}


@responses.activate
def test_get_custom_metric() -> None:
    responses.get(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
        json=API_RESPONSE_200,
    )

    responses.get(
        url=f'{URL}/v3/models',
        json=MODEL_API_RESPONSE_FROM_NAME,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )

    cm = CustomMetric.get(id_=CUSTOM_METRIC_ID)
    assert isinstance(cm, CustomMetric)


@responses.activate
def test_get_cm_not_found() -> None:
    responses.get(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        CustomMetric.get(id_=CUSTOM_METRIC_ID)


@responses.activate
def test_cm_from_name() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "xyzabc"}]}',
        'model_name': 'bank_churn',
        'organization_name': 'fiddler_dev',
        'project_name': 'bank_churn',
    }

    responses.get(
        url=f'{URL}/v2/custom-metrics',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    responses.get(
        url=f'{URL}/v3/models',
        json=MODEL_API_RESPONSE_FROM_NAME,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    cm = CustomMetric.from_name(
        name=CUSTOM_METRIC_NAME,
        model_name=MODEL_NAME,
        project_name=PROJECT_NAME,
    )
    assert isinstance(cm, CustomMetric)


@responses.activate
def test_cm_from_name_not_found() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "xyzabc"}]}',
        'model_name': 'bank_churn',
        'organization_name': 'fiddler_dev',
        'project_name': 'bank_churn',
    }
    responses.get(
        url=f'{URL}/v2/custom-metrics',
        json=EMPTY_LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )
    with pytest.raises(NotFound):
        CustomMetric.from_name(
            name=CUSTOM_METRIC_NAME,
            model_name=MODEL_NAME,
            project_name=PROJECT_NAME,
        )


@responses.activate
def test_cm_list_empty() -> None:
    responses.get(
        url=f'{URL}/v2/custom-metrics',
        json=EMPTY_LIST_API_RESPONSE,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )

    assert len(list(CustomMetric.list(model_id=MODEL_ID))) == 0


@responses.activate
def test_cm_list_success() -> None:
    params = {
        'organization_name': ORG_NAME,
        'project_name': PROJECT_NAME,
        'model_name': MODEL_NAME,
        'limit': 50,
        'offset': 0,
    }

    responses.get(
        url=f'{URL}/v2/custom-metrics',
        json=LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )

    responses.get(
        url=f'{URL}/v3/models',
        json=MODEL_API_RESPONSE_FROM_NAME,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )

    for cm in CustomMetric.list(model_id=MODEL_ID):
        assert isinstance(cm, CustomMetric)


@responses.activate
def test_cm_create() -> None:
    responses.post(
        url=f'{URL}/v2/custom-metrics',
        json=API_RESPONSE_200,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )

    custom_metric = CustomMetric(
        name=CUSTOM_METRIC_NAME,
        model_id=MODEL_ID,
        definition="average(\"Age\")",
        description='meh',
    ).create()

    assert isinstance(custom_metric, CustomMetric)
    assert custom_metric.id == UUID(CUSTOM_METRIC_ID)
    assert custom_metric.name == CUSTOM_METRIC_NAME
    assert custom_metric.model_id


@responses.activate
def test_cm_create_conflict() -> None:
    responses.post(
        url=f'{URL}/v2/custom-metrics',
        json=API_RESPONSE_409,
        status=HTTPStatus.CONFLICT,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )

    with pytest.raises(Conflict):
        CustomMetric(
            name=CUSTOM_METRIC_NAME,
            model_id=MODEL_ID,
            definition="average(\"Age\")",
            description='meh',
        ).create()


@responses.activate
def test_delete_cm() -> None:
    responses.get(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
        json=API_RESPONSE_200,
    )

    responses.get(
        url=f'{URL}/v3/models',
        json=MODEL_API_RESPONSE_FROM_NAME,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    custom_metric = CustomMetric.get(id_=CUSTOM_METRIC_ID)

    responses.delete(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
    )

    custom_metric.delete()


@responses.activate
def test_delete_cm_not_found() -> None:
    responses.get(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
        json=API_RESPONSE_200,
    )

    responses.get(
        url=f'{URL}/v3/models',
        json=MODEL_API_RESPONSE_FROM_NAME,
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    custom_metric = CustomMetric.get(id_=CUSTOM_METRIC_ID)

    responses.delete(
        url=f'{URL}/v2/custom-metrics/{CUSTOM_METRIC_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        custom_metric.delete()
