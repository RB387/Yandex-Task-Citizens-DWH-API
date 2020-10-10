from aiohttp import web

from citizens_dwh_api.app_builder import AppBuilder
from citizens_dwh_api.config import get_config


def main():
    builder = AppBuilder(get_config())
    app = builder.build_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
