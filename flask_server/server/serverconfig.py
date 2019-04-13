import argparse
import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql+pymysql://egghunt:password@localhost:3306/multiplayerserver'

    SECRET_KEY = os.urandom(24).hex()
    JWT_KEY = os.urandom(24).hex()

    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_IMPORTS = ('server.celery_tasks.tasks')
    CELERY_TASK_RESULT_EXPIRES = 20


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_config(cmd_args=None):

    # Configures argument parser for command line arguments
    argument_parser = argparse.ArgumentParser(
        description="Runs the flask server")

    # Flag group for running server in production, debug or testing
    server_mode_group = argument_parser.add_mutually_exclusive_group()
    server_mode_group.add_argument(
        "-p", "--production", help="Run server in production", action="store_true")
    server_mode_group.add_argument(
        "-d", "--debug", help="Run server in debug mode", action="store_true")
    server_mode_group.add_argument(
        "-t", '--testing', help="Run server in testing configuration", action="store_true")

    # Argument group for setting keys from the command line
    key_group = argument_parser.add_mutually_exclusive_group()
    key_group.add_argument("-sk", "--serverkey", nargs=1,
                           help="Set server secret key")
    key_group.add_argument("-jk", "--jwtkey", nargs=1,
                           help="Set JWT secret key")
    key_group.add_argument("-k", "--keys", nargs=2,
                           help="Sets the server secret key and the jwt secret key")

    # Set database URI
    argument_parser.add_argument(
        '-db', '--database', help="Set the database uri")

    # Sets the args object
    if isinstance(cmd_args, list):
        if len(cmd_args) > 0:
            args = argument_parser.parse_args(cmd_args)
        else:
            args = None  # Debug with no flags set
    else:
        args = argument_parser.parse_args()

    # Gets env arguments
    os_debug = os.environ.get('DEBUG', default='FALSE')
    os_testing = os.environ.get('TESTING', default='FALSE')
    os_secret = os.environ.get('SECRET_KEY', default=None)
    os_jwt = os.environ.get('JWT_KEY', default=None)
    os_db = os.environ.get('DATABASE_URI', default=None)

    ServerConfig = Config

    # Setting the config based on cmd line arguments and
    # environment variable. Command line arguments take
    # precedence over environment variables
    #
    # Command flag passed
    if args is not None:
        if args.debug or args.testing or args.production:
            if args.debug:
                ServerConfig = DevelopmentConfig
            elif args.testing:
                ServerConfig = TestingConfig
    # Environment variable set
    elif os_debug == "TRUE" or os_testing == "TRUE":
        # Only one should be set
        if os_debug == "TRUE" and os_testing == "TRUE":
            raise EnvironmentError(
                "Either DEBUG or TESTING must be set to False")
        elif os_debug == "TRUE":
            ServerConfig = DevelopmentConfig
        else:

            ServerConfig = TestingConfig

    # Sets the server and JWT secret keys
    #
    # Command line args
    if args is not None:
        if args.keys or args.jwtkey or args.serverkey:
            if args.keys:
                ServerConfig.SECRET_KEY, ServerConfig.JWT_KEY = args.keys
            elif args.serverkey:
                ServerConfig.SECRET_KEY = args.serverkey[0]
            else:
                ServerConfig.JWT_KEY = args.jwtkey[0]
    # Environment args
    elif os_secret or os_jwt:
        if os_secret:
            ServerConfig.SECRET_KEY = os_secret
        if os_jwt:
            ServerConfig.JWT_KEY = os_jwt

    # Updates the database uri
    if args is not None and args.database:
        ServerConfig.DATABASE_URI = args.database[0]
    elif os_db:
        ServerConfig.DATABASE_URI = os_db

    return ServerConfig
