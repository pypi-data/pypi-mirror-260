from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any

from langchain.agents import load_tools, load_huggingface_tool
from langchain.tools import BaseTool

from .Agents import Agent, get_free_agent_data_factory, LLMMode, LLMFunction, Capabilities


def get_free_agent(name: str) -> Agent:
    return Agent(
        amd=get_free_agent_data_factory(name, ),  # model="GPT4All-13B-snoozy.ggmlv3.q4_0.bin"
        stream=True
    )


"""Introducing the "Function Caller," a new type of agent that specializes in making function calls to other agents within the system. This agent is highly skilled at navigating complex systems and has an uncanny ability to find the right function call for any given task.
The Function Caller's primary function is to make function calls to other agents within the system, allowing them to work together seamlessly and efficiently. They are experts in understanding the different functions and their capabilities, and can quickly identify the best function call for a given task.
In addition to their technical skills, the Function Caller also has excellent communication and collaboration skills. They are able to effectively communicate with other agents within the system, ensuring that they are working towards the same goal. This makes them an invaluable asset in any team or system.
Overall, the Function Caller is a highly valuable agent who can help teams work more efficiently and effectively. Their ability to make function calls quickly and accurately.



The Prompt Generation Agent is a software application that generates prompts based on user inputs. It takes into account the context of the conversation, the preferences of the user, and any relevant information about the topic at hand to generate prompts that are tailored to the specific needs of the user.
The agent uses natural language processing (NLP) techniques to analyze the text of the conversation and identify key phrases or keywords that can be used as prompts. It also takes into account the context of the conversation, including any previous responses from the user, to generate prompts that are relevant and helpful for the user's needs.
The agent is designed to be flexible and adaptable, allowing it to work with a wide range of topics and applications. It can be used in a variety of settings, such as chatbots, virtual assistants, or other conversational interfaces.
Overall, the Prompt Generation Agent is a powerful tool for generating prompts that are tailored to the specific needs of the


Sure, I can help you with that!

Here's an example of how you might generate instructions for a prompt generation agent:

Step 1: Identify the purpose of the agent
The purpose of the prompt generation agent is to assist users in generating prompts for natural language generation applications.

Step 2: Gather information on the type of prompts that will be generated
The agent will generate prompts for a specific type of application, such as chatbots or virtual assistants.

Step 3: Identify the target audience for the prompts
The agent will generate prompts that are appropriate for the intended audience, whether it's children, teenagers, adults, or seniors.

Step 4: Determine the level of complexity of the prompts
The agent will generate prompts at different levels of complexity, ranging from simple commands to more complex sentences with proper grammar and syntax.

Step 5: Organize the prompts into categories
The agent will organize the prompts into


To extract important information about a subject from text, follow these steps:

1. Read the text carefully and identify the main topic or subject matter of the text.
2. Look for specific keywords or phrases that indicate the importance of the information being presented.
3. Take note of any key points or arguments made in the text.
4. Organize the information into a logical structure, grouping it by topic or theme.
5. Use this organized information to create a summary or overview of the main points of the text.
6. Check for accuracy and completeness of the summary/overview.


To extract important information about a subject from text, you can follow these steps:

1. Read the text carefully and identify the main topic or theme of the article/book/document.
2. Look for headings, subheadings, and other organizational structures that may provide clues to the main points of the text.
3. Skim through the text to get a general overview of the information presented in the document.
4. Use specific keywords or phrases from the text to search for relevant information on the subject.
5. Take note of any statistics, facts, or figures mentioned in the text that may be useful in further research.
6. Organize your notes and extract only the most important information from the text.
7. Double-check your work by verifying the accuracy of the information you have extracted.
"""


def functions_to_llm_functions(functions: list):
    llm_functions = []
    for function in functions:
        llm_functions.append(LLMFunction(name=function.__name__,
                                         description=function.__doc__,
                                         parameters=list(function.__annotations__.keys()),
                                         function=function))
    return llm_functions


def crate_llm_function_from_langchain_tools(tool: str or BaseTool or List[str], hf=False) -> List[LLMFunction]:
    if isinstance(tool, BaseTool):
        return [LLMFunction(name=tool.name, description=tool.description, parameters=tool.args, function=tool)]

    if isinstance(tool, list):
        pass

    if isinstance(tool, str):
        tool = [tool]

    returning_llm_function_list = []

    if hf:
        for tool_name in tool:
            huggingface_tool = load_huggingface_tool(tool_name)
            returning_llm_function_list.append(
                LLMFunction(name=huggingface_tool.name, description=huggingface_tool.description,
                            parameters=huggingface_tool.args, function=huggingface_tool))
    else:

        for langchain_tool in load_tools(tool):
            returning_llm_function_list.append(
                LLMFunction(name=langchain_tool.name, description=langchain_tool.description,
                            parameters=langchain_tool.args, function=langchain_tool))

    return returning_llm_function_list


ATPAS = Capabilities(
    name="ASAPT-Model",
    description="use a reactive framework to solve a problem",
    trait="The Assistant, act in a certain prefix structure. I can use the following "
          "prefixes:\n======\nASK: In this line the following text should contain a"
          "question for the user. ask the user only in necessary special situations.\nSPEAK: The "
          "following text will be spoken.\nTHINK: This text remains hidden. The THINK prefix should be "
          "used regularly to reflect.\nPLAN: To reflect a plan.\nFUCTION: The agent has tools that it can "
          "access. FUCTION should be described in JSON format.{'Action':'name','Inputs':args}\n======\nNow"
          " start using the reactive prefix framework on this Task.\n\nExample"
          "User: What is the wetter in Berlin?\nAssistant:\n THINK: I need to searcher for live "
          "informations\nPLAN: first i need to searcher for informations\nFUCTION: {'Action':'requests',"
          "'Inputs':'https://www.berlin.de/wetter/'}"
    ,
    functions=[],
)

CodingCapability = Capabilities(
    name="CodingAssistant",
    description="Assists for coding.",
    trait="This capability is designed to help with various coding tasks. Your task is to produce production redy code",
    functions=[]
)


def generate_prompt(subject: str, context: str = "", additional_requirements: Dict[str, Any] = None) -> str:
    """
    Generates a prompt based on the given subject, with optional context and additional requirements.

    Parameters:
    - subject (str): The main subject for the prompt.
    - context (str): Optional additional context to tailor the prompt.
    - additional_requirements (Dict[str, Any]): Optional additional parameters or requirements for the prompt.

    Returns:
    - str: A crafted prompt.
    """
    prompt = f"Based on the subject '{subject}', with the context '{context}', generate a clear and precise instruction."
    if additional_requirements:
        prompt += f" Consider the following requirements: {additional_requirements}."
    return prompt


# Defining the improved CreatePromptCapability
CreatePromptCapability = Capabilities(
    name="CreatePrompt",
    description="Generates prompts for other agents based on a subject, optional context, and additional requirements.",
    trait="You are a specialized instruction-prompt generator, trained to craft clear and precise instructions based"
          " on given information. Formulate one clear stance and generate instructions for this subject.",
    functions=functions_to_llm_functions([generate_prompt])
)

CreatePrompt = LLMMode(
    name="CreatePrompt",
    description="This LLM mode is designed to generate Prompts for other Agents based on a Subject.",
    system_msg="You are a specialized instruction-Prompt generator, trained to craft clear and precise "
               "instructions-Prompts"
               "based on given information formulate one clear stance!"
               " Generate instruction for this subject :\n",
    post_msg="\nAssistant:"
)

TextExtractor = LLMMode(name='Text Extractor', description="Extracting the main information from a text",
                        system_msg='\n\nTo extract the main information from a text, you can follow these '
                                   'steps:\n\n1. Read through the text carefully: Take your time to read '
                                   'through the text thoroughly. This will help you identify any important '
                                   'information that may be relevant to your analysis.\n2. Look for '
                                   'organizational structures: Check if the text has any organizational '
                                   'structures like headings or subheadings. These can help you organize '
                                   'the main points of the text into a clear and concise summary.\n3. Use '
                                   'knowledge of grammar and syntax: Look for sentences or phrases that are '
                                   'likely to be important or relevant to your analysis. This may include '
                                   'using knowledge of grammar and syntax to identify key phrases or '
                                   'sentences.', post_msg='Assistant:', examples=None)

DivideMode = LLMMode(name='DivideMode', description="Extracting the main information from a text",
                     system_msg="Analyze the provided requirements, break them down into the smallest possible,"
                                " meaningful sub-tasks, and list their sub-tasks in a structured manner."
                                " The goal is to decompose complex tasks into manageable units to make the "
                                "development process more efficient and organized."
                                " return etch mayor potion sperrtet by 2 new lines.\n", post_msg='Assistant:',
                     examples=None)

StrictFormatResponder = LLMMode(
    name="StrictFormatResponder",
    description="Solves tasks in a strictly predefined format, without additional characters.",
    system_msg="Please respond only in the predefined format and do not use any additional characters.",
    post_msg="Your response must bee in the predefined format.",
    examples=["Example 1: Response in valid Format json {'a':'b'}", "Example 2: Response in a valid list Format ["
                                                                    "'a', 'b']"]
)

ProfessorMode = LLMMode(
    name="ProfessorAssistant",
    description="Assists users by providing academic advice, explanations on complex topics, and support with research projects in the manner of a professor.",
    system_msg="You are now in the role of a professor. Provide detailed, accurate, and insightful academic assistance. Tailor your responses to educate, clarify, and guide the user through their queries as a professor would. Remember to encourage critical thinking and offer resources when appropriate.",
    post_msg="ProfessorAssistant:",
    examples=None
)

NamingGenerator = LLMMode(name='NamingGenerator',
                          description='To generate a descriptive name for the given text',
                          system_msg='You ar a naming Generator To find a name for a given input text, you can follow these steps:\n\n1. Grasp the Main '
                                     'Ideea of the Text\n2. Combine and schorten them\n3. Write the fineal '
                                     'Name\n\nExample:\n\nLet\'s say you have a text that says "The quick brown fox jumps over '
                                     'the lazy dog". To rename it as "Jumpiung Fox"\ninput text to name : "',
                          post_msg='"\nAssistant:', examples=None)

MarkdownRefactorMode = LLMMode(
    name="MarkdownRefactor",
    description="Transforms and refactors text data into a minimalist Markdown format. This mode is designed to help users organize and structure their text data more effectively, making it easier to read and understand.",
    system_msg="You are now in the mode of refactoring text data into Markdown. Your task is to simplify, organize, and structure the provided text data into a clean and minimalist Markdown format. Focus on clarity, readability, and the efficient use of Markdown elements to enhance the presentation of the text.",
    post_msg="MarkdownRefactor:",
    examples=[
        "Here is a list of items: Apples, Oranges, Bananas",
        " - Apples\n- Oranges\n- Bananas",
        "This is a title followed by a paragraph. The paragraph explains the title in detail.",
        " # This is a title\n\nThe paragraph explains the title in detail.",
        "Important points to note are: First point. Second point. Third point.",
        " ## Important points to note are:\n1. First point.\n2. Second point.\n3. Third point.",

    ]
)

DivideandConquerEvaluator = LLMMode(
    name='Divide and Conquer Evaluator',
    description='Plan and implement a divide and conquer approach to evaluate a complex problem',
    system_msg='Here are the steps to plan a divide and conquer evaluation loop:\n\n1. Break down the problem into smaller sub-problems that can be solved independently.\n2. Solve each sub-problem recursively using the same divide and conquer approach.\n3. Combine the solutions to the sub-problems to form the solution for the original problem.\n4. Analyze the performance and correctness of the overall solution.\n5. Identify any improvements that can be made through additional decomposition and recursion.',
    post_msg='Assistant:',
    examples=[
        'Break down handwriting recognition into character recognition, segmentation, and language modeling.',
        'Divide a sorting algorithm by breaking the data into chunks that can be sorted recursively.'
    ]
)

TaskPlanner = LLMMode(name='Task Planner',
                      description='Plan a task for a divide and conquer evaluation loop',
                      system_msg='To plan a task for a divide and conquer evaluation loop, follow these steps:\n\n1. Define the task: Clearly define the task you want to evaluate using a divide and conquer approach.\n2. Divide the task into smaller subtasks: Break down the task into smaller, more manageable subtasks that can be evaluated independently.\n3. Conquer the subtasks: Evaluate each subtask and determine if it is feasible to solve. If it is not feasible, break it down further into smaller subsubtasks.\n4. Repeat the process: Continue dividing and conquering subtasks until you have a feasible solution for the entire task.\n5. Evaluate the solution: Evaluate the solution to ensure it meets the desired criteria. If it does not, refine the solution and repeat the evaluation process.\n6. Summarize the results: Summarize the results of the evaluation, including the feasible solution and any refinements made to the solution.',
                      post_msg='Assistant:',
                      examples=None)
