from finance.agents import FINANCE_FACTOR_MODEL_AGENTS
from komodo import KomodoApp
from komodo.framework.komodo_agent import KomodoAgent
from komodo.server.fast import app
from komodo.server.globals import set_appliance_for_fastapi


def build() -> KomodoApp:
    app = KomodoApp(shortcode='finance', name='Finance Appliance', purpose='Explain equity factor models')
    for agent in FINANCE_FACTOR_MODEL_AGENTS:
        k = KomodoAgent(**agent)
        app.add_agent(k)
    return app


WEB_APP = app
KOMODO_APP = build()
set_appliance_for_fastapi(KOMODO_APP)


def run_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker


if __name__ == '__main__':
    run_server()
