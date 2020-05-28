import click
from .validations.auth_handler import auth_handler
from app.tools import logger, app_config


silent_help = 'Тихий режим.' \
              'Предполагает наличие в конфигурационном файле токена.' \
              'В консоль не выводятся запросы недостающей информации.' \
              'В консоль не выводится информация о происходящем.' \
              'Выводятся сообшения в случае критической ошибки'

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
@click.option('--silent', is_flag=True, help=silent_help)
@click.option('--db-init', is_flag=True)
@click.option('--auth', '-a', callback= lambda ctx, opt, data: auth_handler(ctx, opt, data, logger, app_config), help=auth_help)
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

    params = {key: value for key, value in kwargs.items() if value}


if __name__ == '__main__':
    cli()
