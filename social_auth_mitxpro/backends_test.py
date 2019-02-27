"""Tests for our backend"""
import pytest

from social_auth_mitxpro.backends import MITxProOAuth2

# pylint: disable=redefined-outer-name


@pytest.fixture
def strategy(mocker):
    """Mock strategy"""
    return mocker.Mock()


@pytest.fixture
def backend(strategy):
    """MITxProOAuth2 backend fixture"""
    return MITxProOAuth2(strategy)


@pytest.mark.parametrize(
    "response, expected",
    [
        (
            {"username": "abc123", "email": "user@example.com", "name": "Jane Doe"},
            {"username": "abc123", "email": "user@example.com", "name": "Jane Doe"},
        ),
        ({"username": "abc123"}, {"username": "abc123", "email": "", "name": ""}),
    ],
)
def test_get_user_details(backend, response, expected):
    """Test that get_user_details produces expected results"""
    assert backend.get_user_details(response) == expected


@pytest.mark.parametrize(
    "api_root", ["http://xpro.example.com/", "http://xpro.example.com"]
)
def test_user_data(backend, strategy, mocked_responses, api_root):
    """Tests that the backend makes a correct appropriate request"""
    access_token = "user_token"
    response = {"username": "abc123", "email": "user@example.com", "name": "Jane Doe"}

    mocked_responses.add(
        mocked_responses.GET, "http://xpro.example.com/api/users/me", json=response
    )

    strategy.setting.return_value = api_root

    assert backend.user_data(access_token)

    request, _ = mocked_responses.calls[0]

    assert request.headers["Authorization"] == "Bearer user_token"
    strategy.setting.assert_any_call("API_ROOT", default=None, backend=backend)


def test_authorization_url(backend, strategy):
    """Test authorization_url()"""
    strategy.setting.return_value = "abc"
    assert backend.authorization_url() == "abc"
    strategy.setting.assert_called_once_with(
        "AUTHORIZATION_URL", default=None, backend=backend
    )


def test_access_token_url(backend, strategy):
    """Test access_token_url()"""
    strategy.setting.return_value = "abc"
    assert backend.access_token_url() == "abc"
    strategy.setting.assert_called_once_with(
        "ACCESS_TOKEN_URL", default=None, backend=backend
    )
