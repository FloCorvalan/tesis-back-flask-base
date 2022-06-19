from dotenv import load_dotenv
from os import environ, getcwd
from apps import create_app


if __name__ == "__main__":
    pwd = getcwd()
    dotenv_path = pwd + '/.env'
    print(dotenv_path)
    load_dotenv(dotenv_path)
    print(environ)
    config_mode = environ.get('CONFIG_MODE')
    app_port = environ.get('PORT')
    app, mongo = create_app(config_mode)
    app.run(port=app_port)