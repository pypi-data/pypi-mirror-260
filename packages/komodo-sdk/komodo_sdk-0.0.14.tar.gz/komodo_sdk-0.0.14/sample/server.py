from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent, websearch_agent
from komodo.loaders.appliance_loader import ApplianceLoader
from komodo.models.framework.runners import run_appliance
from komodo.server.fast import app
from komodo.server.globals import set_appliance_for_fastapi


def build() -> KomodoApp:
    app = KomodoApp(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK')
    app.add_agent(summarizer_agent())
    app.add_agent(translator_agent())
    app.add_agent(websearch_agent())
    print(app.capabilities())
    return app


def build_and_run():
    app = build()
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    response = run_appliance(app, prompt)
    print(response.text)


def load_and_run():
    app = ApplianceLoader.load('sample')
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    response = run_appliance(app, prompt)
    print(response.text)


SAMPLE_APP = app
set_appliance_for_fastapi(build())

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker
