
from toolboxv2 import App, get_app

Name = 'isaa'
version = "0.0.2"
export = get_app(from_=f"{Name}.module.EXPORT").tb
test_only = export(mod_name=Name, test_only=True, version=version, state=True)


@test_only
def testing_agent(app: App):
    assert test_run_agent(app=app), "Agent Not Running Properly"


def test_run_agent(app: App = None):
    exit_app = False
    if app is None:
        exit_app = True
        app = get_app(from_="testing_isaa_run_agent", name="testing_isaa")

    isaa = app.get_mod("isaa")

    isaa.register_agents_setter(lambda x: x.
                                set_amd_model("ollama/mistral").
                                set_stream(True).
                                set_max_tokens(1200).
                                set_amd_stop_sequence(['\n\n']))
    # .set_logging_callback(lambda p: print(f"AGENT LOGGER {p}")))

    isaa.run_agent("self", "Suche Nach Information Bezüglich dem gasastreifen im web",
                   running_mode="once",
                   max_iterations=5,
                   persist_x=False,
                   fetch_memory=True,
                   persist_local=True,
                   persist_mem=False,
                   persist_mem_x=False)
    if exit_app:
        app.exit()

    return True

