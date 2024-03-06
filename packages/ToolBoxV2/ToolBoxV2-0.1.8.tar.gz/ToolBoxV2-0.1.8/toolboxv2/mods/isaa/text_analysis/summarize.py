
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.llms.base import BaseLLM
from litellm.llms.base import *
# from langchain_openai import ChatOpenAI

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

# llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
# chain = load_summarize_chain(llm, chain_type="stuff")

# chain.run(docs)
