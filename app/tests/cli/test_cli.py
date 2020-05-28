import string
from random import choice, randint

import pytest
from click.testing import CliRunner

from app.cli.cli import cli


@pytest.fixture()
def auth():
    login = ''
    password = ''
    length_login = randint(3, 15)
    length_password = randint(8, 25)
    while length_login:
        login += choice(string.ascii_letters)
        length_login -= 1
    while length_password:
        password += choice(string.ascii_letters + string.digits)
        length_password -= 1

    return f'{login}@{password}'


@pytest.fixture()
def token():
    token = ''
    lenght_token = 85
    while lenght_token:
        token += choice('abcdef' + string.digits)
        lenght_token -= 1
    return token


@pytest.fixture()
def broken_token():
    token = ''
    lenght_token = randint(1, 84)
    while lenght_token:
        token += choice('abcdef' + string.digits)
        lenght_token -= 1
    return token


def test_aush_data_login_pass(auth):
    this_auth = auth
    runner = CliRunner()
    result = runner.invoke(cli, input=auth)
    assert result.exit_code == 0
    assert result.output == f"Введите токен или  логин@пароль для получения токена или оставьте пустым для отмены: {this_auth}\n"


def test_aush_data_token(token):
    this_token = token
    runner = CliRunner()
    result = runner.invoke(cli, input=token)
    assert result.exit_code == 0
    assert result.output == f"Введите токен или  логин@пароль для получения токена или оставьте пустым для отмены: {this_token}\n"


def test_token_args(token):
    runner = CliRunner()
    result = runner.invoke(cli, args=f'--auth={token}')
    assert result.exit_code == 0


def test_broken_token(broken_token):
    runner = CliRunner()
    result = runner.invoke(cli, args=f'--auth={broken_token}')
    assert result.exit_code == 2
