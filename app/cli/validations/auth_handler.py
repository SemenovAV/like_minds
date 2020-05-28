import re

import click


def is_auth_data(data):
    patern = '.+@.+'
    return re.fullmatch(patern, data)


def is_token(data):
    patern = '[0-9a-f]{85}'
    return re.fullmatch(patern, data)


def get_auth(data, logger):
    if is_auth_data(data):
        auth = data.split('@')
        logger.info('Получены данные для получения токена')
        return {
            'login': auth[0],
            'password': auth[1]
        }


def get_token(data, logger):
    if is_token(data):
        logger.info('Получен токен')
        return {'access_token': data}


def auth_handler(ctx, opt, data, logger, config):
    if data and (is_auth_data(data) or is_token(data)):
        result = get_auth(data, logger) or get_token(data, logger)
        return result
    elif not data:
        token = config.get_section('app').get('access_token').value
        if token:
            logger.info('Использован сохраненный токен.')
            result = {'access_token': token}
            return result
        else:
            logger.warning('Токен безопасности отсутствует!!!')
            if logger.level < 49:
                data = '-1'
                while data and not is_auth_data(data) and not is_token(data):
                    if data != '-1':
                        logger.warning('Введены неверные данные!!!')
                    if logger.level < 50:
                        data = click.prompt(
                            click.style(
                                'Введите токен или  логин@пароль для получения токена или оставьте пустым для отмены',
                                fg='yellow'
                            ),
                            default=False,
                            show_default=False
                        )
                if data:
                    auth_data = get_auth(data, logger)
                    access_token = get_token(data, logger)
                    return auth_data or access_token
                else:
                    logger.critical('Данные отсутствуют!!!')
                    ctx.exit(2)


    else:
        logger.critical('Введены неверные данные!!!')
        ctx.exit(2)
