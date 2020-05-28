import json

import click
from AuthVK.core import Auth

import app.context
from app.searcher import searcher
from app.tools import logger, app_config
from .validations.auth_handler import auth_handler

app.context.context.update(**{
    'config': app_config,
    'logger': logger
})


@app.context.get_context
def set_silent(ctx, data, *args, **kwargs):
    context = kwargs.get('this_app_context')
    context.update(silent=data)


@app.context.get_context
def set_save_token(ctx, data, *args, **kwargs):
    context = kwargs.get('this_app_context')
    context.update(save_token=data)


@app.context.get_context
def set_save_params(ctx, data, *args, **kwargs):
    context = kwargs.get('this_app_context')
    context.update(save_params=data)


@app.context.get_context
def set_use_config_params(ctx, data, *args, **kwargs):
    context = kwargs.get('this_app_context')
    context.update(use_config_params=data)


@app.context.get_context
def reformat_params(params, *args, **kwargs):
    params_file = params.get('use_file')
    out_params_file = params.get('save_params')
    context = kwargs.get('this_app_context')
    save_token = context.save_token
    save_params = context.save_params
    access_token = None
    if 'auth' in params:
        auth = params['auth']
        if 'access_token' in auth:
            access_token = auth['access_token']
        else:
            my_auth = Auth(**auth, logger=logger)
            data = my_auth.get_auth()
            if 'access_token' in data:
                access_token = data['access_token']
    del params['auth']
    if access_token:
        if save_token:
            context.config.get_section('app').set(access_token=access_token)
        if save_params:
            context.config.get_section('app').set(**params)
        if params_file:
            file_params = json.load(params_file)
            params.update(file_params)
        if out_params_file:
            params_for_save = {
                key: value for key, value in params.items()
                if key != 'save_token' and
                   key != 'save_params' and
                   key != 'silent' and
                   key !='use_file'
            }
            json.dump(
                params_for_save,
                out_params_file,
                indent=4,
                ensure_ascii=False
            )
        params = {key: value for key, value in params.items() if value}
        return {
            'access_token': access_token,
            'params': params
        }
    else:
        raise ValueError("Неполучен access token")


silent_help = 'Тихий режим.' \
              'Предполагает наличие в конфигурационном файле токена.' \
              'В консоль не выводятся запросы недостающей информации.' \
              'В консоль не выводится информация о происходящем.' \
              'Выводятся сообшения в случае критической ошибки'
save_token = 'Сохранить используемый токен в конфигурационном файле'
save_params = 'Сохранить используемые параметры в конфиг файле'
use_file = 'Использовать json фаил с параметрами поиска. Если параметры поиска указанные при запуске' \
           'и параметры в файле совпадают, будут использованы параметры из файла.'
auth_help = 'Токен доступа к API VK или логин и пароль для автоматического ' \
            'получения токена. Логин и пароль передаются в формате: логин@пароль'
uid_help = 'ID пользователя VK, или короткое имя страницы для которого будет ' \
           'производиться поиск.' \
           '\n\n Параметры поиска: '
sex_help = 'Пол'
afrom_help = 'Возраст от'
ato_help = 'Возраст до' \
           '\n\n Различные интересы,если не один - через запятую:'
mu_help = 'Любимая музыка через запятую'
mo_help = 'Любимые фильмы через запятую'
t_help = 'Любимые тв-программы через запятую'
b_help = 'Любимые книги через запятую'
g_help = 'Любимые игры через запятую'
i_help = 'Прочие интересы'


@click.command(context_settings={'color': True})
@click.option('--silent', callback=set_silent, is_flag=True, help=silent_help)
@click.option('--save-token', callback=set_save_token, is_flag=True, help=save_token)
@click.option('--save-params', type=click.File(mode='w', encoding='utf8'), help=save_params)
@click.option('--use-file', type=click.File(mode='r', encoding='utf-8'), help=use_file)
@click.option('--auth', '-a', callback=lambda ctx, data: auth_handler(ctx, data, logger, app_config),
              help=auth_help)
@click.option('--uid', '-u', 'user_id', help=uid_help)
@click.option('--sex', '-s', type=click.Choice(['2', '1'], case_sensitive=True), help=sex_help)
@click.option('--status', '-st', type=str)
@click.option('--country', '-c', type=str)
@click.option('--city', '-ci', type=str)
@click.option('--afrom', '-f', 'age_from', type=click.IntRange(0, 130, clamp=True), help=afrom_help)
@click.option('--ato', '-t', 'age_to', type=click.IntRange(0, 130, clamp=True), help=ato_help)
@click.option('--music', '-mu', help=mu_help)
@click.option('--movies', '-mo', help=mo_help)
@click.option('--tv', help=t_help)
@click.option('--books', '-b', help=b_help)
@click.option('--games', '-g', help=g_help)
@click.option('--interests', '-i', help=i_help)
def cli(**kwargs):
    """
     Программа для поиска единомышленников в VK.
    """
    searcher(**reformat_params(kwargs))


if __name__ == '__main__':
    cli()
