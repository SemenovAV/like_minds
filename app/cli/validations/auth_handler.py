import re

import click

import app.context


def is_auth_data(data):
    patern = '.+@.+'
    return re.fullmatch(patern, data)


def is_token(data):
    patern = '[0-9a-f]{85}'
    return re.fullmatch(patern, data)


def get_auth(data):
    if is_auth_data(data):
        auth = data.split('@')
        return {
            'login': auth[0],
            'password': auth[1]
        }



def get_token(data, context):
    if is_token(data):
        return {'access_token': data}


@app.context.get_context
def auth_handler(ctx, data, *args, **kwargs):
    context = kwargs.get('this_app_context')
    silent = context.silent
    config = context.config
    logger = context.logger

    if silent:
        logger.setLevel(50)
    if data and is_auth_data(data):
        logger.info('Получены данные для аунтификации')
        return get_auth(data)
    elif data and is_token(data):
        logger.info('Получен токен')
        return get_token(data,context)

    elif not data:
        token = config.get_section('app').get('access_token').value
        if token:
            logger.info('Использован сохраненный токен.')
            result = {'access_token': token}
            return result
        else:

            if logger.level < 50:
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
                if data and is_auth_data(data):
                    logger.info('Получены данные для аунтификации')
                    return get_auth(data)
                elif data and is_token(data):
                    logger.info('Получен токен')
                    return get_token(data,context)

            else:
                logger.critical('Отсутствуют токен и данные для его получения!')
                ctx.exit(2)


    else:
        logger.critical('Введены неверные данные!!!')
        ctx.exit(2)
