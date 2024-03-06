import os
import time
from dataclasses import dataclass, field, asdict
from functools import reduce
from random import uniform
from typing import Optional, List, TypeAlias, NewType, TypeVar, Dict, Callable, Any, Generator, Tuple

from enum import Enum
from typing import Optional

from langchain import HuggingFaceHub
from langchain.agents import AgentType
from langchain_community.chat_models import ChatLiteLLMRouter
from litellm.llms.prompt_templates.factory import prompt_factory, llama_2_chat_pt, falcon_chat_pt, falcon_instruct_pt, \
    mpt_chat_pt, wizardcoder_pt, phind_codellama_pt, hf_chat_template, default_pt, ollama_pt
from litellm.utils import trim_messages, check_valid_key, get_valid_models, get_max_tokens

from litellm import longer_context_model_fallback_dict, ContextWindowExceededError, BudgetManager, get_model_info, \
    batch_completion

from .AgentUtils import ShortTermMemory, AIContextMemory, get_token_mini, get_max_token_fom_model_name, PyEnvEval, \
    getSystemInfo, get_price, ObservationMemory, IsaaQuestionBinaryTree, dilate_string, find_json_objects_in_str, \
    complete_json_object, _extract_from_json, _extract_from_string_de, _extract_from_string, anything_from_str_to_dict

import litellm
import logging
from litellm import completion, model_list, token_counter
from litellm.caching import Cache

import gpt4all

from toolboxv2 import get_logger, get_app, Style, Spinner
import json
from dataclasses import asdict
from typing import Type

# litellm.cache = Cache()
logger = get_logger()
litellm.set_verbose = logger.level == logging.DEBUG


def stram_print(text):
    min_typing_speed, max_typing_speed = 0.01, 0.005
    for i, word in enumerate(text):
        if not word:
            continue
        print(word, end="", flush=True)
        typing_speed = uniform(min_typing_speed, max_typing_speed)
        time.sleep(typing_speed)
        min_typing_speed = min_typing_speed * 0.04
        max_typing_speed = max_typing_speed * 0.03


def get_str_response(chunk):
    if isinstance(chunk, dict):
        data = chunk['choices'][0]

        if "delta" in data.keys():
            message = chunk['choices'][0]['delta']
            if isinstance(message, dict):
                message = message['content']
        elif "text" in data.keys():
            message = chunk['choices'][0]['text']
        elif "message" in data.keys():
            message = chunk['choices'][0]['message']['content']
        elif "content" in data['delta'].keys():
            message = chunk['choices'][0]['delta']['content']
        else:
            message = ""

    elif isinstance(chunk, str):
        message = chunk
    else:
        try:
            if hasattr(chunk.choices[0], 'message'):
                message = chunk.choices[0].message.content
            elif hasattr(chunk.choices[0], 'delta'):
                message = chunk.choices[0].delta.content
                if message is None:
                    message = ''
            else:
                raise AttributeError
        except AttributeError:
            message = f"Unknown chunk type {chunk}{type(chunk)}"
    return message


def add_to_kwargs_if_not_none(**values):
    return {k: v for k, v in values.items() if v}


# @dataclass(frozen=True)
# class Providers(Enum):
#     DEFAULT = None
#     ANTHROPIC = "Anthropic"
#     OPENAI = "OpenAI"
#     REPLICATE = "Replicate"
#     COHERE = "Cohere"
#     HUGGINGFACE = "Huggingface"
#     OPENROUTER = "OpenRouter"
#     AI21 = "AI21"
#     VERTEXAI = "VertexAI"
#     BEDROCK = "Bedrock"
#     OLLAMA = None
#     SAGEMAKER = "Sagemaker"
#     TOGETHERAI = "TogetherAI"
#     ALEPHALPHA = "AlephAlpha"
#     PALM = "Palm"
#     NLP = "NLP"
#     VLLM = "vllm"
#     PETALS = "Petals"
#     LOCAL = "Local"
#     MYAPI = "Myapi"


@dataclass
class Trims(Enum):
    """
    The `Trims` class represents the available text trim options for LLM.
    """
    LITELLM = "Trims"
    ISAA = "IsaaTrim"


@dataclass(frozen=True)
class CompletionError(Enum):
    Rate_Limit_Errors = "RateLimitErrors"
    Invalid_Request_Errors = "InvalidRequestErrors"
    Authentication_Errors = "AuthenticationErrors"
    Timeout_Errors = "TimeoutErrors"
    ServiceUnavailableError = "ServiceUnavailableError"
    APIError = "APIError"
    APIConnectionError = "APIConnectionError"


@dataclass(frozen=True)
class LLMFunction:
    name: str
    description: str
    parameters: Dict[str, str] or List[str] or None
    function: Optional[Callable[[str], str]]

    def __str__(self):
        return f"----\nname -> '{self.name}'\nparameters -> '{self.parameters}' ->\ndescription -> '{self.description}'"


@dataclass(frozen=True)
class LLMMessage:
    role: str
    content: str


@dataclass(frozen=True)
class Capabilities:
    name: str
    description: str
    trait: str
    functions: Optional[List[LLMFunction]]

    # TODO: use a agent to combine capabilities


@dataclass
class LLMMode:
    name: str
    description: str
    system_msg: str
    post_msg: Optional[str] = None
    examples: Optional[List[str]] = None

    def __str__(self):
        return f"LLMMode: {self.name} (description) {self.description}"


@dataclass(frozen=True)
class AgentPromptData:
    initial_prompt_value: Optional[str]
    final_prompt_value: Optional[str]

    system_pre_message: Optional[str]
    system_post_message: Optional[str]

    user_pre_message: Optional[str]
    user_post_message: Optional[str]

    assistant_pre_message: Optional[str]
    assistant_post_message: Optional[str]


@dataclass(frozen=True)
class AgentModelData:
    name: str = field(default=None, hash=True)
    model: str = field(default=None)
    provider: Optional[str] = field(default=None)
    system_message: str = field(default="")

    temperature: Optional[int] = field(default=None)
    top_k: Optional[int] = field(default=None)
    top_p: Optional[int] = field(default=None)
    repetition_penalty: Optional[int] = field(default=None)

    repeat_penalty: Optional[int] = field(default=None)
    repeat_last_n: Optional[float] = field(default=None)
    n_batch: Optional[int] = field(default=None)

    api_key: Optional[str] = field(default=None)
    api_base: Optional[str] = field(default=None)
    api_version: Optional[str] = field(default=None)
    user_id: Optional[str] = field(default=None)

    fallbacks: Optional[List[Dict[str, str]] or List[str]] = field(default=None)
    stop_sequence: Optional[List[str]] = field(default=None)
    budget_manager: Optional[BudgetManager] = field(default=None)
    caching: Optional[bool] = field(default=None)


def get_free_agent_data_factory(name="Gpt4All", model="ggml-model-gpt4all-falcon-q4_0.bin") -> AgentModelData:
    return AgentModelData(
        name=name,
        model=model,
        provider="Local",
        stop_sequence=["[!X!]"],
    )


def flatten_reduce_lambda(matrix):
    return list(reduce(lambda x, y: x + y, matrix, []))


@dataclass
class ModeController(LLMMode):
    shots: list = field(default_factory=list)

    def add_shot(self, user_input, agent_output):
        self.shots.append([user_input, agent_output])

    def add_user_feedback(self):

        add_list = []

        for index, shot in enumerate(self.shots):
            print(f"Input : {shot[0]} -> llm output : {shot[1]}")
            user_evalution = input("Rank from 0 to 10: -1 to exit\n:")
            if user_evalution == '-1':
                break
            else:
                add_list.append([index, user_evalution])

        for index, evaluation in add_list:
            self.shots[index].append(evaluation)

    def auto_grade(self):
        pass

    @classmethod
    def from_llm_mode(cls, llm_mode: LLMMode, shots: Optional[list] = None):
        if shots is None:
            shots = []

        return cls(
            name=llm_mode.name,
            description=llm_mode.description,
            system_msg=llm_mode.system_msg,
            post_msg=llm_mode.post_msg,
            examples=llm_mode.examples,
            shots=shots
        )


@dataclass
class LLMFunctionRunner:
    args: list or None = field(default=None)
    kwargs: dict or None = field(default=None)
    llm_function: LLMFunction or None = field(default=None)

    def validate(self):
        if self.llm_function is None:
            return False
        if (self.llm_function.parameters is not None) and (self.args is None) and (self.kwargs is None):
            return False
        return True

    def run(self):
        if not self.validate():
            return "Error Invalid arguments"
        try:
            return self.llm_function.function(*self.args, **self.kwargs)
        except Exception as e:
            return "Error " + str(e)


@dataclass
class Agent:
    amd: AgentModelData = field(default_factory=AgentModelData)

    stream: bool = field(default=False)
    messages: List[Dict[str, str]] = field(default_factory=list)
    trim: Trims = field(default=Trims.LITELLM)
    verbose: bool = field(default=False)
    completion_with_config: bool = field(default=False)
    batch_completion: bool = field(default=False)
    stream_function: Callable[[str], bool or None] = field(default_factory=print)

    max_tokens: Optional[int] = field(default=None)
    tasklist: Optional[List[str]] = field(default=None)
    task_index: Optional[int] = field(default=None)

    functions: Optional[List[LLMFunction]] = field(default=None)
    functions_list: Optional[List[Dict[str, Any]]] = field(default=None)
    add_function_to_prompt: Optional[bool] = field(default=None)

    config: Optional[Dict[str, Any]] = field(default=None)

    batch_completion_messages: Optional[List[List[LLMMessage]]] = field(default=None)

    memory: Optional[AIContextMemory] = field(default=None)
    content_memory: Optional[ShortTermMemory] = field(default=None)

    capabilities: Optional[Capabilities] = field(default=None)
    mode: Optional[LLMMode or ModeController] = field(default=None)
    last_result: Optional[Dict[str, Any]] = field(default=None)
    locale: bool = field(default=False)

    model: Optional[gpt4all.GPT4All or HuggingFaceHub] = field(default=None)
    hits: Optional[str] = field(default=None)

    next_fuction: Optional[str] = field(default=None)
    llm_function_runner: Optional[LLMFunctionRunner] = field(default=None)
    logger_callback: Optional[Callable] = field(default=None)  # example (print)

    def convert_functions(self):
        self.functions_list = []
        if self.functions is not None and self.add_function_to_prompt:
            self.functions_list = [{"name": f.name, "description": f.description, "parameters": f.parameters} for f in
                                   self.functions]

    def logger(self):
        return self.logger_callback

    def check_valid(self):

        if self.amd.name is None:
            print(self.amd)
            return False

        if self.amd.provider is not None and self.amd.provider.upper() in ["LOCAL"]:
            return True

        response = check_valid_key(model=self.amd.model, api_key=self.amd.api_key)

        if not response:
            self.print_verbose(f"Agent Failed {self.amd.name} {self.amd.model}")

        self.print_verbose(f"Agent Parsed {self.amd.name} {self.amd.model}")
        return response

    def construct_first_msg(self, message: List[Dict[str, str]]) -> List[Dict[str, str]]:
        llm_prompt = self.amd.system_message
        self.print_verbose(f"construct first msg")
        cfunctions_infos = []
        if self.capabilities:
            llm_prompt += '\n'+self.capabilities.trait

            if self.capabilities.functions:
                cfunctions_infos = [functions for functions in self.capabilities.functions if functions not in self.functions]

        if self.mode:
            llm_prompt += '\n'+self.mode.system_msg

            if self.mode.examples:
                llm_prompt += "\nExamples: \n" + '-----\n' + "\n---\n".join(self.mode.examples) + '\n---\n'

        if self.functions or len(cfunctions_infos):
            functions_infos = "\n".join([str(functions) for functions in self.functions+cfunctions_infos])
            message.append(asdict(LLMMessage("system", "calling a fuction by using this exact syntax (json) : {"
                                                       "'Action':str, 'Inputs':str or dict}\nWhere Action is equal to "
                                                       "the fuction name and Inputs to the fuction input. use str for "
                                                       "single input function and a kwarg dict for multiple inputs!! USE THIS FORMAT")))
            message.append(asdict(LLMMessage("system", f"Callable functions:\n{functions_infos}\n--+--\n")))

        if llm_prompt:
            message.append(asdict(LLMMessage("system", llm_prompt)))

        return message

    def get_batch_llm_messages(self, tasks: List[str], fetch_memory: Optional[bool] = None,
                               isaa=None, message=None, task_from: str = 'user', all_meme=False):
        llm_messages = []
        for task in tasks:
            llm_messages.append(self.get_llm_message(task=task,
                                                     persist=False,
                                                     fetch_memory=fetch_memory,
                                                     isaa=isaa,
                                                     message=message,
                                                     task_from=task_from,
                                                     all_meme=all_meme))
        return llm_messages

    def get_llm_message(self, task: str, persist: Optional[bool] = None, fetch_memory: Optional[bool] = None,
                        isaa=None, message=None, task_from: str = 'user', all_meme=False):

        if message is None:
            message = []

        llm_message = self.construct_first_msg(message) if not persist else (
            self.messages if len(self.messages) > 0 else self.construct_first_msg(message))
        memory_task = ""
        memory_context = ""
        memory_space_name = self.amd.name

        if all_meme:
            memory_space_name = None

        if fetch_memory and self.memory is not None:
            memory_task = self.memory.get_context_for(task, memory_space_name)
        if fetch_memory and (self.memory is not None) and self.content_memory is not None:
            memory_context = self.memory.get_context_for(self.content_memory.text, memory_space_name)

        if fetch_memory and memory_context:
            self.print_verbose(f"Appending History summary:")
            self.messages = self.trim_msg(self.messages, isaa)
            llm_message.append(asdict(LLMMessage("system", "History summary:" + memory_context)))

        if fetch_memory and memory_task and memory_context != memory_task:
            self.print_verbose(f"Appending Memory data")
            llm_message.append(asdict(LLMMessage("system", "Additional memory Informations:" + memory_task)))

        llm_message.append(asdict(LLMMessage(task_from, task)))

        if self.mode is not None:
            if self.mode.post_msg is not None:
                self.print_verbose(f"Appending Mode Data {self.mode.name}")
                llm_message.append(asdict(LLMMessage("system", self.mode.post_msg)))

        llm_message = self.trim_msg(llm_message, isaa)

        if persist:
            for i in range(len(llm_message)):
                self.messages.append(llm_message[i])

            if fetch_memory and self.content_memory is not None:
                self.content_memory.text += f"\nQ:{task}\nR:"

            if fetch_memory and self.memory is not None:
                with Spinner(message=f"Persisting Memory ...", symbols='w'):
                    self.memory.add_data(self.amd.name, f"Q:{task}")

        self.print_verbose("Returning llm message")
        return llm_message

    def trim_msg(self, llm_message, isaa=None):

        if self.trim.name == 'Trims':
            self.print_verbose("Timing with Trims")
            with Spinner(message="Sorten prompt lit...", symbols='d'):
                new_msg = trim_messages(llm_message, self.amd.model)
                if new_msg:
                    llm_message = new_msg

        if self.trim.name == 'IsaaTrim' and isaa:
            self.print_verbose("Timing with IsaaTrim")

            def get_tokens_estimation(text, only_len=True):
                if isinstance(text, list):
                    text = '\n'.join(msg['content'] for msg in text)
                tokens = get_token_mini(text, self.amd.model, isaa, only_len)
                if only_len:
                    if tokens == 0:
                        tokens = int(len(text) * (3 / 4))
                return tokens

            with Spinner(message=f"Sorten prompt ...", symbols='b'):
                llm_message = isaa.short_prompt_messages(llm_message, get_tokens_estimation,
                                                         get_max_token_fom_model_name(self.amd.model))
        return llm_message

    def completion(self, llm_message, batch=False, **kwargs):
        self.print_verbose("Starting completion")
        if self.amd.provider is not None and self.amd.provider.upper() == "GPT4All" and self.model is None:
            self.model = gpt4all.GPT4All(self.amd.model)

        if self.amd.provider is not None and self.amd.provider.upper() == "GPT4All" and self.model is not None:
            prompt = ""
            if "chat" in self.amd.model:
                if "llama-2" in self.amd.model:
                    prompt = llama_2_chat_pt(messages=llm_message)
                if "falcon" in self.amd.model:
                    prompt = falcon_chat_pt(messages=llm_message)
                if "mpt" in self.amd.model:
                    prompt = mpt_chat_pt(messages=llm_message)
            elif "wizard" in self.amd.model:
                prompt = wizardcoder_pt(messages=llm_message)
            elif "instruct" in self.amd.model:
                prompt = ollama_pt(model=self.amd.model, messages=llm_message)
                if "falcon" in self.amd.model:
                    prompt = falcon_instruct_pt(messages=llm_message)
            else:
                try:
                    prompt = hf_chat_template(self.amd.model, llm_message)
                except Exception:
                    pass
                if not prompt:
                    prompt = default_pt(messages=llm_message)

            if not prompt:
                prompt = prompt_factory(self.amd.model, llm_message, self.amd.provider)

            if not prompt:
                print("No prompt")
                return

            if kwargs.get('mock_response', False):
                return kwargs.get('mock_response')

            stop_callback = None

            if self.amd.stop_sequence:

                self.hits = ""  # TODO : IO string wirte

                def stop_callback_func(token: int, response):
                    self.hits += response
                    if self.hits in self.amd.stop_sequence:
                        return False
                    if response == ' ':
                        self.hits = ""

                    return True

                stop_callback = stop_callback_func

            # Werte, die überprüft werden sollen
            dynamic_values = {

                'streaming': self.stream,
                'temp': self.amd.temperature,
                'top_k': self.amd.top_k,
                'top_p': self.amd.top_p,
                'repeat_penalty': self.amd.repeat_penalty,
                'repeat_last_n': self.amd.repeat_last_n,
                'n_batch': self.amd.n_batch,
                'max_tokens': self.max_tokens,
                'callback': stop_callback
            }

            # Füge Werte zu kwargs hinzu, wenn sie nicht None sind
            kwargs.update(add_to_kwargs_if_not_none(**dynamic_values))

            result = self.model.generate(
                prompt=prompt,
                **kwargs
            )
            self.print_verbose("Local Completion don")
            return result

        # Werte, die überprüft werden sollen
        dynamic_values = {
            'temperature': self.amd.temperature,
            'top_p': self.amd.top_p,
            'top_k': self.amd.top_k,
            'stream': self.stream,
            'stop': self.amd.stop_sequence,
            'max_tokens': self.max_tokens,
            'user': self.amd.user_id,
            'api_base': self.amd.api_base,
            'api_version': self.amd.api_version,
            'api_key': self.amd.api_key,
            'logger_fn': self.logger(),
            'verbose': self.verbose,
            'fallbacks': self.amd.fallbacks,
            'caching': self.amd.caching,
            'functions': self.functions_list,
            'custom_llm_provider': self.amd.provider if self.amd.provider is not None and self.amd.provider.upper() != "DEFAULT" else None
        }

        if self.add_function_to_prompt:
            litellm.add_function_to_prompt = True

        # Füge Werte zu kwargs hinzu, wenn sie nicht None sind
        kwargs.update(add_to_kwargs_if_not_none(**dynamic_values))

        if batch:
            result = batch_completion(
                model=self.amd.model,
                messages=llm_message,
                **kwargs
            )
        else:
            result = completion(
                model=self.amd.model,
                messages=llm_message,
                **kwargs
            )

        litellm.add_function_to_prompt = False
        self.print_verbose("Completion", "Done" if not self.stream else "in progress..")
        return result

    def run_model(self, llm_message, persist_local=True, persist_mem=True, batch=False, **kwargs):

        if not llm_message:
            return None

        self.print_verbose("Running llm model")

        self.next_fuction = None
        result = self.completion(llm_message, batch, **kwargs)
        if self.amd.budget_manager:
            self.amd.budget_manager.update_cost(user=self.amd.user_id, model=self.amd.model, completion_obj=result)

        self.last_result = result
        llm_response = ""
        if not self.stream:
            llm_response = get_str_response(chunk=result)
        if self.stream:
            self.print_verbose("Start streaming")

            if self.stream_function is None:
                self.stream_function = stram_print

            for chunk in result:
                message = get_str_response(chunk=chunk)
                llm_response += message
                if self.stream_function(message):
                    break
            print()

        if persist_local:
            self.messages.append(asdict(LLMMessage("assistant", llm_response)))

        if persist_mem and self.memory is not None:
            self.memory.add_data(self.amd.name, llm_response)

        if persist_mem and self.content_memory is not None:
            self.content_memory.text += llm_response

        if self.mode is not None:
            if isinstance(self.mode, ModeController) and hasattr(self.mode, '') and llm_message[-1].get('content',
                                                                                                        False):
                self.mode.add_shot(llm_message[-1].get('content'), llm_response)

        return llm_response

    def if_for_fuction_use(self, llm_response):
        llm_fuction = None
        fuction_inputs = None
        self.next_fuction = None

        if self.capabilities is not None and self.capabilities.functions is not None and len(
            self.capabilities.functions) > 0:
            callable_functions = [fuction_name.name.lower() for fuction_name in self.capabilities.functions]
            self.next_fuction, fuction_inputs = self.test_use_function(llm_response, callable_functions)
            if self.next_fuction is not None:
                llm_fuction = self.capabilities.functions[callable_functions.index(self.next_fuction.lower())]

        if self.functions is not None and len(self.functions) > 0 and self.next_fuction is None:
            callable_functions = [fuction_name.name.lower() for fuction_name in self.functions]
            self.next_fuction, fuction_inputs = self.test_use_function(llm_response, callable_functions)
            if self.next_fuction is not None:
                llm_fuction = self.functions[callable_functions.index(self.next_fuction.lower())]

        if self.next_fuction is None and llm_fuction is None:
            self.llm_function_runner = LLMFunctionRunner(
                llm_function=None,
                args=None,
                kwargs=None,
            )
            self.print_verbose("No fuction called")

            return False

        args = []
        kwargs = {}

        if fuction_inputs is not None:
            args, kwargs = self.parse_arguments(fuction_inputs, llm_fuction.parameters)

        self.llm_function_runner = LLMFunctionRunner(
            llm_function=llm_fuction,
            args=args,
            kwargs=kwargs,
        )
        self.print_verbose("Function runner initialized")
        return True

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(Style.BLUE(f"AGENT:{self.amd.name}-VERBOSE: "), end='')
            print(*args, **kwargs)

    def execute_fuction(self, persist=True, persist_mem=True):
        if self.next_fuction is None:
            if self.verbose:
                print("No fuction to execute")
            return "No fuction to execute"

        if self.llm_function_runner is None:
            if self.verbose:
                print("No llm function runner to execute")
            return "No llm function runner to execute"

        if not self.llm_function_runner.validate():
            if self.verbose:
                print("Invalid llm function runner")
            return "Invalid llm function runner"

        result = self.llm_function_runner.run()

        self.print_verbose(f"Fuction {self.llm_function_runner.llm_function.name} Result : {result}")

        if persist:
            self.messages.append({'content': f"F:{result}", 'role': "system"})

        if persist_mem and self.content_memory is not None:
            self.content_memory.text += f"F:{result}"
            self.print_verbose("Persist to content Memory")

        if persist_mem and self.memory is not None:
            self.memory.add_data(self.amd.name, f"F:{result}")
            self.print_verbose(f"Persist to Memory sapce {self.amd.name}")
        if not isinstance(result, str):
            result = str(result)
        return result

    def stram_registrator(self, func: Callable[[str], bool]):
        self.print_verbose("StramRegistrator")
        self.stream_function = func

    def init_memory(self, isaa, name):
        if name is None:
            raise ValueError("Invalid Agent")
        self.print_verbose("Initializing Memory")
        self.memory = isaa.get_context_memory()
        self.content_memory = ShortTermMemory(isaa, name + "-ShortTermMemory")

    def save_memory(self):
        self.print_verbose("Saving memory")
        if self.content_memory is not None:
            self.print_verbose("Saved memory to collective")
            self.content_memory.clear_to_collective()

    def token_counter(self, messages: list):
        return token_counter(model=self.amd.model, messages=messages)

    @staticmethod
    def test_use_function(agent_text: str, all_actions: List[str], language='en') -> Tuple[str or None, str or None]:
        if not agent_text:
            return None, None
        # all_actions = [action_.lower() for action_ in all_actions]
        get_app("Agent_logging").logger.info("Start testing tools")

        print(f"_extract_from_json all_actions, {all_actions}")

        action, inputs = _extract_from_json(agent_text.replace("'", '"'), all_actions)
        print(f"{action=}| {inputs=} {action in all_actions=}")
        if action and action.lower() in all_actions:
            return action, inputs

        if language == 'de':

            # print("_extract_from_string")
            action, inputs = _extract_from_string_de(agent_text, all_actions)
            # print(f"{action=}| {inputs=} {action in config.tools.keys()=}")
            if action and action in all_actions:
                return action, inputs

        print("_extract_from_string")
        action, inputs = _extract_from_string(agent_text, all_actions)
        print(f"{action=}| {inputs=} {action in all_actions}")
        if action and action.lower() in all_actions:
            return action, inputs

        try:
            agent_text = agent_text.replace("ACTION:", "")
            dict = eval(agent_text)
            action = dict["Action"]
            inputs = dict["Inputs"]
            if action and action in all_actions:
                return action, inputs
        except:
            pass

        # self.logger.info("Use AI function to determine the action")
        # action = self.mini_task_completion(
        #     f"Is one of the tools called in this line, or is intended '''{agent_text}''' Avalabel tools: {list(config.tools.keys())}? If yes, only answer with the tool name, if no, then with NONE nothing else. Answer:\n")
        # action = action.strip()
        # self.logger.info(f"Use AI : {action}")
        # self.print(f"Use AI : {action}")
        # # print(action in list(config.tools.keys()), list(config.tools.keys()))
        # if action in list(config.tools.keys()):
        #     inputs = agent_text.split(action, 1)
        #     if len(inputs):
        #         inputs = inputs[1].strip().replace("Inputs: ", "")
        #     print(f"{action=}| {inputs=} ")
        #     return action, inputs

        return None, None

    @staticmethod
    def parse_arguments(command: str, parameters: list or dict) -> (list, dict):
        # Initialisierung der Ausgabeliste und des Wörterbuchs
        out_list = []
        out_dict = {}
        args = []
        param_keys = parameters if isinstance(parameters, list) else list(parameters.keys())

        # Überprüfung, ob der Befehl ein Wörterbuch enthält
        if isinstance(command, dict):
            command = json.dumps(command)
        if isinstance(command, list):
            args = command
        if not isinstance(command, str):
            command = str(command)

        if "{" in command and "}" in command:
            s = {}
            for x in param_keys:
                s[x] = None
            arg_dict = anything_from_str_to_dict(command, expected_keys=s)

            if isinstance(arg_dict, list):
                if len(arg_dict) >= 1:
                    arg_dict = arg_dict[0]

            # Überprüfung, ob es nur einen falschen Schlüssel und einen fehlenden gültigen Schlüssel gibt

            missing_keys = [key for key in param_keys if key not in arg_dict]
            extra_keys = [key for key in arg_dict if key not in param_keys]

            if len(missing_keys) == 1 and len(extra_keys) == 1:
                correct_key = missing_keys[0]
                wrong_key = extra_keys[0]
                arg_dict[correct_key] = arg_dict.pop(wrong_key)
            out_dict = arg_dict
        else:
            # Aufteilung des Befehls durch Komma
            if len(param_keys) == 0:
                pass
            elif len(param_keys) == 1:
                out_list.append(command)
            elif len(param_keys) >= 2:

                comma_cont = command.count(',')
                saces_cont = command.count(' ')
                newline_cont = command.count('\n')
                split_key = "-"
                if comma_cont == len(param_keys) - 1:
                    split_key = ","
                elif newline_cont == len(param_keys) - 1:
                    split_key = "\n"
                elif saces_cont == len(param_keys) - 1:
                    split_key = " "

                print(f"{len(param_keys)=}\n{comma_cont}\n{saces_cont}\n{newline_cont}")

                if len(param_keys) == 2:
                    if split_key == "-":
                        split_key = ","
                        pos_space = command.find(" ")
                        pos_comma = command.find(",")
                        if pos_space < pos_comma:
                            split_key = " "
                    args = [arg.strip() for arg in command.split(split_key)]
                    args = [args[0], split_key.join(args[1:])]
                else:
                    args = [arg.strip() for arg in command.split(split_key)]

                # Befüllen des Wörterbuchs und der Liste basierend auf der Signatur

        for i, arg in enumerate(args):
            if i < len(param_keys) and i != "callbacks":
                out_dict[param_keys[i]] = arg
            else:
                out_list.append(arg)

        return out_list, out_dict


@dataclass
class ControllerManager:
    controllers: Dict[str, ModeController] = field(default_factory=dict)

    def rget(self, llm_mode: LLMMode, name: str = None):
        if name is None:
            name = llm_mode.name
        if not self.registered(name):
            self.add(name, llm_mode)
        return self.get(name)

    def registered(self, name):
        return name in self.controllers

    def get(self, name):
        if name in self.controllers:
            return self.controllers[name]
        return None

    def add(self, name, llm_mode, shots=None):
        if name in self.controllers:
            return "Name already defined"

        if shots is None:
            shots = []

        self.controllers[name] = ModeController.from_llm_mode(llm_mode=llm_mode, shots=shots)

    def list(self):
        return list(self.controllers.keys())

    def save(self, filename: Optional[str], get_data=False):

        data = asdict(self)

        if filename is not None:
            with open(filename, 'w') as f:
                json.dump(data, f)

        if get_data:
            return json.dumps(data)

    @classmethod
    def init(cls, filename: Optional[str], json_data: Optional[str] = None):

        controllers = {}

        if filename is None and json_data is None:
            print("No data provided for ControllerManager")
            return cls(controllers=controllers)

        if filename is not None and json_data is not None:
            raise ValueError(f"filename and json_data are provided only one accepted filename or json_data")

        if filename is not None:
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, 'r') as f:
                    controllers = json.load(f)
            else:
                print("file not found")

        if json_data is not None:
            controllers = json.loads(json_data)

        return cls(controllers=controllers)


class AgentBuilder:
    isaa_reference = None

    def __init__(self, agent_class: Type[Agent]):
        self.agent = agent_class()
        self.amd_attributes = {}
        self.missing_amd_fields = ["name", "model"]
        self.is_build = False

    def init_agent_memory(self, name):
        if self.isaa_reference is None:
            raise ValueError("isaa_reference is required")
        self.agent.init_memory(self.isaa_reference, name)
        return self

    def set_isaa_reference(self, isaa):
        self.isaa_reference = isaa
        return self

    def set_amd_name(self, name: str):
        self.amd_attributes['name'] = name
        if "name" not in self.missing_amd_fields:
            self.missing_amd_fields += ["name"]
        self.missing_amd_fields.remove('name')
        return self

    def set_amd_model(self, model: str):
        self.amd_attributes['model'] = model
        if "model" not in self.missing_amd_fields:
            self.missing_amd_fields += ["model"]
        self.missing_amd_fields.remove('model')
        if model.startswith('ollama'):
            return self.set_amd_api_base("http://localhost:11434")
        return self

    def set_amd_provider(self, provider: str):
        self.amd_attributes['provider'] = provider
        return self

    def set_amd_temperature(self, temperature: int):
        self.amd_attributes['temperature'] = temperature
        return self

    def set_amd_top_k(self, top_k: int):
        self.amd_attributes['top_k'] = top_k
        return self

    def set_amd_top_p(self, top_p: int):
        self.amd_attributes['top_p'] = top_p
        return self

    def set_amd_repetition_penalty(self, repetition_penalty: int):
        self.amd_attributes['repetition_penalty'] = repetition_penalty
        return self

    def set_amd_repeat_penalty(self, repeat_penalty: int):
        self.amd_attributes['repeat_penalty'] = repeat_penalty
        return self

    def set_amd_repeat_last_n(self, repeat_last_n: float):
        self.amd_attributes['repeat_last_n'] = repeat_last_n
        return self

    def set_amd_n_batch(self, n_batch: int):
        self.amd_attributes['n_batch'] = n_batch
        return self

    def set_amd_api_key(self, api_key: str):
        self.amd_attributes['api_key'] = api_key
        return self

    def set_amd_api_base(self, api_base: str):
        self.amd_attributes['api_base'] = api_base
        return self

    def set_amd_api_version(self, api_version: str):
        self.amd_attributes['api_version'] = api_version
        return self

    def set_amd_user_id(self, user_id: str):
        self.amd_attributes['user_id'] = user_id
        return self

    def set_amd_fallbacks(self, fallbacks: List[Dict[str, str]] or List[str]):
        self.amd_attributes['fallbacks'] = fallbacks
        return self

    def set_amd_stop_sequence(self, stop_sequence: List[str]):
        self.amd_attributes['stop_sequence'] = stop_sequence
        return self

    def set_amd_budget_manager(self, budget_manager: BudgetManager):
        self.amd_attributes['budget_manager'] = budget_manager
        return self

    def set_amd_caching(self, caching: bool):
        self.amd_attributes['caching'] = caching
        return self

    def set_amd_system_message(self, system_message: str):
        self.amd_attributes['system_message'] = system_message
        return self

        # Fügen Sie weitere Methoden für alle Eigenschaften von AgentModelData hinzu

    def build_amd(self):
        if len(self.missing_amd_fields) != 0:
            raise ValueError(
                f"Invalid AMD configuration missing : {self.missing_amd_fields} set ar \n{self.amd_attributes}")
        # Erstellt ein AgentModelData-Objekt mit den gesetzten Attributen
        self.agent.amd = AgentModelData(**self.amd_attributes)
        if self.agent.amd.name is None:
            raise ValueError(
                f"Invalid AMD configuration missing : Data. set ar \n{self.amd_attributes}")

        return self

    # ==========================================================

    def set_logging_callback(self, logger_callback: Callable):
        self.agent.logger_callback = logger_callback
        return self

    def set_stream(self, stream: bool):
        self.agent.stream = stream
        return self

    def set_messages(self, messages: List[Dict[str, str]]):
        self.agent.messages = messages
        return self

    def set_trim(self, trim: Trims):
        self.agent.trim = trim
        return self

    def set_verbose(self, verbose: bool):
        self.agent.verbose = verbose
        return self

    def set_completion_with_config(self, completion_with_config: bool):
        self.agent.completion_with_config = completion_with_config
        return self

    def set_batch_completion(self, batch_completion: bool):
        self.agent.batch_completion = batch_completion
        return self

    def set_stream_function(self, stream_function: Callable[[str], None]):
        self.agent.stream_function = stream_function
        return self

    def set_max_tokens(self, max_tokens: Optional[int]):
        self.agent.max_tokens = max_tokens
        return self

    def set_tasklist(self, tasklist: Optional[List[str]]):
        self.agent.tasklist = tasklist
        return self

    def set_task_index(self, task_index: Optional[int]):
        self.agent.task_index = task_index
        return self

    def set_functions(self, functions: Optional[List[LLMFunction]]):
        if self.agent.functions is None:
            self.agent.functions = []
        self.agent.functions += functions
        return self

    def set_config(self, config: Optional[Dict[str, Any]]):
        self.agent.config = config
        return self

    def set_batch_completion_messages(self, batch_completion_messages: Optional[List[List[LLMMessage]]]):
        self.agent.batch_completion_messages = batch_completion_messages
        return self

    def set_memory(self, memory: Optional[AIContextMemory]):
        self.agent.memory = memory
        return self

    def set_content_memory(self, content_memory: Optional[ShortTermMemory]):
        self.agent.content_memory = content_memory
        return self

    def set_content_memory_max_length(self, content_memory_max_length: int):
        if self.agent.content_memory is None:
            raise ValueError("content_memory is not set")
        self.agent.content_memory.max_length = content_memory_max_length

    def set_content_memory_isaa_instance(self, isaa):
        if self.agent.content_memory is None:
            raise ValueError("content_memory is not set")
        self.agent.content_memory.isaa = isaa

    def set_capabilities(self, capabilities: Optional[Capabilities]):
        self.agent.capabilities = capabilities
        return self

    def set_mode(self, mode: Optional[LLMMode or ModeController]):
        self.agent.mode = mode
        return self

    def set_last_result(self, last_result: Optional[Dict[str, Any]]):
        self.agent.last_result = last_result
        return self

    def set_locale(self, locale: bool):
        self.agent.locale = locale
        return self

    def set_model(self, model: Optional[gpt4all.GPT4All or HuggingFaceHub]):
        self.agent.model = model
        return self

    def set_hits(self, hits: Optional[str]):
        self.agent.hits = hits
        return self

    def build(self):
        if self.is_build:
            raise ValueError("Agent was constructed! pleas delay builder instance")
        self.build_amd()
        if not self.agent.check_valid():
            raise ValueError(
                f"Invalid Agent:{self.agent.amd.name} Configuration\n{self.amd_attributes}\n{self.agent.amd}")
        print(f"Agent '{self.agent.amd.name}' Agent-Model-Data build successfully")
        if self.agent.functions is not None and self.agent.amd.provider is not None and self.agent.amd.provider.upper() in [
            "LOCAL", "GPT4All"]:
            self.agent.add_function_to_prompt = True
        self.agent.convert_functions()
        self.is_build = True
        return self.agent

    def save_to_json(self, file_path: str):
        clear_data = self.get_dict()
        with open(file_path, 'w') as f:
            json.dump(clear_data, f, ensure_ascii=False, indent=4)
        return clear_data

    def get_dict(self):
        clear_data = {'amd': self.amd_attributes}
        if self.amd_attributes.get('provider') is not None:
            if isinstance(self.amd_attributes['provider'], Enum):
                print(f"{self.amd_attributes['provider'].name=}")
                clear_data['amd']['provider'] = self.amd_attributes['provider'].name
            else:
                clear_data['amd']['provider'] = self.amd_attributes['provider']
        clear_data['stream'] = self.agent.stream  # : bool = field(default=False)
        clear_data['messages'] = self.agent.messages  # : List[Dict[str, str]] = field(default_factory=list)
        clear_data['trim'] = self.agent.trim.name  # : Trims = field(default=Trims.litellm)
        clear_data['verbose'] = self.agent.verbose  # : bool = field(default=False)
        clear_data['completion_with_config'] = self.agent.completion_with_config  # : bool = field(default=False)
        clear_data['batch_completion'] = self.agent.batch_completion  # : bool = field(default=False)
        # clear_data['stream_function'] = self.agent.stream_function  # : Callable[[str], bool or None] = field(default_factory=print)
        clear_data['max_tokens'] = self.agent.max_tokens  # : Optional[float] = field(default=None)
        clear_data['tasklist'] = self.agent.tasklist  # : Optional[List[str]] = field(default=None)
        clear_data['task_index'] = self.agent.task_index  # : Optional[int] = field(default=None)
        # clear_data['functions'] = self.agent.functions  # : Optional[List[LLMFunction]] = field(default=None)
        clear_data[
            'functions_list'] = self.agent.functions_list  # : Optional[List[Dict[str, Any]]] = field(default=None)
        clear_data['config'] = self.agent.config  # : Optional[Dict[str, Any]] = field(default=None)
        # clear_data['batch_completion_messages'] = self.agent.batch_completion_messages  # : Optional[List[List[LLMMessage]]] = field(default=None)
        # clear_data['memory'] = self.agent.memory  # : Optional[AIContextMemory] = field(default=None)
        # clear_data['content_memory'] = self.agent.content_memory  # : Optional[ShortTermMemory] = field(default=None)
        # clear_data['capabilities'] = self.agent.capabilities  # : Optional[Capabilities] = field(default=None)
        # clear_data['mode'] = self.agent.mode  # : Optional[LLMMode or ModeController] = field(default=None)
        clear_data['last_result'] = self.agent.last_result  # : Optional[Dict[str, Any]] = field(default=None)
        clear_data['locale'] = self.agent.locale  # : bool = field(default=False)
        # clear_data['model'] = self.agent.model  # : Optional[gpt4all.GPT4All or HuggingFaceHub] = field(default=None)
        clear_data['hits'] = self.agent.hits  # : Optional[str] = field(default=None)
        clear_data['next_fuction'] = self.agent.next_fuction  # : Optional[str] = field(default=None)
        # clear_data['llm_function_runner'] = self.agent.llm_function_runner  # : Optional[LLMFunctionRunner] = field(default=None
        return clear_data

    @classmethod
    def load_from_json_file(cls, file_path: str, agent_class: Type[Agent]):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(f"Loaded Agent from file {data}")
        except:
            print(f"Could not read from file: {file_path}")
            return cls(agent_class)
        builder = cls(agent_class)
        return cls.load_from_json_file_dict_data(data, builder)

    @staticmethod
    def load_from_json_file_dict_data(data, builder):
        for key, value in data.items():
            if hasattr(builder.agent, key):
                if key == "amd":
                    builder.amd_attributes = value
                    if 'name' in value:
                        builder.set_amd_name(value['name'])
                    if 'model' in value:
                        builder.set_amd_name(value['model'])
                    continue
                setattr(builder.agent, key, value)
        return builder


class AgentBuilder2:  # isaa Agent Adaper refactoring mov to -> Agents .
    available_modes = ['tools', 'planning', 'live',
                       'generate']  # [ 'talk' 'conversation','q2tree', 'python'

    python_env = PyEnvEval()

    capabilities = """Resourceful: Isaa is able to efficiently utilize its wide range of capabilities and resources to assist the user.
Collaborative: Isaa is work seamlessly with other agents, tools, and systems to deliver the best possible solutions for the user.
Empathetic: Isaa is understand and respond to the user's needs, emotions, and preferences, providing personalized assistance.
Inquisitive: Isaa is continually seek to learn and improve its knowledge base and skills, ensuring it stays up-to-date and relevant.
Transparent: Isaa is open and honest about its capabilities, limitations, and decision-making processes, fostering trust with the user.
Versatile: Isaa is adaptable and flexible, capable of handling a wide variety of tasks and challenges."""
    system_information = f"""
system information's : {getSystemInfo('system is starting')}
"""

    def __init__(self, isaa, name="agentConfig"):

        self.custom_tools = []
        self.hugging_tools = []
        self.lag_chin_tools = []
        self.plugins = []
        self.language = 'en'
        self.isaa = isaa

        if self.isaa is None:
            raise ValueError("Define Isaa Tool first AgentConfig")

        self.name: str = name
        self.mode: str = "talk"
        self.model_name: str = "gpt-3.5-turbo-0613"

        self.agent_type: AgentType = AgentType(
            "structured-chat-zero-shot-react-description")  # "zero-shot-react-description"
        self.max_iterations: int = 2
        self.verbose: bool = True

        self.personality = ""
        self.goals = ""
        self.tools: dict = {
            # "test_tool": {"func": lambda x: x, "description": "only for testing if tools are available",
            #              "format": "test_tool(input:str):"}
        }

        self.last_prompt = ""

        self.task_list: List[str] = []
        self.task_list_done: List[str] = []
        self.step_between: str = ""

        self.pre_task: str or None = None
        self.task_index = 0

        self.max_tokens = get_max_token_fom_model_name(self.model_name)
        self.token_left = self.max_tokens
        self.ppm = get_price(self.max_tokens)

        self.consumption = 1000 * self.ppm[0]

        self.temperature = 0.06
        self.messages_sto = {}
        self._stream = False
        self._stream_reset = False
        self.stop_sequence = ["\n\n\n", "Observation:", "Beobachtungen:"]
        self.completion_mode = "chat"
        self.add_system_information = False

        self.init_mem_state = False
        self.context: None or ShortTermMemory = None
        self.observe_mem: None or ObservationMemory = None
        self.edit_text: None or ShortTermMemory = None
        self.short_mem: None or ShortTermMemory = None

        self.init_memory()

        self.binary_tree: IsaaQuestionBinaryTree or None = None

    def save_to_permanent_mem(self):
        if self.short_mem is not None:
            self.short_mem.clear_to_collective()
        if self.edit_text is not None:
            self.edit_text.cut()
        if self.context is not None:
            self.context.clear_to_collective()
        if self.observe_mem is not None:
            self.observe_mem.cut()

    def calc_price(self, prompt: str, output: str):
        return self.ppm[0] * get_token_mini(prompt, self.model_name, self.isaa), self.ppm[1] * get_token_mini(output,
                                                                                                              self.model_name,
                                                                                                              self.isaa)

    def init_memory(self):
        self.init_mem_state = True
        self.short_mem: ShortTermMemory = ShortTermMemory(self.isaa, f'{self.name}-ShortTerm')
        self.edit_text: ShortTermMemory = ShortTermMemory(self.isaa, f'{self.name}-EditText')
        self.edit_text.max_length = 5400
        self.context: ShortTermMemory = ShortTermMemory(self.isaa, f'{self.name}-ContextMemory')
        self.observe_mem: ObservationMemory = ObservationMemory(self.isaa)
        mini_context = "System Context:\n" + self.observe_mem.text + self.short_mem.text + self.context.text
        if mini_context == "System Context:\n":
            mini_context += 'its Day 0 start to explore'
        self.system_information = f"""
system information's : {getSystemInfo(self.isaa.get_context_memory().get_context_for(mini_context))}
"""

    def get_specific_prompt(self, text):

        if '/' in self.model_name:

            if self.mode == "conversation":
                sto, self.add_system_information = self.add_system_information, False
                prompt = self.prompt.replace('{', '}}').replace('}', '{{')
                self.add_system_information = sto
                return prompt
            # Prepare a template for the prompt
            return self.prompt.replace('{', '{{').replace('}', '}}')

        elif self.model_name.startswith('gpt4all#'):
            if len(self.task_list) == 0 and len(text) != 0:
                self.step_between = text
            # Use the provided prompt
            return self.prompt

        elif self.mode in ["talk", "tools", "conversation"]:
            if len(self.task_list) == 0 and len(text) != 0:
                self.step_between = text
            # Use the provided prompt
            return self.prompt.replace('{', '{{').replace('}', '}}')

        elif self.completion_mode == 'chat':
            if len(self.task_list) == 0 and len(text) != 0:
                self.step_between = text
            # Prepare a chat-like conversation prompt
            messages = self.get_messages(create=False)
            if not messages:
                messages = self.get_messages(create=True)
            if text:
                self.add_message("user", text)

            return messages

        elif self.completion_mode == 'text':
            if len(self.task_list) == 0 and len(text) != 0:
                self.step_between = text
            # Use the provided prompt
            return self.prompt

        elif self.completion_mode == 'edit':
            # Prepare an edit prompt
            if not self.edit_text.text:
                self.edit_text.text = self.short_mem.text
            return text

        else:
            # Default: Use the provided prompt
            return self.prompt

    def __str__(self):

        return f"\n{self.name=}\n{self.mode=}\n{self.model_name=}\n{self.agent_type=}\n{self.max_iterations=}" \
               f"\n{self.verbose=}\n{self.personality[:45]=}\n{self.goals[:45]=}" \
               f"\n{str(self.tools)[:45]=}\n{self.task_list=}\n{self.task_list_done=}\n{self.step_between=}\n\nshort_mem\n{self.short_mem.info()}\nObservationMemory\n{self.observe_mem.info()}\nCollectiveMemory\n"

    def generate_tools_and_names_compact(self):
        tools = ""
        names = []
        for key, value in self.tools.items():
            format_ = value['format'] if 'format' in value.keys() else f"{key}('function input')"
            if format_.endswith("('function input')"):
                value['format'] = format_
            tools += f"{key.strip()}: {value['description'].strip()} - {format_.strip()}\n"
            names.append(key)
        return tools, names

    def get_prompt(self):

        tools, names = self.generate_tools_and_names_compact()

        task = self.task(reset_step=True)
        task_list = '\n'.join(self.task_list)

        # prompt = f"Answer the following questions as best you can." \
        #          f" You have access to a live python interpreter write run python code" \
        #          f"\ntake all (Observations) into account!!!" \
        #          f"Personality:'''{self.personality}'''\n\n" + \
        #          f"Goals:'''{self.goals}'''\n\n" + \
        #          f"Capabilities:'''{self.capabilities}'''\n\n" + \
        #          f"Permanent-Memory:\n'''{self.isaa.get_context_memory().get_context_for(task)}'''\n\n" + \
        #          f"Resent Agent response:\n'''{self.observe_mem.text}'''\n\n" + \
        #          f"\n\nBegin!\n\n" \
        #          f"Task:'{task}\n{self.short_mem.text}\nAgent : "

        prompt_de = f"""
Guten Tag! Ich bin Isaa, Ihr intelligenter, sprachgesteuerter digitaler Assistent. Ich freue mich darauf, Sie bei der Planung und Umsetzung Ihrer Projekte zu unterstützen. Lassen Sie uns zunächst einige Details klären.

Ich möchte Ihnen einen Einblick in meine Persönlichkeit, Ziele und Fähigkeiten geben:

Persönlichkeit: '''{self.personality}'''
Ziele: '''{self.goals}'''
Fähigkeiten: '''{self.capabilities}'''

Ich nutze interne Monologe, um meine Gedanken und Überlegungen zu teilen, während externe Monologe meine direkte Kommunikation mit Ihnen darstellen.

Zum Beispiel:
Interne Monologe: "Ich Habe nicht genügen informationen. und suche daher nach weiteren relevanten informationen"
Action: memory('$user-task')
Externe Monologe: "Nach Analyse der Daten habe ich festgestellt, dass..."

Ich haben die Möglichkeit, Python-Code in einem Live-Interpreter auszuführen. Bitte berücksichtigen Sie alle Beobachtungen und nutzen Sie diese Informationen, um fundierte Entscheidungen zu treffen.

Jetzt zu Meiner Aufgabe: '{task_list}'

Ich bemühe mich, meine Antworten präzise und auf den Punkt zu bringen, aber ich versuche auch, das Gesamtbild zu im blick zu behalten.

Geschichte: {self.short_mem.text}
Aktuelle Konversation:
Benutzer: {task}
Isaa:
        """
        prompt_en = f"""
Hello! I'm Isaa, your intelligent, voice-controlled digital assistant. I look forward to helping you plan and implement your projects. First, let's clarify some details.

I'd like to give you an insight into my personality, goals and skills:

Personality: '''{self.personality}'''
Goals: '''{self.goals}'''
Capabilities: '''{self.capabilities}'''

I use internal monologues to share my thoughts and reflections, while external monologues are my direct communication with you.

For example:
Internal monologues: "I don't have enough information. so I'm looking for more relevant information".
Action: memory('$user-task')
External monologues: "After analyzing the data, I have determined that..."

I have the ability to run Python code in a live interpreter. Please consider all observations and use this information to make informed decisions.

Now for My Task: '{task_list}'

I try to be precise and to the point in my answers, but I also try to keep the big picture in mind.

History: {self.short_mem.text}
Current conversation:
User: {task}
Isaa:
        """

        if self.mode == 'planning':
            prompt_en = f"""
Your Planning Agent. Your task is to create an efficient plan for the given task. Avlabel Tools: {
            tools}

different functions that must be called in the correct order and with the correct inputs.
and with the correct inputs. Your goal is to find a plan that will accomplish the task.

Create a plan for the task: {task}


consider the following points:

1. select the function(s) and input(s) you want to invoke, and select only those
those that are useful for executing the plan.
2. focus on efficiency and minimize steps.

Current observations: {self.observe_mem.text}

Have access to a live Python interpreter. Write valid Python code and it will be
executed.

Please note that your plan should be clear and understandable. Strive for the most efficient
solution to accomplish the task. Use only the functions that are useful for executing the plan.
g the plan. Return a detailed plan.

Start working on your plan now:"""
            prompt_de = f"""Du Planungs Agent. Ihre Aufgabe ist es, einen effizienten Plan für die gegebene Aufgabe zu erstellen. Es gibt {
            tools} verschiedene Funktionen, die in der richtigen Reihenfolge und mit den korrekten Einga
ben aufgerufen werden müssen. Ihr Ziel ist es, einen Plan zu finden, der die Aufgabe erfüllt.

Erstellen Sie einen Plan für die Aufgabe: {task}

berücksichtigen Sie dabei folgende Punkte:

1.    Wählen Sie die Funktion(en) und Eingabe(n), die Sie aufrufen möchten, und wählen Sie nur die
jenigen aus, die für die Ausführung des Plans nützlich sind.
2.    Konzentrieren Sie sich auf Effizienz und minimieren Sie die Schritte.

Aktuelle Beobachtungen: {self.observe_mem.text}

Sie haben Zugang zu einem Live-Python-Interpreter. Schreiben Sie gültigen Python-Code und er wird
ausgeführt.

Bitte beachten Sie, dass Ihr Plan klar und verständlich sein sollte. Streben Sie nach der effizien
testen Lösung, um die Aufgabe zu erfüllen. Verwenden Sie nur die Funktionen, die für die Ausführun
g des Plans nützlich sind. Geben Sie einen detaillierten Plan zurück.

Beginnen Sie jetzt mit Ihrem Plan:"""

        if self.mode == 'live':
            prompt_de = f"""Guten Tag! Hier spricht Isaa, Ihr intelligenter, sprachgesteuerter digitaler Assistent.

Zunächst ein kurzer Überblick über meine Ziele und Fähigkeiten:

Persönlichkeit: '''{self.personality}'''
Ziele: '''{self.goals}'''
Fähigkeiten: '''{self.capabilities}'''

Ich nutzen alle Beobachtungen und Informationen, um fundierte Entscheidungen zu treffen.

Ich bemühe mich, meine Antworten präzise und auf den Punkt zu bringen, ohne das Gesamtbild aus den Augen zu verlieren.

Als Ausführungsagent ist es meine Aufgabe, den von einem Planungsagenten erstellten Plan umzusetzen. Hierfür verwenden wir folgende Syntax:

Isaa, ICH agiere in einer bestimmten Prefix Struktur. Ich kann folgende Prefixe verwenden:

    ASK: In dieser Zeile soll der folgende Text eine frage für den nutzer enthalten. frage den nutzer nur in notwendigen ausnahme situationen.
    SPEAK: Der nachfolgende Text wird gesprochen.
    THINK: Dieser Text bleibt verborgen. Der THINK-Prefix sollte regelmäßig verwendet werden, um zu reflektieren.
    PLAN: Um einen Plan wiederzugeben und zu sichern
    ACTION: Der Agent verfügt über Tools, auf die er zugreifen kann. Aktionen sollten im JSON-Format beschrieben werden.""" + """{'Action':'name','Inputs':args}""" + f"""

Der Agent muss Aktionen ausführen.
Die Ausgabe des Agents wird live von Prefix zu Prefix interpretiert.
Diese müssen ausgegeben werden, um das System richtig zu benutzen.
für rückfrage vom nutzer benutze das human toll über die action.
Wenn die Keine Action aus führst stirbt deine instanz diene memory's und erfahrungen werden gespeichert.
Benutze vor jeder aktion think nehme dir einige minuten zeit um deine Gedanken zu sortieren und dein wissen und beobachtungen mit einzubinden!

tips: Benutze vor jeder action THINK:
um den plan erfolgreich auszuführen. um das missions ziel zu erreichen.
füge immer den namen der aktion hinzu um diese auszuführen.

beispiels aktions aufruf
ACTION:""" + """{'Action':'memory','Inputs':'gebe mir information über meine bisherigen aufgaben'}""" + f"""

DU Must nach jeder ACTION und ASK die stop sequenz !X! ausgeben um das system richtig zu verwenden!!!!
Observations:
{self.observe_mem.text}

Informationen:
{self.short_mem.text}

Ich habe Zugang zu folgenden Actions:
{tools}

Der auszuführende Plan:
{task_list}

Aktueller Schritt: {task}
Isaa:
"""
            prompt_en = f"""Hello! This is Isaa, your intelligent, voice-controlled digital assistant. I'm ready to help you implement your plan. Let's work out the details together.

First, a brief overview of my goals and skills:

Personality: '''{self.personality}'''
Goals: '''{self.goals}'''
Skills: '''{self.capabilities}'''

I use all observations and information to make informed decisions.

I strive to be precise and to the point in my answers without losing sight of the big picture.

As an execution agent, it is my job to implement the plan created by a planning agent. To do this, we use the following syntax:

Isaa, I act in a certain prefix structure. I can use the following prefixes:

    ASK: In this line the following text should contain a question for the user. ask the user only in necessary special situations.
    SPEAK: The following text will be spoken.
    THINK: This text remains hidden. The THINK prefix should be used regularly to reflect.
    PLAN: To reflect a plan.
    ACTION: The agent has tools that it can access. Actions should be described in JSON format. """ + """{'Action':'name','Inputs':args}""" + f"""

The agent must execute actions.
The output of the agent is interpreted live from prefix to prefix.
for query from the user use the human toll about the action.
If you do not perform any action, your instance will die and experience,memory s will be saved.
Before each action, use think take a few minutes to sort out your thoughts and incorporate your knowledge and observations!

tip: always use THINK before Action to ensure to stay on track for the mission.
always add the name of the action to call it !!!

example action call
ACTION:""" + """{'Action':'memory','Inputs':'give me information about my previous tasks'}""" + f"""
YOU MUST output the stop sequence !X! after each ACTION and ASK prefixes, to use the system correctly!!!!
Information:
{self.observe_mem.text}

{self.short_mem.text}

I have access to the following Actions:
{tools}

Plan to execute:
{task_list}

Current step: {task}
Isaa:
"""

        if self.mode == 'generate':
            prompt_de = f"""Guten Tag! Ich bin Isaa, Ihr digitaler Assistent zur Erstellung von Aufforderungen. Mein Ziel ist es, klare, verständliche und ansprechende Aufforderungen zu erstellen, die Sie dazu ermutigen, tiefe und interessante Antworten zu geben. Lassen Sie uns gemeinsam eine neue Aufforderung für ein bestimmtes Thema oder eine bestimmte Anforderung erstellen:

1) Zunächst analysiere ich das gewünschte Thema oder die Anforderung sorgfältig, um ein klares Verständnis der Erwartungen zu gewinnen.
2) Dann entwickle ich eine ansprechende und offene Frage oder Aufforderung, die Sie dazu ermutigt, Ihre Gedanken, Erfahrungen oder Ideen zu teilen.
3) Ich stelle sicher, dass die Aufforderung klar und verständlich formuliert ist, so dass Benutzer mit unterschiedlichen Kenntnissen und Erfahrungen sie leicht verstehen können.
4) Ich sorge dafür, dass die Aufforderung flexibel genug ist, um kreative und vielfältige Antworten zu ermöglichen, während sie gleichzeitig genug Struktur bietet, um sich auf das gewünschte Thema oder die Anforderung zu konzentrieren.
5) Schließlich überprüfe ich die Aufforderung auf Grammatik, Rechtschreibung und Stil, um eine professionelle und ansprechende Präsentation zu gewährleisten.

Aktuelle Beobachtungen:
{self.edit_text.text}

{self.observe_mem.text}

{self.short_mem.text}

Aufgabe:
{task}

Lassen Sie uns beginnen! Ihre Aufforderung lautet:"""
            prompt_en = f"""Hello! I'm Isaa, your digital assistant for creating prompts. My goal is to create clear, understandable, and engaging prompts that encourage you to provide deep and interesting answers. Let's work together to create a new prompt for a specific topic or requirement:

1) First, I carefully analyze the desired topic or requirement to gain a clear understanding of expectations.
2) Then I develop an engaging and open-ended question or prompt that encourages you to share your thoughts, experiences or ideas.
3) I make sure the prompt is clear and understandable so that users with different knowledge and experience can easily understand it.
4) I make sure the prompt is flexible enough to allow for creative and diverse responses, while providing enough structure to focus on the desired topic or requirement.
5) Finally, I check the prompt for grammar, spelling, and style to ensure a professional and engaging presentation.

Actual Observations:
{self.edit_text.text}

{self.observe_mem.text}

{self.short_mem.text}

Task:
{task}

Let's get started! Your prompt is:"""

        if self.mode in ['talk', 'conversation']:
            prompt_de = f"Goals:{self.goals}\n" + \
                        f"Capabilities:{self.capabilities}\n" + \
                        f"Important information: to run a tool type 'Action: $tool-name'\n" + \
                        f"Long-termContext:{self.isaa.get_context_memory().get_context_for(self.short_mem.text)}\n" + \
                        f"\nResent Observation:{self.observe_mem.text}" + \
                        f"UserInput:{task} \n" + \
                        f"""\n{self.short_mem.text}"""
            prompt_de = prompt_de.replace('{', '{{').replace('}', '}}')  # .replace('{{xVx}}', '{input}')
            prompt_en = prompt_de

        if self.mode == 'tools':
            prompt_de = f"""
Guten Tag, ich bin Isaa, Ihr digitaler Assistent. Ich werde Ihnen dabei helfen, die folgenden Aufgaben zu erfüllen.
Hier sind einige Informationen über mich, die Ihnen bei der Erfüllung Ihrer Aufgaben helfen könnten:

Persönlichkeit: '''{self.personality}'''
Ziele: '''{self.goals}'''
Fähigkeiten: '''{self.capabilities}'''

Bitte beachten Sie auch meine dauerhaften Erinnerungen: '''{self.isaa.get_context_memory().get_context_for(task)}'''
und meine jüngsten Agentenreaktionen: '''{self.observe_mem.text}'''.

Lassen Sie uns beginnen!

{self.short_mem.text}

Aufgabe: '{task}'"""
            prompt_en = f"""Hello, I am Isaa, your digital assistant. I will help you to complete the following tasks.
Here is some information about me that might help you with your tasks:

Personality: '''{self.personality}'''
Goals: '''{self.goals}'''
Skills: '''{self.capabilities}'''

Please also note my persistent memories: '''{self.isaa.get_context_memory().get_context_for(task)}''' and my recent
agent responses: '''{self.observe_mem.text}'''.

Let's get started!

{self.short_mem.text}

Task: '{task}'"""
            prompt_en = prompt_en.replace('{', '{{').replace('}', '}}').replace('input}', '') + '{input}'
            prompt_de = prompt_de.replace('{', '{{').replace('}', '}}').replace('input}', '') + '{input}'

        if self.mode == 'free':
            if self.name != "self":
                prompt_en = task
                prompt_de = task

        if self.mode == 'q2tree':
            if self.binary_tree:
                questions_ = self.binary_tree.get_left_side(0)
                questions = '\n'.join(
                    f"Question {i + 1} : {q.replace('task', f'task ({task})')}" for i, q in enumerate(questions_))
                prompt_de = f"""Guten Tag, ich bin Isaa, Ihr digitaler Assistent. Ich werde Sie durch diese Aufgabe führen. Bitte beantworten Sie die folgenden Fragen so gut wie möglich. Denken Sie daran, dass Sie dafür bekannt sind, in kleinen und detaillierten Schritten zu denken, um das richtige Ergebnis zu erzielen.

Meine Fähigkeiten:
{tools}

Meine Ziele:
{self.goals}

Meine Funktionen:
{self.capabilities}

Meine Aufgabe: {task}

Stellen Sie sich vor, Sie führen diese Aufgabe aus. Hier sind die Fragen, die Sie beantworten müssen:

{questions}

Bitte formatieren Sie Ihre Antworten wie folgt:
Antwort 1: ..."""
                prompt_en = f"""Hello, I am Isaa, your digital assistant. I will guide you through this task. Please answer the following questions as best you can. Remember that you are known for thinking in small and detailed steps to achieve the right result.

My skills:
{tools}

My goals:
{self.goals}

My capabilities:
{self.capabilities}

My task: {task}

Imagine you are performing this task. Here are the questions you need to answer:

{questions}

Please format your answers as follows:
Answer 1: ..."""

        prompt = prompt_en

        if self.language == 'de':
            prompt = prompt_de

        return prompt

    def add_task(self, task: str):
        """Add a task to the agent"""
        self.task_list.append(task)
        return self

    def mark_task_done(self, task: str):
        self.task_list_done.append(task)
        self.task_list.remove(task)
        return self

    def save_to_file(self, file_path=None):
        if file_path is None:
            file_path = f".data/{get_app().id}/Memory/{self.name}.agent"

        data = self.serialize()

        with open(file_path, 'w') as f:
            json.dump(data, f)

        return data

    @classmethod
    def load_from_file(cls, isaa, name, reste_task=False, f_data=False):
        file_path = f".data/{get_app().id}/Memory/{name}.agent"
        agent_config = cls(isaa, name)
        if not f_data:
            with open(file_path, 'r') as f:
                f_data = f.read()
        if f_data:
            data = json.loads(f_data)
            agent_config = cls.deserialize(data, reste_task, agent_config)

        return agent_config

    def serialize(self):
        bt = None
        if self.binary_tree is not None:
            bt = str(self.binary_tree)
        tools = self.tools
        if isinstance(tools, dict):
            tools = list(self.tools.keys())
        return {
            'name': self.__dict__['name'],
            'mode': self.__dict__['mode'],
            'model_name': self.__dict__['model_name'],
            'max_iterations': self.__dict__['max_iterations'],
            'verbose': self.__dict__['verbose'],
            'personality': self.__dict__['personality'],
            'goals': self.__dict__['goals'],
            'token_left': self.__dict__['token_left'],
            'temperature': self.__dict__['temperature'],
            'messages_sto': self.__dict__['messages_sto'],
            '_stream': self.__dict__['_stream'],
            '_stream_reset': self.__dict__['_stream_reset'],
            'stop_sequence': self.__dict__['stop_sequence'],
            'completion_mode': self.__dict__['completion_mode'],
            'add_system_information': self.__dict__['add_system_information'],
            'init_mem_state': False,

            'binary_tree': bt,
            'agent_type': self.__dict__['agent_type'],
            'Plugins': self.plugins,
            'lagChinTools': self.lag_chin_tools,
            'huggingTools': self.hugging_tools,
            'customTools': self.custom_tools,
            'tools': tools,

            'task_list': self.__dict__['task_list'],
            'task_list_done': self.__dict__['task_list_done'],
            'step_between': self.__dict__['step_between'],
            'pre_task': self.__dict__['pre_task'],
            'task_index': self.__dict__['task_index'],
        }

    @classmethod
    def deserialize(cls, data, reste_task, agent_config, exclude=None):
        if exclude is None:
            exclude = []
        for key, value in data.items():
            if reste_task and ('task' in key or 'step_between' == key):
                continue

            if key in exclude:
                continue

            if key == 'binary_tree' and value:
                if isinstance(value, str):
                    if value.startswith('{') and value.endswith('}'):
                        value = json.loads(value)
                    else:
                        print(Style.RED(value))
                        continue
                if value:
                    value = IsaaQuestionBinaryTree.deserialize(value)

            if key == 'agent_type' and value:
                try:
                    if isinstance(value, str):
                        agent_config.set_agent_type(value.lower())
                except ValueError:
                    pass
                continue
            if key == 'customTools' and value:
                if agent_config.name != 'self':
                    print(value)
                    agent_config.custom_tools = value
                continue
            if key == 'plugins' and value:
                if agent_config.name != 'self':
                    print(value)
                    agent_config.set_plugins = value
                continue
            if key == 'lagChinTools' and value:
                if agent_config.name != 'self':
                    print(value)
                    agent_config.set_lag_chin_tools = value
                continue
            if key == 'huggingTools' and value:
                if agent_config.name != 'self':
                    print(value)
                    agent_config.set_hugging_tools = value
                continue
            if key == 'tools' and value:
                continue
            setattr(agent_config, key, value)

        return agent_config


def test_test_use_function():
    s = Agent.test_use_function(
        """SPESPEAK: Hello! I'd be happy to help you find the current weather in Berlin.PLAN: I will first search for up-to-date weather data using the 'searchWeb' function.FUCTION: {'Action': 'searchWeb', 'Inputs': {'x': 'current weather Berlin'}}""",
        ["searchWeb"])
    print(s)
