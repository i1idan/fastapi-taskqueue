import os
from typing import get_type_hints, Union
from dotenv import load_dotenv

load_dotenv()

class CeleryConfigError(Exception):
    """Exception raised for errors in celery environment variables."""

    pass

def _parse_bool(val: Union[str, bool]) -> bool: 

    """ convert values of other data types to bool type

    Args:
        val (Union[str, bool]): input environment variable

    Returns:
        bool: actual Boolean
    """

    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']

# CeleryConfig class with required fields, default values, type checking, and typecasting for int and bool values
class CeleryConfig:
    
    DEBUG: bool = False
    # RABBITMQ
    RABBITMQ_HOST: str = 'rabbitmq'
    RABBITMQ_USERNAME: str = 'guest'
    RABBITMQ_PASSWORD: str = 'guest'
    RABBITMQ_PORT: int = 5672
    # REDIS
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_CELERY_DB_INDEX: int = 0
    REDIS_STORE_DB_INDEX: int = 0

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """
    
    def __init__(self, env):

        """ type checking, and typecasting 

        Raises:
            CeleryConfigError: if required field not supplied
            CeleryConfigError: if required type not provided
        """        
        
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise CeleryConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise CeleryConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise CeleryConfigError on failure
            try:
                var_type = get_type_hints(CeleryConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise CeleryConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )
            )

    def __repr__(self):
        return str(self.__dict__)

# Expose Config object for app to import
Config = CeleryConfig(os.environ)
