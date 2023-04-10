"""
Чтение переменных из окружения
"""

from environs import Env

def load_config_token():
    env = Env()
    env.read_env()
    token = env('BOT_TOKEN')
    return token

def load_config_yandex_key():
    env = Env()
    env.read_env()
    key = env('YANDEX_MAP')
    return key