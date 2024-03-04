from unittest.mock import MagicMock, patch
import pytest
from collections import namedtuple
from robot_azure_sync_get import create_robot_content, process_new_test_cases


# Fixture para campos mockados do Azure Test Case work item
@pytest.fixture
def fields():
    return {
        "System.Id": "1",
        "System.Title": "Test Case Title",
        "System.IterationPath": "Iteration Path",
        "Microsoft.VSTS.Common.Priority": "High",
        "Microsoft.VSTS.TCM.AutomationStatus": "Automated",
        "Sprint": "Sprint 1",
        "System.Tags": "tag1; tag2",
    }


# Fixture para configuração de prefixo mockada
@pytest.fixture
def pref_config():
    return {
        "prefix_test_case": "[TestCase]",
        "prefix_automation_status": "[AutomationStatus]",
        "prefix_priority": "[Priority]",
        "prefix_iteration_path": "[IterationPath]",
        "title": "[Title]",
    }


# Teste de Caso Básico
def test_create_robot_content_basic(fields, pref_config):
    result = create_robot_content(fields, pref_config)
    assert "Test Case Title" in result
    assert "[tags]  TestCase 1" in result


# Teste de Caso com Campos Nulos
def test_create_robot_content_null_fields(fields, pref_config):
    fields.clear()
    result = create_robot_content(fields, pref_config)
    assert (
        result
        == "\n[Title] \n    [tags]  TestCase     Automation_Status     Priority     Iteration \n\n"
    )


# Teste de Caso com Etapas e Resultados Esperados
def test_create_robot_content_with_steps_and_expected_results(fields, pref_config):
    fields["Microsoft.VSTS.TCM.Steps"] = (
        '<steps id="0" last="1"><step id="1" type="ActionStep"><parameterizedString isformatted="true">&lt;P&gt;Passo 1&lt;BR/&gt;&lt;/P&gt;</parameterizedString><parameterizedString isformatted="true">&lt;DIV&gt;&lt;P&gt;&lt;BR/&gt;&lt;/P&gt;&lt;/DIV&gt;</parameterizedString><description/></step><step id="2" type="ActionStep"><parameterizedString isformatted="true">&lt;P&gt;Passo 2&lt;BR/&gt;&lt;/P&gt;</parameterizedString><parameterizedString isformatted="true">&lt;DIV&gt;&lt;P&gt;&lt;BR/&gt;&lt;/P&gt;&lt;/DIV&gt;</parameterizedString><description/></step></steps>'
    )
    result = create_robot_content(fields, pref_config)
    assert "Passo 1" in result
    assert "Passo 2" in result


# Teste de Caso com Tags de Sistema Vazias
def test_create_robot_content_empty_system_tags(fields, pref_config):
    fields["System.Tags"] = None
    result = create_robot_content(fields, pref_config)
    assert "[System_Tags]" not in result


# Teste de Caso com Relações Vazias
def test_create_robot_content_empty_relations(fields, pref_config):
    fields["relations"] = []
    result = create_robot_content(fields, pref_config)
    assert "[User_Story]" not in result


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "value": [
            {
                "fields": {
                    "System.Title": "Test Case Title",
                    "System.ChangedDate": "2024-02-15T10:00:00.000Z",
                }
            }
        ]
    }
    return response


@pytest.fixture
def mock_requests_get(mock_response):
    with patch("robot_azure_sync_get.requests.get") as mock_get:
        mock_get.return_value = mock_response
        yield mock_get


@patch("requests.get")
def test_process_new_test_cases(mock_requests_get):
    new_test_case_ids = {1, 2, 3}
    robot_test_case_ids = {3, 4, 5}
    url = "https://your-azure-devops-instance/"
    headers = {"Authorization": "Bearer your_access_token"}

    responses = [
        MagicMock(
            status_code=200,
            json=lambda: {
                "value": [
                    {
                        "fields": {
                            "System.Title": "Test Case Title",
                            "System.ChangedDate": "2024-02-15T10:00:00.000Z",
                        }
                    }
                ]
            },
        ),
        MagicMock(
            status_code=200,
            json=lambda: {
                "value": [
                    {
                        "fields": {
                            "System.Title": "Test Case Title 2",
                            "System.ChangedDate": "2024-02-15T11:00:00.000Z",
                        }
                    }
                ]
            },
        ),
        MagicMock(
            status_code=200,
            json=lambda: {
                "value": [
                    {
                        "fields": {
                            "System.Title": "Test Case Title 3",
                            "System.ChangedDate": "2024-02-15T12:00:00.000Z",
                        }
                    }
                ]
            },
        ),
    ]

    mock_requests_get.side_effect = responses

    expected_result = [
        {
            "value": [
                {
                    "fields": {
                        "System.Title": "Test Case Title",
                        "System.ChangedDate": "2024-02-15T10:00:00.000Z",
                    }
                }
            ]
        },
        {
            "value": [
                {
                    "fields": {
                        "System.Title": "Test Case Title 2",
                        "System.ChangedDate": "2024-02-15T11:00:00.000Z",
                    }
                }
            ]
        }
    ]

    result = process_new_test_cases(
        new_test_case_ids, robot_test_case_ids, url, headers
    )

    # Verifica se cada item em result está presente em expected_result
    for res in result:
        assert res in expected_result

    assert mock_requests_get.call_count == 2
