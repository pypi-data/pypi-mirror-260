import copy
import functools
import json
import logging
import os
import platform
import shlex
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future
from dataclasses import asdict
from enum import Enum
from inspect import signature
from typing import Optional, List

import requests
import torch
from tqdm import tqdm

try:
    from duckduckgo_search import ddg, ddg_answers, ddg_news
except Exception as e:
    print("Error importing duckduckgo_search", e)
from langchain import OpenAI, HuggingFaceHub, GoogleSearchAPIWrapper
from langchain.agents import load_tools, load_huggingface_tool
from langchain.chains import ConversationalRetrievalChain
from langchain.agents.agent_toolkits import FileManagementToolkit
# Model
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import AIPluginTool
from litellm.utils import trim_messages
from pebble import concurrent
import gpt4all

from toolboxv2 import MainTool, FileHandler, get_logger, Style, Spinner, get_app
from .AgentFramwork import crate_llm_function_from_langchain_tools, ATPAS, StrictFormatResponder
from .AgentUtils import AgentChain, AIContextMemory, Scripts
from .Agents import Agent, AgentBuilder, LLMFunction, ControllerManager, stram_print
from .isaa_modi import browse_website

PIPLINE = None
Name = 'isaa'
version = "0.0.2"

pipeline_arr = [
    # 'audio-classification',
    # 'automatic-speech-recognition',
    # 'conversational',
    # 'depth-estimation',
    # 'document-question-answering',
    # 'feature-extraction',
    # 'fill-mask',
    # 'image-classification',
    # 'image-segmentation',
    # 'image-to-text',
    # 'ner',
    # 'object-detection',
    'question-answering',
    # 'sentiment-analysis',
    'summarization',
    # 'table-question-answering',
    'text-classification',
    # 'text-generation',
    # 'text2text-generation',
    # 'token-classification',
    # 'translation',
    # 'visual-question-answering',
    # 'vqa',
    # 'zero-shot-classification',
    # 'zero-shot-image-classification',
    # 'zero-shot-object-detection',
    # 'translation_en_to_de',
    # 'fill-mask'
]


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


@concurrent.process(timeout=12)
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = f"city: {response.get('city')},region: {response.get('region')},country: {response.get('country_name')},"

    return location_data


def extract_code(x):
    data = x.split('```')
    if len(data) == 3:
        text = data[1].split('\n')
        code_type = text[0]
        code = '\n'.join(text[1:])
        return code, code_type
    if len(data) > 3:
        print(x)
    return '', ''


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):

        if app is None:
            app = get_app()
        self.version = "0.0.2"
        self.name = "isaa"
        self.logger: logging.Logger or None = app.logger if app else None
        self.color = "VIOLET2"
        self.config = {'controller-init': False,
                       'agents-name-list': [],
                       }
        self.per_data = {}
        self.agent_data = {}
        self.keys = {
            "KEY": "key~~~~~~~",
            "Config": "config~~~~"
        }
        self.initstate = {}
        self.mas_text_summaries_dict = [[], []]
        extra_path = ""
        if self.toolID:
            extra_path = f"/{self.toolID}"
        self.observation_term_mem_file = f".data/{app.id}/Memory{extra_path}/observationMemory/"
        self.config['controller_file'] = f".data/{app.id}{extra_path}/controller.json"
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["api_run", "name inputs"],
                    ["add_api_key", "Adds API Key"],
                    ["imageP", "genarate image input"],
                    ["api_initIsaa", "init isaa wit dif functions", 0, 'init_isaa_wrapper'],
                    ["add_task", "Agent Chin add - Task"],
                    ["api_save_task", "Agent Chin save - Task", 0, "save_task"],
                    ["api_load_task", "Agent Chin load - Task", 1, "load_task"],
                    ["api_get_task", "Agent Chin get - Task", 0, "get_task"],
                    ["api_list_task", "Agent Chin list - Task", 0, "list_task"],
                    ["api_start_widget", "api_start_widget", 0, "start_widget"],
                    ["api_get_use", "get_use", 0, "get_use"],
                    ["generate_task", "generate_task", 0, "generate_task"],
                    ["init_cli", "init_cli", 0, "init_cli"],
                    ["chain_runner_cli", "run_chain_cli", 0, "run_chain_cli"],
                    ["remove_chain_cli", "remove_chain_cli", 0, "remove_chain_cli"],
                    ["create_task_cli", "create_task_cli", 0, "create_task_cli"],
                    ["optimise_task_cli", "optimise_task_cli", 0, "optimise_task_cli"],
                    ["run_create_task_cli", "run_create_task_cli", 0, "run_create_task_cli"],
                    ["run_describe_chains_cli", "run_describe_chains", 0, "run_describe_chains"],
                    ["run_auto_chain_cli", "run_auto_chain_cli", 0, "run_auto_chain_cli"],
                    ["save_to_mem", "save_to_mem", 0, "save_to_mem"],
                    ["set_local_files_tools", "set_local_files_tools", 0, "set_local_files_tools"],
                    ],
            "name": "isaa",
            "Version": self.show_version,
            "add_task": self.add_task,
            "save_task": self.save_task,
            "load_task": self.load_task,
            "get_task": self.get_task,
            "list_task": self.list_task,
            "save_to_mem": self.save_to_mem,
            "set_local_files_tools": self.set_local_files_tools,
        }
        self.working_directory = os.getenv('ISAA_WORKING_PATH')
        self.app = app
        self.print_stream = stram_print
        self.agent_collective_senses = False
        self.global_stream_override = False
        self.pipes_device = 1
        self.lang_chain_tools_dict = {}
        self.agent_chain = AgentChain(directory=f".data/{app.id}{extra_path}/chains")
        self.agent_memory = AIContextMemory(extra_path=extra_path)
        self.controller = ControllerManager({})
        self.summarization_mode = 0  # 0 to 3  0 huggingface 1 text 2 opnai 3 gpt
        self.summarization_limiter = 102000
        self.speak = lambda x, *args, **kwargs: x
        self.scripts = Scripts(f".data/{app.id}{extra_path}/ScriptFile")
        self.ac_task = None
        self.default_setter = None
        self.local_files_tools = True

        FileHandler.__init__(self, f"isaa{extra_path.replace('/', '-')}.config", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=None, color=self.color, on_exit=self.on_exit)

        self.toolID = ""
        MainTool.toolID = ""

    def add_task(self, name, task):
        self.agent_chain.add_task(name, task)

    def save_task(self, name=None):
        self.agent_chain.save_to_file(name)

    def load_task(self, name=None):
        self.agent_chain.load_from_file(name)

    def get_task(self, name):
        return self.agent_chain.get(name)

    def get_augment(self, task_name=None, exclude=None):
        return {
            "tools": {},
            "Agents": self.serialize_all(exclude=exclude),
            "customFunctions": json.dumps(self.scripts.scripts),
            "tasks": self.agent_chain.save_to_dict(task_name)
        }

    def init_from_augment(self, augment, agent_name: str or AgentBuilder = 'self', exclude=None):
        if isinstance(agent_name, str):
            agent = self.get_agent_class(agent_name)
        elif isinstance(agent_name, AgentBuilder):
            agent = agent_name
        else:
            return ValueError(f"Invalid Type {type(agent_name)} accept ar : str and AgentProvider")
        a_keys = augment.keys()

        if "tools" in a_keys:
            tools = augment['tools']
            print("tools:", tools)
            self.init_tools(tools, tools.get("tools.model", self.config['DEFAULTMODEL_LF_TOOLS'], agent))
            self.print("tools initialized")

        if "Agents" in a_keys:
            agents = augment['Agents']
            self.deserialize_all(agents)
            self.print("Agents crated")

        if "customFunctions" in a_keys:
            custom_functions = augment['customFunctions']
            if isinstance(custom_functions, str):
                custom_functions = json.loads(custom_functions)
            if custom_functions:
                self.scripts.scripts = custom_functions
                self.print("customFunctions saved")

        if "tasks" in a_keys:
            tasks = augment['tasks']
            if isinstance(tasks, str):
                tasks = json.loads(tasks)
            if tasks:
                self.agent_chain.load_from_dict(tasks)
                self.print("tasks chains restored")

    def init_tools(self, tools, model_name: str, agent: Optional[Agent] = None):  # not  in unit test

        plugins = [
            # SceneXplain
            # "https://scenex.jina.ai/.well-known/ai-plugin.json",
            # Weather Plugin for getting current weather information.
            #    "https://gptweather.skirano.repl.co/.well-known/ai-plugin.json",
            # Transvribe Plugin that allows you to ask any YouTube video a question.
            #    "https://www.transvribe.com/.well-known/ai-plugin.json",
            # ASCII Art Convert any text to ASCII art.
            #    "https://chatgpt-plugin-ts.transitive-bullshit.workers.dev/.well-known/ai-plugin.json",
            # DomainsGPT Check the availability of a domain and compare prices across different registrars.
            # "https://domainsg.pt/.well-known/ai-plugin.json",
            # PlugSugar Search for information from the internet
            #    "https://websearch.plugsugar.com/.well-known/ai-plugin.json",
            # FreeTV App Plugin for getting the latest news, include breaking news and local news
            #    "https://www.freetv-app.com/.well-known/ai-plugin.json",
            # Screenshot (Urlbox) Render HTML to an image or ask to see the web page of any URL or organisation.
            # "https://www.urlbox.io/.well-known/ai-plugin.json",
            # OneLook Thesaurus Plugin for searching for words by describing their meaning, sound, or spelling.
            # "https://datamuse.com/.well-known/ai-plugin.json", -> long loading time
            # Shop Search for millions of products from the world's greatest brands.
            # "https://server.shop.app/.well-known/ai-plugin.json",
            # Zapier Interact with over 5,000+ apps like Google Sheets, Gmail, HubSpot, Salesforce, and thousands more.
            "https://nla.zapier.com/.well-known/ai-plugin.json",
            # Remote Ambition Search millions of jobs near you
            # "https://remoteambition.com/.well-known/ai-plugin.json",
            # Kyuda Interact with over 1,000+ apps like Google Sheets, Gmail, HubSpot, Salesforce, and more.
            # "https://www.kyuda.io/.well-known/ai-plugin.json",
            # GitHub (unofficial) Plugin for interacting with GitHub repositories, accessing file structures, and modifying code. @albfresco for support.
            #     "https://gh-plugin.teammait.com/.well-known/ai-plugin.json",
            # getit Finds new plugins for you
            "https://api.getit.ai/.well_known/ai-plugin.json",
            # WOXO VidGPT Plugin for create video from prompt
            "https://woxo.tech/.well-known/ai-plugin.json",
            # Semgrep Plugin for Semgrep. A plugin for scanning your code with Semgrep for security, correctness, and performance issues.
            # "https://semgrep.dev/.well-known/ai-plugin.json",
        ]

        # tools = {  # Todo save tools to file and loade from usaage data format : and isaa_extras
        #    "lagChinTools": ["ShellTool", "ReadFileTool", "CopyFileTool",
        #                     "DeleteFileTool", "MoveFileTool", "ListDirectoryTool"],
        #    "huggingTools": [],
        #    "Plugins": ["https://nla.zapier.com/.well-known/ai-plugin.json"],
        #    "Custom": [],
        # }

        if agent is None:
            agent = self.get_agent_class("self")

        if 'Plugins' not in tools.keys():
            tools['Plugins'] = []
        if 'lagChinTools' not in tools.keys():
            tools['lagChinTools'] = []
        if 'huggingTools' not in tools.keys():
            tools['huggingTools'] = []

        llm_fuctions = []

        for plugin_url in set(tools['Plugins']):
            get_logger().info(Style.BLUE(f"Try opening plugin from : {plugin_url}"))
            try:
                plugin_tool = AIPluginTool.from_plugin_url(plugin_url)
                get_logger().info(Style.GREEN(f"Plugin : {plugin_tool.name} loaded successfully"))
                plugin_tool.description += "API Tool use request; infos :" + plugin_tool.api_spec + "." + str(
                    plugin_tool.args_schema)
                llm_fuctions += crate_llm_function_from_langchain_tools(plugin_tool)
                self.lang_chain_tools_dict[plugin_tool.name + "-usage-information"] = plugin_tool
            except Exception as e:
                get_logger().error(Style.RED(f"Could not load : {plugin_url}"))
                get_logger().error(Style.GREEN(f"{e}"))

        for tool in load_tools(list(set(tools['lagChinTools'])),
                               self.get_llm_models(model_name)):
            llm_fuctions += crate_llm_function_from_langchain_tools(tool)
        for tool in set(tools['huggingTools']):
            llm_fuctions += crate_llm_function_from_langchain_tools(
                load_huggingface_tool(tool, self.config['HUGGINGFACEHUB_API_TOKEN']))

        agent.functions += llm_fuctions

    def serialize_all(self, exclude=None):
        if exclude is None:
            exclude = []
        data = copy.deepcopy(self.agent_data)
        for agent_name, agent_data in data.items():
            for e in exclude:
                del agent_data[e]
            if 'amd' in agent_data.keys() and 'provider' in agent_data['amd'].keys():
                if isinstance(agent_data['amd'].get('provider'), Enum):
                    agent_data['amd']['provider'] = str(agent_data['amd'].get('provider').name).upper()
            data[agent_name] = agent_data
        return data

    def deserialize_all(self, data):
        for key, agent_data in data.items():
            _ = self.get_agent_class(key)

    def list_task(self):
        return str(self.agent_chain)

    def init_isaa(self, name='self', build=False):

        sys.setrecursionlimit(1500)

        # qu_init_t = threading.Thread(target=self.init_all_pipes_default)
        # qu_init_t.start()

        mem_init_t = threading.Thread(target=self.get_context_memory().load_all, daemon=True)
        mem_init_t.start()

        def helper():
            with Spinner(message=f"loading from files", symbols='c'):
                self.agent_chain.load_from_file()
                self.scripts.load_scripts()
                self.init_config_var_set("controller")
                print("Loading Done")
                return True

        threading.Thread(target=helper, daemon=True).start()

        if build:
            return self.get_agent_class(name)

        return self.get_default_agent_builder(name)

    def show_version(self):
        self.print("Version: ", self.version)
        return self.version

    def on_start(self):  # TODO: add flags
        self.print(f"Start {self.spec}.isaa")
        with Spinner(message=f"Starting module", symbols='c'):
            self.load_file_handler()

            self.controller.init(self.config['controller_file'])
            config = self.get_file_handler(self.keys["Config"])
            if config is not None:
                if isinstance(config, str):
                    config = json.loads(config)
                if isinstance(config, dict):
                    self.config = {**self.config, **config}

            if self.spec == 'app':
                self.load_keys_from_env()
            if not os.path.exists(f".data/{get_app().id}/Agents/"):
                os.mkdir(f".data/{get_app().id}/Agents/")
            if not os.path.exists(f".data/{get_app().id}/Memory/"):
                os.mkdir(f".data/{get_app().id}/Memory/")
            self.agent_memory.load_all()

    def load_keys_from_env(self):
        self.config['WOLFRAM_ALPHA_APPID'] = os.getenv('WOLFRAM_ALPHA_APPID')
        self.config['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
        self.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        self.config['REPLICATE_API_TOKEN'] = os.getenv('REPLICATE_API_TOKEN')
        self.config['IFTTTKey'] = os.getenv('IFTTTKey')
        self.config['SERP_API_KEY'] = os.getenv('SERP_API_KEY')
        self.config['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
        self.config['PINECONE_API_ENV'] = os.getenv('PINECONE_API_ENV')
        self.config['DEFAULTMODEL0'] = os.getenv("DEFAULTMODEL0", "ollama/llama2")
        self.config['DEFAULTMODEL1'] = os.getenv("DEFAULTMODEL1", "ollama/llama2")
        self.config['DEFAULTMODEL2'] = os.getenv("DEFAULTMODEL2", "ollama/llama2")
        self.config['DEFAULTMODELCODE'] = os.getenv("DEFAULTMODELCODE", "ollama/llama2")
        self.config['DEFAULTMODELSUMMERY'] = os.getenv("DEFAULTMODELSUMMERY", "ollama/llama2")
        self.config['DEFAULTMODEL_LF_TOOLS'] = os.getenv("DEFAULTMODEL_LF_TOOLS", "ollama/llama2")

    def webInstall(self, user_instance, construct_render) -> str:
        self.print('Installing')
        return construct_render(content="./app/0/isaa_installer/ii.html",
                                element_id="Installation",
                                externals=["/app/0/isaa_installer/ii.js"],
                                from_file=True)

    def on_exit(self):

        self.config['augment'] = self.get_augment(exclude=['amd'])
        del self.config['augment']['tasks']

        if self.config["controller-init"]:
            self.controller.save(self.config['controller_file'])
            self.init_config_var_reset("controller")

        for key in list(self.config.keys()):
            if key.startswith("LLM-model-"):
                del self.config[key]
            if key.startswith("agent-config-"):
                del self.config[key]
            if key.endswith("_pipeline"):
                del self.config[key]
            if key.endswith("-init"):
                self.config[key] = False
            if key == 'agents-name-list':
                self.config[key] = []
        self.add_to_save_file_handler(self.keys["Config"], json.dumps(self.config))
        self.save_file_handler()
        self.agent_chain.save_to_file()
        self.scripts.save_scripts()

    def init_config_var_initialise(self, key: str, value):
        key_i = key + '-init'
        if key_i not in self.config.keys():
            self.config[key_i] = False
        if not self.config[key_i]:
            self.config[key] = value
            self.config[key_i] = True

    def init_config_var_reset(self, key):
        key = key + '-init'
        self.config[key] = False

    def init_config_var_set(self, key):
        key = key + '-init'
        self.config[key] = True

    def init_all_pipes_default(self):
        pass
        # self.init_pipeline('question-answering', "deepset/roberta-base-squad2")
        # self.init_pipeline('summarization', "pinglarin/summarization_papers")
        # self.init_pipeline('text-classification', "distilbert-base-uncased-finetuned-sst-2-english")

    def init_pipeline(self, p_type, model, **kwargs):
        global PIPLINE
        if PIPLINE is None:
            from transformers import pipeline as PIPLINE
        if p_type not in self.initstate.keys():
            self.initstate[p_type + model] = False

        if not self.initstate[p_type + model]:
            self.logger.info(f"init {p_type} pipeline")
            if self.pipes_device >= 1 and torch.cuda.is_available():
                if torch.cuda.device_count() < self.pipes_device:
                    self.print("device count exceeded ava-label ar")
                    for i in range(1, torch.cuda.device_count()):
                        self.print(torch.cuda.get_device_name(i - 1))

                self.config[f"{p_type + model}_pipeline"] = PIPLINE(p_type, model=model, device=self.pipes_device - 1,
                                                                     **kwargs)
            else:
                self.logger.warning("Cuda is not available")
                self.config[f"{p_type + model}_pipeline"] = PIPLINE(p_type, model=model, **kwargs)
            self.logger.info("Done")
            self.initstate[p_type + model] = True

    def question_answering(self, question, context, model="deepset/roberta-base-squad2", **kwargs):
        self.init_pipeline('question-answering', model)
        qa = {
            'question': question,
            'context': context
        }
        return self.config[f"question-answering{model}_pipeline"](qa, **kwargs)

    def run_any_hf_pipline(self, p_type: str, model: str, init_kwargs=None, **kwargs):
        if init_kwargs is None:
            init_kwargs = {}
        self.init_pipeline(p_type, model, **init_kwargs)
        return self.config[f"{p_type}{model}_pipeline"](**kwargs)

    def summarization(self, text, model="pinglarin/summarization_papers", **kwargs):
        # if isinstance(text, str):
        #     print(f"\t\tsummarization({len(text)})")
        # if isinstance(text, list):
        #     print(f"\t\tsummarization({len(text) * len(text[0])})")
        self.init_pipeline('summarization', model)
        try:
            summary_ = self.config[f"summarization{model}_pipeline"](text, **kwargs)
        except IndexError as e:
            if isinstance(text, str):
                h = len(text) // 2
                self.logger.warning(f'Summarization text to log split in to tex len : {len(text)} splitt to {h}')
                summary_text_ = self.summarization(text[:h], **kwargs)[0]['summary_text']
                summary_ = self.summarization(text[h:], **kwargs)
                summary_[0]['summary_text'] = summary_text_ + '\n' + summary_[0]['summary_text']
            if isinstance(text, list):
                old_cap = len(text[0])
                new_cap = int(old_cap * .95)

                print(f"\tCould not generate summary old cap : {old_cap} new cap : {new_cap}")

                new_text = []
                str_text = ' '.join(text)
                num_tokens = new_cap / 2.0

                if num_tokens > 1020:
                    new_cap = int(new_cap / (num_tokens / 1020))
                    print(f"\t\t2New cap : {new_cap}")

                while len(str_text) > new_cap:
                    new_text.append(str_text[:new_cap])
                    str_text = str_text[new_cap:]
                if str_text:
                    new_text.append(str_text)
                summary_ = self.summarization(new_text, **kwargs)
            else:
                raise TypeError(f"text type invalid {type(text)} valid ar str and list")

        return summary_

    def text_classification(self, text, model="distilbert-base-uncased-finetuned-sst-2-english", **kwargs):
        self.init_pipeline('text-classification', model)
        return self.config[f"text-classification{model}_pipeline"](text, **kwargs)

    def free_llm_model(self, names: List[str]):
        for model in names:
            self.initstate[f'LLM-model-{model}-init'] = False
            del self.config[f'LLM-model-{model}']

    def load_llm_models(self, names: List[str]):
        for model in names:
            if f'LLM-model-{model}-init' not in self.initstate.keys():
                self.initstate[f'LLM-model-{model}-init'] = False

            if not self.initstate[f'LLM-model-{model}-init']:
                self.initstate[f'LLM-model-{model}-init'] = True
                if '/' in model:
                    self.config[f'LLM-model-{model}'] = HuggingFaceHub(repo_id=model,
                                                                       huggingfacehub_api_token=self.config[
                                                                           'HUGGINGFACEHUB_API_TOKEN'])
                    self.print(f'Initialized HF model : {model}')
                elif model.startswith('gpt4all#'):
                    m = gpt4all.GPT4All(model.replace('gpt4all#', ''))
                    self.config[f'LLM-model-{model}'] = m
                    self.print(f'Initialized gpt4all model : {model}')
                elif model.startswith('gpt'):
                    self.config[f'LLM-model-{model}'] = ChatOpenAI(model_name=model,
                                                                   openai_api_key=self.config['OPENAI_API_KEY'],
                                                                   streaming=True)
                    self.print(f'Initialized OpenAi model : {model}')
                else:
                    self.config[f'LLM-model-{model}'] = OpenAI(model_name=model,
                                                               openai_api_key=self.config['OPENAI_API_KEY'])
                    self.print(f'Initialized OpenAi : {model}')

    def get_llm_models(self, name: str):
        if f'LLM-model-{name}' not in self.config.keys():
            self.load_llm_models([name])
        return self.config[f'LLM-model-{name}']

    def add_lang_chain_tools_to_agent(self, agent: Agent, tools=None):

        if tools is None:
            tools = []
        for key in self.lang_chain_tools_dict.keys():
            try:
                tools += key
            except Exception as e:
                self.logger.error(Style.YELLOW(Style.Bold(f"Error in add tool : {key} {e}")))
                self.print(Style.RED(f"Tools:{key} Not available"))

        self.lang_chain_tools_dict = {}

        ll_functions = crate_llm_function_from_langchain_tools(tools)

        agent.functions += ll_functions

    def tools_to_llm_functions(self, tools: dict):
        llm_functions = []
        for tool_name, tool in tools.items():
            func = tool.get('func', None)
            if func is None:
                self.logger.warning(f'No function found for {tool_name}')
                continue

            parameters = tool.get('parameters')
            if parameters is None:
                parameters = {}

                for _1, _ in signature(func).parameters.items():
                    parameters[_1] = _.annotation.__name__
            llm_functions.append(
                LLMFunction(name=tool_name,
                            description=tool.get('description'),
                            parameters=parameters,
                            function=func)
            )
        return llm_functions

    def get_agent_builder(self, name="BP") -> AgentBuilder:
        return AgentBuilder(Agent).set_isaa_reference(self).set_amd_name(name)

    def register_agents_setter(self, setter):
        self.default_setter = setter

    def register_agent(self, agent_builder):
        if f'agent-config-{agent_builder.agent.amd.name}' in self.config:
            print(f"{agent_builder.agent.amd.name} Agent already registered")
            return

        agent_builder.save_to_json(f".data/{get_app().id}/Agents/{agent_builder.agent.amd.name}.agent")
        self.config[f'agent-config-{agent_builder.agent.amd.name}'] = agent_builder.build()
        self.config["agents-name-list"].append(agent_builder.agent.amd.name)
        self.agent_data[agent_builder.amd_attributes['name']] = agent_builder.get_dict()
        self.print(f"Agent:{agent_builder.agent.amd.name} Registered")
        return self.config[f'agent-config-{agent_builder.agent.amd.name}']

    def get_default_agent_builder(self, name="self") -> AgentBuilder:
        self.print(f"Default AgentBuilder::{name}")
        agent_builder: AgentBuilder = self.get_agent_builder(name)
        if name != "":
            if os.path.exists(f".data/{get_app().id}/Memory/{name}.agent"):
                agent_builder = agent_builder.load_from_json_file(f".data/{get_app().id}/Memory/{name}.agent", Agent)
                agent_builder.set_isaa_reference(self)

        if self.global_stream_override:
            agent_builder.set_stream(True)

        mem = self.get_context_memory()
        tools = {}

        agent_builder.set_memory(mem)  # .set_trim(Trims.isaa)

        if self.default_setter is not None:
            agent_builder = self.default_setter(agent_builder)

        if self.local_files_tools:
            if 'tools' in name:
                toolkit = FileManagementToolkit(
                    root_dir=str(self.working_directory)
                )  # If you don't provide a root_dir, operations will default to the current working directory
                for file_tool in toolkit.get_tools():
                    tools[file_tool.name] = file_tool
            elif name in ['self', 'liveInterpretation']:
                isaa_ide_online = self.app.mod_online("isaa_ide", installed=True)
                if isaa_ide_online:
                    isaa_ide = self.app.get_mod("isaa_ide")
                    isaa_ide.scope = self.working_directory
                    isaa_ide.add_tools(tools)

        agent_builder.init_agent_memory(name)

        def run_agent(agent_name: str, text: str):
            text = text.replace("'", "").replace('"', '')
            if agent_name:
                return self.run_agent(agent_name, text)
            return "Provide Information in The Action Input: fild or function call"

        def search_text(query: str):
            search = GoogleSearchAPIWrapper()
            x = query.replace("'", "").replace('"', '')
            print(Style.CYAN(x))
            responses = ddg(x)
            qa = ddg_answers(x)
            responses_yz = search.run(x)
            response = self.mas_text_summaries(responses_yz, min_length=600)

            if responses:
                for res in responses[:4]:
                    response += f"\ntitle:{res['title']}\nhref:{res['href']}\n" \
                                f"body:{self.mas_text_summaries(res['body'], min_length=600)}\n\n"

            if qa:
                for res in qa[:4]:
                    response += f"\nurl:{res['url']}\n" \
                                f"text:{self.mas_text_summaries(res['text'], min_length=600)}\n\n"

            print(response)
            if len(response) == 0:
                return "No data found"
            return response

        def search_news(query: str):

            x = query.replace("'", "").replace('"', '')
            responses = ddg_news(x, max_results=5)

            if not responses:
                return "No News"
            response = ""
            for res in responses:
                response += f"\ntitle:{res['title']}\n" \
                            f"date:{res['date']}\n" \
                            f"url:{res['url']}\n" \
                            f"source:{res['source']}\n" \
                            f"body:{self.mas_text_summaries(res['body'], min_length=1000)}\n\n"
            if len(response) == 0:
                return "No data found"
            return response

        def browse_url(text: str):

            text = text.replace("'", "").replace('"', '')
            if text.startswith("http:") or text.startswith("https:"):
                url = text.split("|")[0]
                question = text.split("|")[1:]
                res = browse_website(url, question, self.mas_text_summaries)
                return res
            return f"{text[:30]} is Not a Valid url. please just type <url>"

        def memory_search(query: str):
            ress = self.get_context_memory().get_context_for(query)

            task = f"Act as an summary expert your specialties are writing summary. you are known to think in small and " \
                   f"detailed steps to get the right result. Your task : write a summary reladet to {query}\n\n{ress}"
            res = self.run_agent('thinkm', task)

            if res:
                return res

            return ress

        def ad_data(*args):
            x = ' '.join(args)
            mem.add_data(name, x)

            return 'added to memory'

        def get_agents():
            agents_name_list = self.config['agents-name-list'].copy()
            if 'TaskCompletion' in agents_name_list:
                agents_name_list.remove('TaskCompletion')
            if 'create_task' in agents_name_list:
                agents_name_list.remove('create_task')
            if 'summary' in agents_name_list:
                agents_name_list.remove('summary')
            return agents_name_list

        if name == "self":
            # config.mode = "free"
            # config.model_name = self.config['DEFAULTMODEL0']  # "gpt-4"
            # config.max_iterations = 6
            agent_builder.set_amd_model(self.config['DEFAULTMODEL0']).set_amd_system_message(
                """
Resourceful: Isaa is able to efficiently utilize its wide range of capabilities and resources to assist the user.
Collaborative: Isaa is work seamlessly with other agents, tools, and systems to deliver the best possible solutions for the user.
Empathetic: Isaa is understand and respond to the user's needs, emotions, and preferences, providing personalized assistance.
Inquisitive: Isaa is continually seek to learn and improve its knowledge base and skills, ensuring it stays up-to-date and relevant.
Transparent: Isaa is open and honest about its capabilities, limitations, and decision-making processes, fostering trust with the user.
Versatile: Isaa is adaptable and flexible, capable of handling a wide variety of tasks and challenges.
""" + "Isaa's primary goal is to be a digital assistant designed to help the user with various " \
      "tasks and challenges by leveraging its diverse set of capabilities and resources."
            )

            tools["runAgent"] = {
                "func": lambda agent_name, instructions: self.run_agent(agent_name, instructions),
                "description": "The run_agent function takes a 2 arguments agent_name, instructions"
                               + """The function parses the input string x and extracts the values associated with the following keys:

                       agent_name: The name of the agent to be run.
                       instructions: The task that the agent is to perform. (do not enter the name of a task_chain!) give clear Instructions

                   The function then runs the Agent with the specified name and Instructions."""}

            tools["getAvalabelAgents"] = {
                "func": get_agents,
                "description": "Use to get list of all agents avalabel"}

            tools["saveDataToMemory"] = {"func": ad_data, "description": "tool to save data to memory,"
                                                                         " write the data as specific"
                                                                         " and accurate as possible."}

            tools = {**tools, **{
                "memorySearch": {"func": lambda x: memory_search(x),
                                 "description": "Serch for simmilar memory imput <context>"},
                "searchWeb": {"func": lambda x: run_agent('search', x),
                              "description": "Run agent to search the web for information's"
                    , "format": "search(<task>)"},
                # "write-production-redy-code": {"func": lambda x: run_agent('think',
                #                                                            f"Act as a Programming expert your specialties are coding."
                #                                                            f" you are known to think in small and detailed steps to get"
                #                                                            f" the right result.\n\nInformation's:"
                #                                                            f" {config.edit_text.text}\n\n Your task : {x}\n\n"
                #                                                            f"write an production redy code"),
                #                                "description": "Run agent to generate code."
                #     , "format": "write-production-redy-code(<task>)"},

                "think": {"func": lambda x: run_agent('thinkm', x),
                          "description": "Run agent to solve a text based problem"
                    , "format": "programming(<task>)"},
                "shell": {"func": shell_tool_fuction,
                          "description": "Run shell command"
                    , "format": "shell_tool_fuction(<command>)"},
                "miniTask": {"func": lambda x: self.mini_task_completion(x),
                             "description": "programmable pattern completion engin. use text davici args:str only"
                    , "format": "reminder(<detaild_discription>)"},

            }}

        if "tools" in name:
            tools = {}
            for key, _tool in self.lang_chain_tools_dict.items():
                tools[key] = {"func": _tool, "description": _tool.description, "format": f"{key}({_tool.args})"}
            agent_builder.set_amd_model(self.config['DEFAULTMODEL0'])

        if name == "search":
            # config.mode = "tools"
            # config.model_name = self.config['DEFAULTMODEL1']
            # config.completion_mode = "chat"
            # config.set_agent_type("structured-chat-zero-shot-react-description")
            # config.max_iterations = 6
            # config.verbose = True
            agent_builder.set_amd_model(self.config['DEFAULTMODEL0']).set_verbose(True).set_amd_system_message(
                """
            Resourceful: The Search Agent should be adept at finding relevant and reliable information from various sources on the web.
            Analytical: The Search Agent should be skilled at analyzing the retrieved information and identifying key points and themes.
            Efficient: The Search Agent should be able to quickly search for and summarize information, providing users with accurate and concise results.
            Adaptive: The Search Agent should be able to adjust its search and summarization strategies based on the user's query and the available information.
            Detail-Oriented: The Search Agent should pay close attention to the details of the information it finds, ensuring accuracy and relevance in its summaries."""

                + """
            1. Information Retrieval: The primary goal of the Search Agent is to find relevant and reliable information on the web in response to user queries.
            2. Text Summarization: The Search Agent should be able to condense the retrieved information into clear and concise summaries, capturing the most important points and ideas.
            3. Relevance Identification: The Search Agent should be able to assess the relevance of the information it finds, ensuring that it meets the user's needs and expectations.
            4. Source Evaluation: The Search Agent should evaluate the credibility and reliability of its sources, providing users with trustworthy information.
            5. Continuous Improvement: The Search Agent should continuously refine its search algorithms and summarization techniques to improve the quality and relevance of its results over time."""
            )
            agent_builder.set_content_memory_max_length(3500)
            tools = {
                "memorySearch": {"func": lambda x: memory_search(x),
                                 "description": "Search for memory  <context>"},
                "browse": {"func": lambda x: browse_url(x),
                           "description": "browse web page via URL syntax <url>"},
                "searchWeb": {"func": lambda x: search_text(x),
                              "description": "Use Duck Duck go to search the web systax <key word>"},
                # "search_news": {"func": lambda x: search_news(x),
                #                 "description": "Use Duck Duck go to search the web for new get time"
                #                                "related data systax <key word>"}
                # "chain_search_web": {"func": lambda x: run_agent('chain_search_web', x),
                #                     "description": "Run chain agent to search in the web for informations, Only use for complex mutistep tasks"
                #    , "chain_search_web": "search(<task>)"},
                # "chain_search_url": {"func": lambda x: run_agent('chain_search_url', x),
                #                     "description": "Run chain agent to search by url for informations provide mutibel urls, Only use for complex mutistep tasks"
                #    , "format": "chain_search_url(<task,url1,url...>)"},
                # "chain_search_memory": {"func": lambda x: run_agent('chain_search_memory', x),
                #                        "description": "Run chain agent to search in the memory for informations, Only use for complex mutistep tasks"
                #    , "format": "chain_search_memory(<task>)"},
            }

            tools["saveDataToMemory"] = {"func": ad_data, "description": "tool to save data to memory,"
                                                                         " write the data as specific"
                                                                         " and accurate as possible."}

            agent_builder.set_tasklist(["Erfülle die Aufgae in so wenigen Schritten und so Bedacht wie Möglich"])
            agent_builder.set_capabilities(ATPAS)

        if name == "think":
            agent_builder.set_amd_model(self.config['DEFAULTMODEL0'])
            # .stop_sequence = ["\n\n\n"]

        if "shell" in name:
            (agent_builder.set_amd_model(self.config['DEFAULTMODEL0'])
             .set_amd_system_message("Act as an Command Shell Agent. You can run shell commandants by writing "
                                     "\nFUCTION: {'Action','shell','Input':[shell_command]}"))
            tools["shell"] = {"func": shell_tool_fuction,
                              "description": "Run shell command"
                , "parameters": {"type": "string"}}
            pass
            # .set_model_name(self.config['DEFAULTMODEL1'])
            # .add_system_information = False
            # .stop_sequence = ["\n"]

        if name == "liveInterpretation":
            pass
            # .set_model_name(self.config['DEFAULTMODEL0']).stream = True
            # config.stop_sequence = ["!X!"]

        if name == "summary":
            agent_builder.set_amd_model(self.config['DEFAULTMODELSUMMERY'])

        if name == "thinkm":
            agent_builder.set_amd_model(self.config['DEFAULTMODEL1'])

        if name == "TaskCompletion":
            agent_builder.set_amd_model(self.config['DEFAULTMODEL1'])

        if name == "code":
            agent_builder.set_amd_model(self.config['DEFAULTMODELCODE'])
        llm_functions = self.tools_to_llm_functions(tools)
        agent_builder.set_functions(llm_functions)
        agent_builder_dict = agent_builder.save_to_json(f".data/{get_app().id}/Agents/{name}.agent")
        self.agent_data[agent_builder.amd_attributes['name']] = agent_builder_dict
        return agent_builder

    def remove_agent_config(self, name):
        del self.config[f'agent-config-{name}']
        self.config["agents-name-list"].remove(name)

    def get_agent_class(self, agent_name="Normal") -> Agent:

        if "agents-name-list" not in self.config.keys():
            self.config["agents-name-list"] = []

        # self.config["agents-name-list"] = [k.replace('agent-config-', '') for k in self.config.keys() if k.startswith('agent-config-')])
        if f'agent-config-{agent_name}' in self.config.keys():
            agent = self.config[f'agent-config-{agent_name}']
            self.print(f"collecting AGENT: {agent_name} "
                       f"{'Mode:' + str(agent.mode) if agent.mode is not None else ''} "
                       f"{'Cape:' + agent.capabilities.name if agent.capabilities is not None else ''}")
        else:
            agent_builder = self.get_default_agent_builder(agent_name)
            agent = agent_builder.build()
            del agent_builder
            self.config[f'agent-config-{agent_name}'] = agent
            self.print(f"Init:Agent::{agent_name}:{agent.amd.name} {str(agent.mode)}")
        if agent_name in self.config["agents-name-list"]:
            self.config["agents-name-list"].append(agent_name)
        return agent

    def mini_task_completion(self, mini_task, mode=None, fetch_memory=False, all_mem=False):
        agent: Agent = self.get_agent_class("TaskCompletion")
        agent.mode = mode
        if isinstance(mini_task, str):
            llm_message = agent.get_llm_message(mini_task, persist=False, fetch_memory=fetch_memory, all_meme=all_mem,
                                                isaa=self)
            res = agent.run_model(llm_message=llm_message, persist_local=False)
        elif isinstance(mini_task, list):
            llm_messages = agent.get_batch_llm_messages(mini_task, fetch_memory=fetch_memory, all_meme=all_mem,
                                                        isaa=self)
            res = agent.run_model(llm_message=llm_messages, persist_local=False, batch=True)
        else:
            raise TypeError(f"Unable to complete mini_task of type {type(mini_task)}")
        agent.mode = None
        return res

    def mini_task_completion_format(self, mini_task, format_, max_tokens=None, agent_name="TaskCompletion",
                                    fetch_memory=False, all_meme=False):
        agent: Agent = self.get_agent_class(agent_name)
        agent.mode = self.controller.rget(StrictFormatResponder)
        if isinstance(mini_task, str):
            llm_message = agent.get_llm_message(mini_task, persist=False, fetch_memory=fetch_memory, all_meme=all_meme,
                                                isaa=self)
            llm_message.append({'content': format_, 'role': 'system'})
            res = agent.run_model(llm_message=llm_message, persist_local=False, max_tokens=max_tokens)
        elif isinstance(mini_task, list):
            llm_messages = agent.get_batch_llm_messages(mini_task, fetch_memory=fetch_memory, all_meme=all_meme,
                                                        isaa=self)
            [m.append({'content': format_, 'role': 'system'}) for m in llm_messages]
            res = agent.run_model(llm_message=llm_messages, persist_local=False, batch=True, max_tokens=max_tokens)
        else:
            raise TypeError(f"Unable to complete mini_task of type {type(mini_task)}")
        agent.mode = None
        return res

    def short_prompt_messages(self, messages, get_tokens, max_tokens, prompt_token_margin=200, max_iteration=5):

        # Step 2: Handle prompt length
        prompt_len = get_tokens(messages)
        prompt_len_new = prompt_len
        if prompt_len > max_tokens - prompt_token_margin:
            factor = prompt_len // max_tokens
            self.print(f"Context length exceeded by {factor:.2f}X {(prompt_len, max_tokens)}")
            iteration = 0
            while max_tokens - prompt_len < 50 and iteration <= min(max_iteration, factor):
                logging.debug(f'Tokens: {prompt_len}')
                logging.info(f'Prompt is too long. Auto shortening token overflow by {(max_tokens - prompt_len) * -1}')

                if iteration > 0:
                    temp_message = []
                    for msg in messages:
                        temp_message.append({'role': msg['role'], 'content': dilate_string(msg['content'], 1, 2, 0)})
                    logging.info(f"Temp message: {temp_message}")
                    messages = temp_message

                if iteration > 1:
                    temp_message = []
                    for msg in messages:
                        temp_message.append({'role': msg['role'], 'content': dilate_string(msg['content'], 0, 2, 0)})
                    logging.info(f"Temp message: {temp_message}")
                    messages = temp_message

                if iteration > 2:
                    temp_message = []
                    mas_text_sum = self.mas_text_summaries
                    for msg in messages:
                        temp_message.append({'role': msg['role'], 'content': mas_text_sum(msg['content'])})
                    logging.info(f"Temp message: {temp_message}")
                    messages = temp_message

                if iteration > 3:
                    temp_message = []
                    mini_task_com = self.mini_task_completion
                    for msg in messages:
                        important_info = mini_task_com(
                            f"Was ist die wichtigste Information in {msg['content']}")
                        temp_message.append({'role': msg['role'], 'content': important_info})
                    logging.info(f"Temp message: {temp_message}")
                    messages = temp_message

                if iteration > 4:
                    messages = trim_messages(messages, max_tokens=max_tokens, trim_ratio=0.75 - (iteration - 4) * 0.25)

                prompt_len_new = get_tokens(messages, only_len=True)
                iteration += 1

                if iteration > 9:
                    break

            self.print(f"Prompt scale down by {prompt_len / prompt_len_new:.2f}X {(prompt_len_new, max_tokens)}")

        return messages

    def run_agent(self, name: str or Agent, text: str,
                  max_iterations=3, running_mode: str = "once",
                  persist=False,
                  persist_x=True,
                  fetch_memory=True,
                  persist_mem=True,
                  persist_mem_x=True, task_from="user", all_mem=False):

        agent = None
        if isinstance(name, str):
            # self.load_keys_from_env()
            agent = self.get_agent_class(name)

        elif isinstance(name, Agent):
            agent = name
            name = agent.amd.name

            if name not in self.config["agents-name-list"]:
                self.config[f'agent-config-{name}'] = agent
                self.print(f"Register:Agent::{name}:{agent.amd.name} {str(agent.mode)}\n")

        else:
            raise ValueError(f"Invalid arguments agent is not str or Agent {type(agent)}")

        self.print(f"Running agent {name}")

        out = "Invalid configuration\n"
        stream = agent.stream
        self.logger.info(f"stream: {stream}")

        if agent.mode is not None and not self.controller.registered(agent.mode.name):
            self.controller.add(agent.mode.name, agent.mode)

        if running_mode.endswith("Is") and agent.capabilities is None:
            agent.capabilities = ATPAS
            print(f"Agent {agent.amd.name} addet capabilities ATPAS {ATPAS.description}")

        if running_mode == "once":

            with Spinner(message="Fetching llm_message...", symbols='+'):
                llm_message = agent.get_llm_message(text, persist=persist, fetch_memory=fetch_memory, isaa=self,
                                                    task_from=task_from, all_meme=all_mem)
            out = agent.run_model(llm_message=llm_message, persist_local=persist, persist_mem=persist_mem)
        elif running_mode == "oncex":

            with Spinner(message="Fetching llm_message...", symbols='+'):
                llm_message = agent.get_llm_message(text, persist=persist, fetch_memory=fetch_memory, isaa=self,
                                                    task_from=task_from, all_meme=all_mem)
            out = agent.run_model(llm_message=llm_message, persist_local=persist, persist_mem=persist_mem)
            if agent.if_for_fuction_use(out):
                out += "Eval :" + agent.execute_fuction(persist=persist_x, persist_mem=persist_mem_x)
        elif running_mode == "lineIs":

            if agent.tasklist is None:
                agent.tasklist = []
            if agent.task_index is None:
                agent.task_index = 0

            class miniHelperVarStor:
                """Shaid AF"""
                onLiveMode = ""
                action_called = False
                task_list = []
                task_index = 0
                line = ""

            mhvs = miniHelperVarStor()

            def olivemode(line: str):
                modes = ["FUCTION:", "ASK:", "SPEAK:", "THINK:", "PLAN:"]
                if not line:
                    mhvs.onLiveMode = ""
                    return False
                for mode in modes:
                    if mode in line.upper() or line.startswith('{'):
                        mhvs.onLiveMode = mode
                        return mode
                if mhvs.onLiveMode:
                    return mhvs.onLiveMode
                return False

            def online(line):

                mhvs.line += line
                test_line = ""

                if '\n' in mhvs.line:
                    test_line = mhvs.line.split('\n')[0]
                    mhvs.line = mhvs.line.split('\n')[-1]
                self.print_stream(test_line)

                mode = olivemode(test_line)
                if not mode:
                    return False

                # self.print("Mode: " + mode)

                if mode == "FUCTION:":

                    self.logger.info(f"analysing test_task_done")

                    if agent.if_for_fuction_use(test_line):
                        mhvs.action_called = True
                        self.print(f"Using-tools: {agent.next_fuction}")
                        ob = agent.execute_fuction(persist=persist_x, persist_mem=persist_mem_x)
                        # config.observe_mem.text = ob

                        self.print(f"Observation: {ob}")
                        mhvs.onLiveMode = ""
                        agent.task_index += 1
                    else:
                        self.print(f"Isaa called a invalid Tool")
                    if agent.task_index > len(agent.tasklist):  # new task
                        self.print(f"Task done")
                        # self.speek("Ist die Aufgabe abgeschlossen?")
                        if agent.content_memory.tokens > 50:
                            agent.content_memory.clear_to_collective()
                        mhvs.onLiveMode = ""
                        mhvs.action_called = False
                    return True

                if mode == "PLAN:":
                    agent.tasklist.append(line)
                    return False

                if mode == "SPEAK:":
                    self.speak(line.replace("SPEAK:", ""))
                    mhvs.onLiveMode = ""
                    return False

                if mode == "ASK:":
                    self.speak(line.replace("ASK:", ""))
                    self.print(line)
                    agent.messages.append({"role": "user", "content": input("\n========== Isaa has a question ======= "
                                                                            "\n:")})
                    mhvs.onLiveMode = ""
                    mhvs.action_called = True
                    return True

                return False

            last_call = False

            agent.stram_registrator(online)

            for turn in range(max_iterations):

                print()
                self.print(f"=================== Enter Turn : {turn} of {max_iterations} =================\n")
                # if turn > config.max_iterations//2:
                #     if input("ENTER Something to stop the agent: or press enter to prosed"):
                #         break

                with Spinner(message="Fetching llm_message...", symbols='+'):
                    llm_message = agent.get_llm_message(text, persist=persist, fetch_memory=fetch_memory, isaa=self,
                                                        task_from=task_from, all_meme=all_mem)
                out = agent.run_model(llm_message=llm_message, persist_local=persist, persist_mem=persist_mem)
                if agent.stream and "\n" not in out and mhvs.onLiveMode == "" and not mhvs.action_called:
                    online(out)
                else:
                    online(out)
                if not stream:
                    self.print_stream(out)

                if len(agent.tasklist) == 0:
                    self.print("execution-break no mor tasks :")
                    break

                if agent.task_index > len(agent.tasklist):
                    self.print("execution-break tasks index overflow:")
                    break

                self.print(
                    f"=================== Prep message for task index {agent.task_index}\n===================== ### =================\n")
                next_task = text
                if agent.task_index < len(agent.tasklist):
                    self.print(f"Next task: {agent.tasklist[agent.task_index]}")
                    next_task = agent.tasklist[agent.task_index]

                if "The task has been completed.".lower() in out:
                    self.print("execution-break 'The task has been completed.' found in response")
                    break

                if "task" in out and "been" in out and "completed" in out and turn > max_iterations // 2:
                    self.print(f"execution-break iteration {turn} 3 keyword found")
                    break

                if not out:
                    self.print(f"execution-break no output")
                    break

                if out.endswith("EVAL") and max_iterations:
                    continue
                if mhvs.action_called and max_iterations:
                    continue
                else:
                    if last_call:
                        break
                    agent.tasklist.append("This is the last Call Report to the user!")
                    last_call = True
        else:
            raise ValueError(f"invalid running mode {running_mode}")

        return out

    def mas_text_summaries(self, text, min_length=1600):

        len_text = len(text)
        if len_text < min_length:
            return text

        if text in self.mas_text_summaries_dict[0]:
            self.print("summ return vom chash")
            return self.mas_text_summaries_dict[1][self.mas_text_summaries_dict[0].index(text)]

        cap = 800
        max_length = 45
        summary_chucks = ""

        # 4X the input
        if len(text) > min_length * 20:
            text = dilate_string(text, 2, 2, 0)
        if len(text) > min_length * 10:
            text = dilate_string(text, 0, 2, 0)

        if 'text-splitter0-init' not in self.config.keys():
            self.config['text-splitter0-init'] = False
        if not self.config['text-splitter0-init'] or not isinstance(self.config['text-splitter0-init'],
                                                                    CharacterTextSplitter):
            self.config['text-splitter0-init'] = CharacterTextSplitter(chunk_size=cap, chunk_overlap=cap / 6)

        splitter = self.config['text-splitter0-init']

        if len(text) >= 6200:
            cap = 1200
            max_length = 80
            if 'text-splitter1-init' not in self.config.keys():
                self.config['text-splitter1-init'] = False
            if not self.config['text-splitter1-init'] or not isinstance(self.config['text-splitter1-init'],
                                                                        CharacterTextSplitter):
                self.config['text-splitter1-init'] = CharacterTextSplitter(chunk_size=cap, chunk_overlap=cap / 6)

            splitter = self.config['text-splitter1-init']

        if len(text) >= 10200:
            cap = 1800
            max_length = 160
            if 'text-splitter2-init' not in self.config.keys():
                self.config['text-splitter2-init'] = False
            if not self.config['text-splitter2-init'] or not isinstance(self.config['text-splitter2-init'],
                                                                        CharacterTextSplitter):
                self.config['text-splitter2-init'] = CharacterTextSplitter(chunk_size=cap, chunk_overlap=cap / 6)

            splitter = self.config['text-splitter2-init']

        if len(text) >= 70200:
            cap = 1900
            max_length = 412
            if 'text-splitter3-init' not in self.config.keys():
                self.config['text-splitter3-init'] = False
            if not self.config['text-splitter3-init'] or not isinstance(self.config['text-splitter3-init'],
                                                                        CharacterTextSplitter):
                self.config['text-splitter3-init'] = CharacterTextSplitter(chunk_size=cap, chunk_overlap=cap / 6)

            splitter = self.config['text-splitter3-init']

        summarization_mode_sto = 0
        if len(text) > self.summarization_limiter and self.summarization_mode:
            self.summarization_mode, summarization_mode_sto = 0, self.summarization_mode

        def summary_func(x):
            return self.summarization(x, max_length=max_length)

        def summary_func2(x, agent_name='summary', mode=None):
            if isinstance(agent_name, str):
                agent = self.get_agent_class(agent_name)
            if isinstance(agent_name, Agent):
                agent = agent_name
            temp_mode = None
            temp_stream = agent.stream
            agent.stream = False
            if mode is not None:
                temp_mode = agent.mode
                agent.mode = temp_mode
            if isinstance(x, list):
                end = []
                for i in x:
                    text_sum = agent.get_llm_message(i + "\nSummary :" if mode is None else '', persist=False,
                                                     fetch_memory='think' == agent_name, isaa=self)
                    text_sum = agent.run_model(text_sum, persist_local=False, persist_mem=False)
                    end.append({'summary_text': text_sum})
            elif isinstance(x, str):
                text_sum = agent.get_llm_message(x + "\nSummary :" if mode is None else '', persist=False,
                                                 fetch_memory='think' == agent_name, isaa=self)
                text_sum = agent.run_model(text_sum, persist_local=False, persist_mem=False)
                end = [{'summary_text': text_sum}]
            else:
                if temp_mode is not None:
                    agent.mode = temp_mode
                agent.stream = temp_stream
                raise TypeError(f"Error invalid type {type(x)}")
            if temp_mode is not None:
                agent.mode = temp_mode
            agent.stream = temp_stream
            return end

        chunks: List[str] = splitter.split_text(text)
        i = 0
        max_iter = int(len(chunks) * 1.2)
        while i < len(chunks) and max_iter > 0:
            max_iter -= 1
            chunk = chunks[i]
            if len(chunk) > cap * 1.5:
                chunks = chunks[:i] + [chunk[:len(chunk) // 2], chunk[len(chunk) // 2:]] + chunks[i + 1:]
            else:
                i += 1

        self.print(f"SYSTEM: chucks to summary: {len(chunks)} cap : {cap}")
        with tqdm(total=len(chunks), unit='chunk', desc='Generating summary') as pbar:
            if self.summarization_mode == 0:
                summaries = summary_func(chunks)
            else:
                mode = None
                if self.summarization_mode == 1:
                    agent_name = 'summary'
                elif self.summarization_mode == 2:
                    agent_name = 'thinkm'
                elif self.summarization_mode == 3:
                    agent_name = 'think'
                agent_ = self.get_agent_class(agent_name)
                fuction = functools.partial(summary_func2, agent_name=agent_, mode=mode)
                summaries = []
                with ThreadPoolExecutor(max_workers=6) as executor:
                    # Load modules in parallel using threads
                    futures: set[Future] = {executor.submit(fuction, chunk) for chunk in chunks}

                    for futures_ in futures:
                        result = futures_.result()
                        pbar.update(1)
                        summaries.append(result)
                print(summaries)

        for chuck_summary in summaries:
            if isinstance(chuck_summary, dict):
                summary_chucks += chuck_summary['summary_text'] + "\n"
            elif isinstance(chuck_summary, list):
                print(chuck_summary)
                chuck_summary = chuck_summary[0]
                if isinstance(chuck_summary, str):
                    summary_chucks += chuck_summary + "'\n"
                elif isinstance(chuck_summary, dict):
                    summary_chucks += chuck_summary['summary_text'] + "\n"
                else:
                    raise ValueError(f"Unknown type of chunk {type(chuck_summary)}")
            else:
                raise ValueError(f"Unknown type of chunk {type(chuck_summary)}")

        self.print(f"SYSTEM: all summary_chucks : {len(summary_chucks)}")

        if len(summaries) > 8:
            if len(summary_chucks) < 20000:
                summary = summary_chucks
            elif len(summary_chucks) > 20000:
                summary = summary_func2(summary_chucks)[0]['summary_text']
            else:
                summary = self.mas_text_summaries(summary_chucks)
        else:
            summary = summary_chucks

        self.print(
            f"SYSTEM: final summary from {len_text}:{len(summaries)} ->"
            f" {len(summary)} compressed {len_text / len(summary):.2f}X\n")

        if summarization_mode_sto:
            self.summarization_mode = summarization_mode_sto

        self.mas_text_summaries_dict[0].append(text)
        self.mas_text_summaries_dict[1].append(summary)

        return summary

    def summarize_ret_list(self, ret_list):
        chucs = []
        print("ret_list:", ret_list)
        for i, step in enumerate(ret_list):
            print("i, step:", i, step)
            if isinstance(step, list):
                step_content = ""
                if len(step) == 2:
                    if isinstance(step[1], str):
                        step_content += f"\nlog {i}  input : {str(step[0])} output :  {str(step[1])}"
                    if isinstance(step[1], list):
                        step_content += f"\nlog {i}  input : {str(step[0][0])} output :  {str(step[0][1])}"
                    if isinstance(step[1], dict):
                        if 'input' in step[1].keys():
                            step_content += f"\ninput {i} " + str(step[1]['input'])
                        if 'output' in step[1].keys():
                            step_content += f"\noutput {i} " + str(step[1]['output'])
                if len(step) > 1600:
                    step_content = self.mas_text_summaries(step_content)
                chucs.append(step_content)
        text = 'NoContent'
        if chucs:
            text = '\n'.join(chucs)
        return text

    def init_db_questions(self, db_name, base_llm_name):
        retriever = self.get_context_memory().get_retriever(db_name)
        if retriever is not None:
            retriever.search_kwargs['distance_metric'] = 'cos'
            retriever.search_kwargs['fetch_k'] = 20
            retriever.search_kwargs['maximal_marginal_relevance'] = True
            retriever.search_kwargs['k'] = 20
            return ConversationalRetrievalChain.from_llm(self.get_llm_models(base_llm_name), retriever=retriever)
        return None

    def get_chain(self, hydrate=None, f_hydrate=None) -> AgentChain:
        logger = get_logger()
        logger.info(Style.GREYBG(f"AgentChain requested"))
        agent_chain = self.agent_chain
        if hydrate is not None or f_hydrate is not None:
            self.agent_chain.add_hydrate(hydrate, f_hydrate)
        logger.info(Style.Bold(f"AgentChain instance, returned"))
        return agent_chain

    def get_context_memory(self) -> AIContextMemory:
        logger = get_logger()
        logger.info(Style.GREYBG(f"AIContextMemory requested"))
        cm = self.agent_memory
        logger.info(Style.Bold(f"AIContextMemory instance, returned"))
        return cm

    def save_to_mem(self):
        for name in self.config['agents-name-list']:
            self.get_agent_class(agent_name=name).save_memory()

    def set_local_files_tools(self, local_files_tools):
        try:
            self.local_files_tools = bool(local_files_tools)
        except ValueError as e:
            return f"Invalid boolean value True or False not {local_files_tools} \n{str(e)}"
        return f"set to {self.local_files_tools=}"


def dilate_string(text, split_param, remove_every_x, start_index):
    substrings = ""
    # Split the string based on the split parameter
    if split_param == 0:
        substrings = text.split(" ")
    elif split_param == 1:
        substrings = text.split("\n")
    elif split_param == 2:
        substrings = text.split(". ")
    elif split_param == 3:
        substrings = text.split("\n\n")
    # Remove every x item starting from the start index
    del substrings[start_index::remove_every_x]
    # Join the remaining substrings back together
    final_string = " ".join(substrings)
    return final_string


def shell_tool_fuction(command: str) -> str:
    """
    Runs a command in the user's shell.
    It is aware of the current user's $SHELL.
    :param command: A shell command to run.
    :return: A JSON string with information about the command execution.
    """
    if platform.system() == "Windows":
        is_powershell = len(os.getenv("PSModulePath", "").split(os.pathsep)) >= 3
        full_command = (
            f'powershell.exe -Command "{command}"'
            if is_powershell
            else f'cmd.exe /c "{command}"'
        )
    else:
        shell = os.environ.get("SHELL", "/bin/sh")
        full_command = f"{shell} -c {shlex.quote(command)}"

    try:
        output = subprocess.check_output(full_command, shell=True, stderr=subprocess.STDOUT)
        return json.dumps({"success": True, "output": output.decode()})
    except subprocess.CalledProcessError as e:
        return json.dumps({"success": False, "error": str(e), "output": e.output.decode()})


"""

    def execute_thought_chain(self, user_text: str, agent_tasks, config: Agent, speak=lambda x: x, start=0,
                              end=None, chain_ret=None, chain_data=None, uesd_mem=None, chain_data_infos=False):
        if uesd_mem is None:
            uesd_mem = {}
        if chain_data is None:
            chain_data = {}
        if chain_ret is None:
            chain_ret = []
        if end is None:
            end = len(agent_tasks) + 1
        ret = ""

        default_mode_ = config.mode
        default_completion_mode_ = config.completion_mode
        config.completion_mode = "chat"
        config.get_messages(create=False)
        sto_name = config.name
        sto_config = None
        chain_mem = self.get_context_memory()
        self.logger.info(Style.GREY(f"Starting Chain {agent_tasks}"))
        config.stop_sequence = ['\n\n\n', "Execute:", "Observation:", "User:"]

        invalid = False
        error = ""
        if not isinstance(agent_tasks, list):
            self.print(Style.RED(f"tasks must be list ist: {type(agent_tasks)}:{agent_tasks}"))
            error = "tasks must be a list"
            invalid = True
        if len(agent_tasks) == 0:
            self.print(Style.RED("no tasks specified"))
            error = "no tasks specified"
            invalid = True

        if invalid:
            if chain_data_infos:
                return chain_ret, chain_data, uesd_mem
            else:
                return error, chain_ret

        work_pointer = start
        running = True
        while running:

            task = agent_tasks[work_pointer]

            self.logger.info(Style.GREY(f"{type(task)}, {task}"))
            chain_ret_ = []
            config.mode = "free"
            config.completion_mode = "chat"

            sum_sto = ""

            keys = list(task.keys())

            task_name = task["name"]
            use = task["use"]
            if isinstance(task["args"], str):
                args = task["args"].replace("$user-input", str(user_text))
            if isinstance(task["args"], dict) and use == "agent":
                args = task["args"]
                args["$user-input"] = user_text

            if use == 'agent':
                sto_config, config = config, self.get_agent_config_class(task_name)
            else:
                config = self.get_agent_config_class('self')

            default_mode = config.mode
            default_completion_mode = config.completion_mode

            if 'mode' in keys:
                config.mode = task['mode']
                self.logger.info(Style.GREY(f"In Task {work_pointer} detected 'mode' {config.mode}"))
            if 'completion-mode' in keys:
                config.completion_mode = task['completion-mode']
                self.logger.info(
                    Style.GREY(f"In Task {work_pointer} detected 'completion-mode' {config.completion_mode}"))
            if "infos" in keys:
                config.short_mem.text += task['infos']
                self.logger.info(Style.GREY(f"In Task {work_pointer} detected 'info' {task['infos'][:15]}..."))

            chain_data['$edit-text-mem'] = config.edit_text.text

            for c_key in chain_data.keys():
                if c_key in args:
                    args = args.replace(c_key, str(chain_data[c_key]))

            if use == 'chain':
                for c_key in chain_data.keys():
                    if c_key in task_name:
                        task_name = task_name.replace(c_key, str(chain_data[c_key]))

            self.print(f"Running task:\n {args}\n_______________________________\n")

            speak(f"Chain running {task_name} at step {work_pointer} with the input : {args}")

            if 'chuck-run-all' in keys:
                self.logger.info(Style.GREY(f"In Task {work_pointer} detected 'chuck-run-all'"))
                chunk_num = -1
                for chunk in chain_data[task['chuck-run-all']]:
                    chunk_num += 1
                    self.logger.info(Style.GREY(f"In chunk {chunk_num}"))
                    if not chunk:
                        self.logger.warning(Style.YELLOW(f"In chunk {chunk_num} no detected 'chunk' detected"))
                        continue

                    self.logger.info(Style.GREY(f"detected 'chunk' {str(chunk)[:15]}..."))

                    args_ = args.replace(task['chuck-run-all'], str(chunk))

                    ret, sum_sto, chain_ret_ = self.chain_cor_runner(use, task_name, args_, config, sto_name, task,
                                                                     work_pointer, keys,
                                                                     chain_ret, sum_sto)

            elif 'chuck-run' in keys:
                self.logger.info(Style.GREY(f"In Task {work_pointer} detected 'chuck-run'"))
                rep = chain_mem.vector_store[uesd_mem[task['chuck-run']]]['represent']
                if len(rep) == 0:
                    self.get_context_memory().crate_live_context(uesd_mem[task['chuck-run']])
                    rep = chain_mem.vector_store[uesd_mem[task['chuck-run']]]['represent']
                if len(rep) == 0:
                    final = chain_mem.search(uesd_mem[task['chuck-run']], args)
                    if len(final) == 0:
                        final = chain_mem.get_context_for(args)

                    action = f"Act as an summary expert your specialties are writing summary. you are known to " \
                             f"think in small and " \
                             f"detailed steps to get the right result. Your task : write a summary reladet to {args}\n\n{final}"
                    t = self.get_agent_config_class('thinkm')
                    ret = self.run_agent(t, action)
                ret_chunk = []
                chunk_num = -1
                for chunk_vec in rep:
                    chunk_num += 1
                    self.logger.info(Style.GREY(f"In chunk {chunk_num}"))
                    if not chunk_vec:
                        self.logger.warning(Style.YELLOW(f"In chunk {chunk_num} no detected 'chunk' detected"))
                        continue

                    chunk = chain_mem.hydrate_vectors(uesd_mem[task['chuck-run']], chunk_vec)

                    args_ = args.replace(task['chuck-run'], str(chunk[0].page_content))

                    ret, sum_sto, chain_ret_ = self.chain_cor_runner(use, task_name, args_, config, sto_name, task,
                                                                     work_pointer,
                                                                     keys,
                                                                     chain_ret, sum_sto)
                    ret_chunk.append(ret)
                ret = ret_chunk

            else:

                ret, sum_sto, chain_ret_ = self.chain_cor_runner(use, task_name, args, config, sto_name, task,
                                                                 work_pointer,
                                                                 keys,
                                                                 chain_ret, sum_sto)

            # if 'validate' in keys:
            #     self.print("Validate task")
            #     try:
            #         pipe_res = self.text_classification(ret)
            #         self.print(f"Validation :  {pipe_res[0]}")
            #         if pipe_res[0]['score'] > 0.8:
            #             if pipe_res[0]['label'] == "NEGATIVE":
            #                 print('🟡')
            #                 if 'on-error' in keys:
            #                     if task['validate'] == 'inject':
            #                         task['inject'](ret)
            #                     if task['validate'] == 'return':
            #                         task['inject'](ret)
            #                         chain_ret.append([task, ret])
            #                         return "an error occurred", chain_ret
            #             else:
            #                 print(f'🟢')
            #     except Exception as e:
            #         print(f"Error in validation : {e}")

            if 'to-edit-text' in keys:
                config.edit_text.text = ret

            chain_data, chain_ret, uesd_mem = self.chain_return(keys, chain_ret_, task, task_name, ret,
                                                                chain_data, uesd_mem, chain_ret)

            self.print(Style.ITALIC(Style.GREY(f'Chain at {work_pointer}\nreturned : {str(ret)[:150]}...')))

            if sto_config:
                config = sto_config
                sto_config = None

            config.mode = default_mode
            config.completion_mode = default_completion_mode

            if 'brakeOn' in keys:
                do_brake = False
                if isinstance(task['brakeOn'], list):
                    for b in task['brakeOn']:
                        if b in ret:
                            do_brake = True

                if isinstance(task['brakeOn'], str):

                    if task['brakeOn'] in ret:
                        do_brake = True

                if isinstance(task['brakeOn'], bool):

                    if task['brakeOn']:
                        do_brake = True

                running = not do_brake

            work_pointer += 1
            if work_pointer >= end or work_pointer >= len(agent_tasks):
                running = False

        config.mode = default_mode_
        config.completion_mode = default_completion_mode_

        if chain_data_infos:
            return chain_ret, chain_data, uesd_mem

        chain_sum_data = dilate_string(self.summarize_ret_list(chain_ret), 0, 2, 0)
        sum_a = self.get_agent_config_class("thinkm")
        sum_a.get_messages(create=True)
        return self.run_agent(sum_a,
                              f"Develop a concise and relevant response for the user. This response should be brief"
                              f", pertinent, and clear. Summarize the information and present the progress."
                              f" This reply will be transcribed into speech for the user."
                              f"\nInformation:{chain_sum_data}"
                              f"User Input:{user_text}\n", mode_over_lode="conversation"), chain_ret

    def chain_cor_runner(self, use, task_name, args, config, sto_name, task, steps, keys, chain_ret, sum_sto):
        ret = ''
        ret_data = []
        task_name = task_name.strip()
        self.logger.info(Style.GREY(f"using {steps} {use} {task_name} {args[:15]}..."))
        if use == "tool":
            if 'agent' in task_name.lower():
                ret = self.run_agent(config, args, mode_over_lode="tools")
            else:
                ret = self.run_tool(args, task_name, config)

        elif use == "agent":
            if config.mode == 'free':
                config.task_list.append(args)
            ret = self.run_agent(config, args, mode_over_lode=config.mode)
        elif use == 'function':
            if 'function' in keys:
                if callable(task['function']) and chain_ret:
                    task['function'](chain_ret[-1][1])

        elif use == 'expyd' or use == 'chain':
            ret, ret_data = self.execute_thought_chain(args, self.agent_chain.get(task_name.strip()), config,
                                                       speak=self.speak)
        else:
            self.print(Style.YELLOW(f"use is not available {use} avalabel ar [tool, agent, function, chain]"))

        self.logger.info(Style.GREY(f"Don : {str(ret)[:15]}..."))

        if 'short-mem' in keys:
            self.logger.warning(Style.GREY(f"In chunk {steps} no detected 'short-mem' {task['short-mem']}"))
            if task['short-mem'] == "summary":
                short_mem = config.short_mem.text
                if short_mem != sum_sto:
                    config.short_mem.clear_to_collective()
                    config.short_mem.text = self.mas_text_summaries(short_mem)
                else:
                    sum_sto = short_mem
            if task['short-mem'] == "full":
                pass
            if task['short-mem'] == "clear":
                config.short_mem.clear_to_collective()

        return ret, sum_sto, ret_data

    def chain_return(self, keys, chain_ret_, task, task_name, ret, chain_data, uesd_mem, chain_ret):

        if "return" in keys:
            if chain_ret_:
                ret = chain_ret_
            if 'text-splitter' in keys:
                mem = self.get_context_memory()
                sep = ''
                al = 'KMeans'
                if 'separators' in keys:
                    sep = task['separators']
                    if task['separators'].endswith('code'):
                        al = 'AgglomerativeClustering'
                        sep = sep.replace('code', '')
                self.print(f"task_name:{task_name} al:{al} sep:{sep}")
                ret = mem.split_text(task_name, ret, separators=sep, chunk_size=task['text-splitter'])
                mem.add_data(task_name)

                mem.crate_live_context(task_name, al)
                uesd_mem[task['return']] = task_name

            chain_data[task['return']] = ret
            chain_ret.append([task['name'], ret])

        return chain_data, chain_ret, uesd_mem

    def execute_2tree(self, user_text, tree, config: Agent):
        config.binary_tree = tree
        config.stop_sequence = "\n\n\n\n"
        config.set_completion_mode('chat')
        res_um = 'Plan for The Task:'
        res = ''
        tree_depth_ = config.binary_tree.get_depth(config.binary_tree.root)
        for _ in range(tree_depth_):
            self.print(f"NEXT chain {config.binary_tree.get_depth(config.binary_tree.root)}"
                       f"\n{config.binary_tree.get_left_side(0)}")
            res = self.run_agent(config, user_text, mode_over_lode='q2tree')
            tree_depth = config.binary_tree.get_depth(config.binary_tree.root)
            don, next_on, speak = False, 0, res
            str_ints_list_to = list(range(tree_depth + 1))
            for line in res.split("\n"):
                if line.startswith("Answer"):
                    print(F"LINE:{line[:10]}")
                    for char in line[6:12]:
                        char_ = char.strip()
                        if char_ in [str(x) for x in str_ints_list_to]:
                            next_on = int(char_)
                            break

                if line.startswith("+1"):
                    print(F"detected +1")
                    line = line.replace("+1", '')
                    exit_on = -1
                    if "N/A" in line:
                        alive = False
                        res_um = "Task is not fitting isaa's capabilities"
                        break
                    for char in line[0:6]:
                        char_ = char.strip()
                        if char_ in [str(x) for x in str_ints_list_to]:
                            exit_on = int(char_)
                            break
                    if exit_on != -1:
                        next_on = exit_on

            if next_on == 0:
                if len(res) < 1000:
                    for char in res:
                        char_ = char.strip()
                        if char_ in [str(x) for x in str_ints_list_to]:
                            next_on = int(char_)
                            break

            if next_on == tree_depth:
                alive = False
                break

            elif next_on == 0:
                alive = False
                res_um = 'Task is to complicated'
                break
            else:
                new_tree = config.binary_tree.cut_tree('L' * (next_on - 1) + 'R')
                config.binary_tree = new_tree

        return res, res_um

    def stream_read_llm(self, text, config, r=2.0, line_interpret=False, interpret=lambda x: '', prompt=None):

        if prompt is None:
            prompt = config.get_specific_prompt(text)

        p_token_num = config.get_tokens(text)
        config.token_left = config.max_tokens - p_token_num
        # self.print(f"TOKENS: {p_token_num}:{len(text)} | left = {config.token_left if config.token_left > 0 else '-'} |"
        #            f" max : {config.max_tokens}")
        llm_output = None

        if config.token_left < 0:
            text = self.mas_text_summaries(text)
            p_token_num = config.get_tokens(text)
            config.token_left = config.max_tokens - p_token_num
            self.print(f"TOKENS: {p_token_num} | left = {config.token_left if config.token_left > 0 else '-'}")

        if p_token_num == 0 and len(text) <= 9:
            self.print(f"No context")
            return "No context"

        if '/' in config.model_name:
            # if text:
            #     config.step_between = text
            if "{input}" not in prompt:
                prompt += '{xVx}'

            prompt_llm = PromptTemplate(
                input_variables=['xVx'],
                template=prompt
            )
            try:
                llm_output = LLMChain(prompt=prompt_llm, llm=self.get_llm_models(config.model_name)).run(text)
            except ValueError:
                llm_output = "ValueError: on generation"

            return self.add_price_data(prompt=prompt,
                                       config=config,
                                       llm_output=llm_output)

        elif config.model_name.startswith('gpt4all#'):

            if f'LLM-model-{config.model_name}' not in self.config.keys():
                self.load_llm_models(config.model_name)

            llm_output = self.config[f'LLM-model-{config.model_name}'].generate(
                prompt=prompt,
                streaming=config.stream,

                temp=config.temperature,
                top_k=34,
                top_p=0.4,
                repeat_penalty=1.18,
                repeat_last_n=64,
                n_batch=8,
            )

            if not config.stream:
                return self.add_price_data(prompt=prompt,
                                           config=config,
                                           llm_output=llm_output)

        try:
            if not config.stream and llm_output is None:
                with Spinner(
                    f"Generating response {config.name} {config.model_name} {config.mode} {config.completion_mode}"):
                    res = self.process_completion(prompt, config)
                if config.completion_mode == 'chat':
                    config.add_message('assistant', res)
                self.add_price_data(prompt=config.last_prompt, config=config, llm_output=res)
                return res

            if llm_output is None:
                llm_output = self.process_completion(prompt, config)

            # print(f"Generating response (/) stream (\\) {config.name} {config.model_name} {config.mode} "
            #       f"{config.completion_mode}")
            min_typing_speed, max_typing_speed, res = 0.01, 0.005, ""
            try:
                line_content = ""
                results = []
                for line in llm_output:
                    ai_text = ""

                    if len(line) == 0 or not line:
                        continue

                    if isinstance(line, dict):
                        data = line['choices'][0]

                        if "text" in data.keys():
                            ai_text = line['choices'][0]['text']
                        elif "content" in data['delta'].keys():
                            ai_text = line['choices'][0]['delta']['content']

                    if isinstance(line, str):
                        ai_text = line
                    line_content += ai_text
                    if line_interpret and "\n" in line_content:
                        if interpret(line_content):
                            line_interpret = False
                        line_content = ""

                    for i, word in enumerate(ai_text):
                        if not word:
                            continue
                        if self.print_stream != print:
                            self.print_stream({'isaa-text': word})
                        else:
                            print(word, end="", flush=True)
                        typing_speed = random.uniform(min_typing_speed, max_typing_speed)
                        time.sleep(typing_speed)
                        # type faster after each word
                        min_typing_speed = min_typing_speed * 0.04
                        max_typing_speed = max_typing_speed * 0.03
                    res += str(ai_text)
                if line_interpret and line_content:
                    interpret(line_content)
            except requests.exceptions.ChunkedEncodingError as ex:
                print(f"Invalid chunk encoding {str(ex)}")
                self.print(f"{' ' * 30} | Retry level: {r} ", end="\r")
                with Spinner("ChunkedEncodingError", symbols='c'):
                    time.sleep(2 * (3 - r))
                if r > 0:
                    print('\n\n')
                    return self.stream_read_llm(text + '\n' + res, config, r - 1, prompt=prompt)
            if config.completion_mode == 'chat':
                config.add_message('assistant', res)
            self.add_price_data(prompt=config.last_prompt, config=config, llm_output=res)
            return res
        except openai.error.RateLimitError:
            self.print(f"{' ' * 30}  | Retry level: {r} ", end="\r")
            if r > 0:
                self.logger.info(f"Waiting {5 * (8 - r)} seconds")
                with Spinner("Waiting RateLimitError", symbols='+'):
                    time.sleep(5 * (8 - r))
                self.print(f"\n Retrying {r} ", end="\r")
                return self.stream_read_llm(text, config, r - 1, prompt=prompt)
            else:
                self.logger.error("The server is currently overloaded with other requests. Sorry about that!")
                return "The server is currently overloaded with other requests. Sorry about that! ist als possible that" \
                       " we hit the billing limit consider updating it."

        except openai.error.InvalidRequestError:
            self.print(f"{' ' * 30} | Retry level: {r} ", end="\r")
            with Spinner("Waiting InvalidRequestError", symbols='b'):
                time.sleep(1.5)
            if r > 1.25:
                config.short_mem.cut()
                config.edit_text.cut()
                config.observe_mem.cut()
                return self.stream_read_llm(text, config, r - 0.25, prompt=prompt)
            elif r > 1:
                config.shorten_prompt()
                return self.stream_read_llm(text, config, r - 0.25, prompt=prompt)
            elif r > .75:
                config.set_completion_mode("chat")
                config.get_messages(create=True)
                return self.stream_read_llm(self.mas_text_summaries(text), config, r - 0.25, prompt=prompt)
            elif r > 0.5:
                config.stream = False
                res = self.stream_read_llm(self.mas_text_summaries(text), config, r - 0.25, prompt=prompt)
                config.stream = True
                return res
            elif r > 0.25:
                config.short_mem.clear_to_collective()
                config.edit_text.clear_to_collective()
                config.observe_mem.cut()
                return self.stream_read_llm(text, config, r - 0.25, prompt=prompt)
            else:
                self.logger.error("The server is currently overloaded with other requests. Sorry about that!")
                return "The System cannot correct the text input for the agent."

        except openai.error.APIError as e:
            self.logger.error(str(e))
            self.print("retying error Service side")
            return self.stream_read_llm(text, config, r - 0.25, prompt=prompt)

        # except Exception as e:
        #    self.logger.error(str(e))
        #    return "*Error*"
"""
