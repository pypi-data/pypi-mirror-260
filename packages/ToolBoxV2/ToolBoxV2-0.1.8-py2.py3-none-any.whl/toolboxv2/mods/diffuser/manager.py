import os

from toolboxv2 import get_app, App
from .content_gen import PipelineManager

Name = "diffuser"
version = "0.0.1"
export = get_app(from_="diffuser.EXPORT").tb
no_test = export(mod_name=Name, test=False, version=version)
test_only = export(mod_name=Name, test_only=True, version=version, state=True)
to_api = export(mod_name=Name, api=True, version=version)
pipeline_manager = None


@export(mod_name=Name, initial=True, name="on_start", version=version)
def on_start(app):
    global pipeline_manager
    pipeline_manager = PipelineManager()


@export(mod_name=Name, exit_f=True, name="on_exit", version=version)
def on_exit(app):
    global pipeline_manager
    del pipeline_manager


@export(mod_name=Name, name="start_ui", version=version)
def start_ui(app: App):
    """starting the application"""
    os.system(f"streamlit run {app.start_dir}/mods/diffuser/st_runner.py")


@export(mod_name=Name, name="get_pipline_manager", version=version)
def get_pipline_manager(*args):
    return pipeline_manager
