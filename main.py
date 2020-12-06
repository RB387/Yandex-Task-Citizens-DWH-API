import uvloop

from simio.app.builder import AppBuilder
from citizens_dwh_api.config import get_config
from citizens_dwh_api.environment import HOST, PORT


def main():
    loop = uvloop.new_event_loop()

    builder = AppBuilder(config=get_config(), loop=loop)
    app = builder.build_app()
    app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
