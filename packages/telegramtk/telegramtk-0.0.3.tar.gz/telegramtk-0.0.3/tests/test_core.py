import pytest
from prettyconf import config

import tgutils


@pytest.fixture
def token():
    return config('BOT_TOKEN')


@pytest.fixture
def recipient():
    return config('RECIPIENT')


@pytest.fixture
def msg():
    return 'Hello'


def test_if_send_message_fails_when_token_is_unset(recipient, msg):
    with pytest.raises(ValueError, match='Bot token is undefined! Use init()'):
        tgutils.send_message(recipient, msg)


def test_send_message_works(token, recipient, msg):
    tgutils.init(token)
    tgutils.send_message(recipient, msg)
