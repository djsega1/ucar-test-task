from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.logging import get_logging_config


class Settings(BaseSettings):
    '''
    Default configs for application.
    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    '''
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    ENV: str = Field('local')
    PATH_PREFIX: str = Field('/api/v1')
    APP_HOST: str = Field('http://127.0.0.1')
    APP_PORT: int = Field(8080)
    LOG_LEVEL: Literal['INFO', 'DEBUG', 'WARNING', 'ERROR'] = Field('INFO')

    POSTGRES_DB: str = Field('test_db')
    POSTGRES_HOST: str = Field('localhost')
    POSTGRES_USER: str = Field('user')
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_PASSWORD: str = Field('hackme')
    DB_CONNECT_RETRY: int = Field(20)
    DB_POOL_SIZE: int = Field(15)

    ENABLE_FILE_LOGGING: bool = Field(False)
    LOG_FILE: str = Field('logs/app.log')
    MAX_FILE_SIZE: int = Field(10 * 1024 * 1024)  # 10MB
    BACKUP_COUNT: int = Field(5)
    ENABLE_JSON_LOGGING: bool = Field(False)
    
    @property
    def logging_config(self) -> dict:
        '''
        Get config for convenient logging.
        '''
        return get_logging_config(
            log_level=self.LOG_LEVEL,
            enable_file_logging=self.ENABLE_FILE_LOGGING,
            log_file=self.LOG_FILE,
            max_file_size=self.MAX_FILE_SIZE,
            backup_count=self.BACKUP_COUNT,
            enable_json_logging=self.ENABLE_JSON_LOGGING,
        )

    @property
    def database_settings(self) -> dict:
        '''
        Get all settings for connection with database.
        '''
        return {
            'database': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        '''
        Get uri for connection with database.
        '''
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'.format(
            **self.database_settings,
        )
