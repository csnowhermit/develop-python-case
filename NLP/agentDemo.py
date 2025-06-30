import os, sys, time
from glob import glob
import time
from time import strftime
from enum import Enum
import uuid
import traceback
from argparse import ArgumentParser
from tqdm import tqdm
import numpy as np

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
import uvicorn

import openai
import langchain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
# from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import StructuredTool
from langchain.tools import YouTubeSearchTool
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.schema.messages import HumanMessage
from langchain.prompts import MessagesPlaceholder
from config import settings, log
import requests
import re
import tempfile

from config import log
from common.collectUtil import collect
from common.checkUtil import format_input_message


# 初始化app对象
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

KNOWLEDGE_BASE_BASE_URL = settings.knowledge_base.base_url
KNOWLEDGE_BASE_SEARCH_ENDPOINT = "/knowledge_base/search_docs"
KNOWLEDGE_BASE_LIST_KNOWLEDGE_BASES_ENDPOINT = "/knowledge_base/list_knowledge_bases"

youtube_search = YouTubeSearchTool()
dalle_image_generator = DallEAPIWrapper(openai_api_key=my_dalle_key)
search = SerpAPIWrapper(serpapi_api_key=settings.SERP_API_KEY)

class ModelEnum(str, Enum):
    gpt35_turbo = "gpt35_turbo"
    gpt4 = "gpt4"
    
class Item(BaseModel):
    model: ModelEnum
    #


# gpt3.5
llm35 = AzureChatOpenAI(
    openai_api_base="https://psyche.openai.azure.com/",
    openai_api_key="my_openai_api_key",
    openai_api_version="2023-05-15",
    deployment_name="gpt-35-turbo",
    temperature=0,
    # openai_api_key=os.getenv("OPENAI_API_KEY"),
    # openai_api_type="azure"
)


# gpt-4
llm4 = AzureChatOpenAI(
    openai_api_base="https://abcdefg.openai.azure.com/",
    openai_api_key="my_openai_api_key",
    openai_api_version="2023-05-15",
    deployment_name="gpt-4",
    temperature=0,
    # openai_api_key=os.getenv("OPENAI_API_KEY"),
    # openai_api_type="azure"
)

my_llm_dict = {
    ModelEnum.gpt35_turbo: llm35, 
    ModelEnum.gpt4: llm4
}

def is_youtube_url(url):
    # 匹配 YouTube 视频 URL 的正则表达式
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    match = re.match(pattern, url)
    return match

def is_bilibili_video(url):
    pattern = r'^https?://www\.bilibili\.com/video/.*$'
    match = re.match(pattern, url)
    return match

def is_zoom_invite_link(url):
    pattern = r'^https?://.*zoom.us/j/.*'
    match = re.match(pattern, url)
    return match

def classify_url(url):
    if is_zoom_invite_link(url):
        return "zoom_meeting"
    elif is_youtube_url(url):
        return "youtube_video"
    elif is_bilibili_video(url):
        return "bilibili_video"
    else:
        return "webpage"

def display_file(file_path):
    # file_name = os.path.basename(file_path)

    # elements = [
    #     cl.File(
    #         name=file_name,
    #         path=file_path,
    #         display="inline",
    #     ),
    # ]
    
    # #
    # cl.run_sync(cl.Message(
    #     content="点击这里下载文件：", elements=elements
    # ).send())
    
    # return {"file_path": file_path, "file_name": file_name}
    # 读取文件内容
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
    except:
        file_content = ""

    # 生成显示文件内容的 HTML 页面
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>File Display</title>
        </head>
        <body>
            <pre>{file_content}</pre>
            <a href="/download">Download</a>
        </body>
        </html>
    """

    return html_content
    

def knowledge_base_search(query: str, knowledge_base_name: str):
    # knowledge_base_name = cl.user_session.get("knowledge_base_name", "samples")
    payload = {"query": query, "knowledge_base_name": knowledge_base_name,  "top_k": 5, "score_threshold": 0.9}
    response = requests.post(f"{KNOWLEDGE_BASE_BASE_URL}{KNOWLEDGE_BASE_SEARCH_ENDPOINT}", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"query": query, "knowledge_base_name": knowledge_base_name, "answer": "遇到了些小问题，没有成功找到知识。"}

def get_knowledge_base_list(filter: str = None):
    response = requests.get(f"{KNOWLEDGE_BASE_BASE_URL}{KNOWLEDGE_BASE_LIST_KNOWLEDGE_BASES_ENDPOINT}")
    if response.status_code == 200:
        knowledge_base_list = response.json()['data']
        knowledge_base_list = filter_list(knowledge_base_list)
        return {"knowledge_base_list": knowledge_base_list}
    else:
        return {"error": "遇到了些小问题，没有成功获取到知识库列表。"}

# def set_knowledege_base_name(knowledge_base_name: str):
#     cl.user_session.set("knowledge_base_name", knowledge_base_name)
#     return {"knowledge_base_name": knowledge_base_name}

def filter_list(my_list):
    # 创建一个新的空列表用于存放过滤后的结果
    filtered_list = []

    # 这是一个UUID的正则表达式，可以匹配你给出的那种格式的字符串
    pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}-\d+')

    # 遍历列表中的每一个元素
    for item in my_list:
        # 如果这个元素不符合我们的正则表达式，那么就把它加入到我们的新列表中
        if not pattern.match(item):
            filtered_list.append(item)

    return filtered_list

tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="Useful for when you need to quickly find answers about current events or the current state of the world."
    ),
    Tool(
        name="URL Classifier",
        func=classify_url,
        description="Useful for when you need to classify the type of a URL: Zoom meeting link, video link, or website."
    ),
    Tool(
        name="Display File",
        func=display_file,
        description="Useful for when you need to display a file specified by file path and provide a download link to the user."
    ),
    StructuredTool.from_function(
        name="Knowledge Base Search",
        func=knowledge_base_search,
        description="Useful for searching the knowledge base for information on various knowledge base specified by its name."
    ),
    StructuredTool.from_function(
        name="Get Knowledge Base List",
        func=get_knowledge_base_list,
        description="Useful for getting the list of the names of the knowledge bases available for searching, don't provide any argument when calling this tool."
    ),
    # Tool(
    #     name="Set Knowledge Base Name",
    #     func=set_knowledege_base_name,
    #     description="Useful for setting the name of the knowledge base when user requests."
    # ),
    Tool(
        name="YouTube Search",
        func=youtube_search.run,
        description="YouTube Search package searches YouTube videos avoiding using their heavily rate-limited API."
    ),
    # StructuredTool.from_function(
    #     name="Dall-E Image Generator",
    #     func=dalle_image_generator_run,
    #     description="you can generate images from a prompt synthesized using an OpenAI LLM."
    # ),
    # Tool(
    #     name="chat with baichuan",
    #     func=chatwithBaichuan,
    #     description="chat with baichuan"
    # )
]

chat_history = MessagesPlaceholder(variable_name="chat_history")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_chain35 = initialize_agent(
    tools, 
    llm35,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,     # gpt-4下使用STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION默认是英文的，需手动加上“说中文”之类的
    verbose=True, 
    memory=memory,
    agent_kwargs = {
    "memory_prompts": [chat_history],
    "input_variables": ["input", "agent_scratchpad", "chat_history"]}
    )

agent_chain4 = initialize_agent(
    tools, 
    llm4,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,     # gpt-4下使用STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION默认是英文的，需手动加上“说中文”之类的
    verbose=True, 
    memory=memory,
    agent_kwargs = {
    "memory_prompts": [chat_history],
    "input_variables": ["input", "agent_scratchpad", "chat_history"]}
    )

my_agent_dict = {
    ModelEnum.gpt35_turbo: agent_chain35, 
    ModelEnum.gpt4: agent_chain4
}


if __name__ == '__main__':
    # agent_chain = my_agent_dict[ModelEnum.gpt35_turbo]
    
    # from langchain import Prompt
    # prompt = Prompt()
    # default_prompt = prompt.get_default_prompt()
    # print("default_prompt:", type(default_prompt), default_prompt)
    
    from langchain.prompts.chat import ChatPromptTemplate
    from langchain import LLMChain
    from common.history import History
    
    while True:
        chat_history = MessagesPlaceholder(variable_name="chat_history")

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        print("=========================================================================")
        print("chat_history:", type(chat_history), chat_history)
        print("memory:", type(memory), memory)
        print("=========================================================================")
        
        message = input("请输入内容: ")
        
        message = format_input_message(message)
        print("使用PROMPT模板之后的输入: ", message)

        # message =  message + " 请以正确的格式返回结果"
        
        # history = [History(**{"role":"user","content":"我们来玩成语接龙，我先来，生龙活虎"}), 
        #            History(**{"role":"assistant","content":"虎头虎脑"})]
        # chat_prompt = ChatPromptTemplate.from_messages([i.to_msg_tuple() for i in history] + [("human", message)])
        # chain = LLMChain(prompt=chat_prompt, llm=llm35)

        agent_chain = initialize_agent(
            tools, 
            llm35,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,     # gpt-4下使用STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION默认是英文的，需手动加上“说中文”之类的
            verbose=True, 
            memory=memory,
            agent_kwargs = {
            "memory_prompts": [chat_history],
            "input_variables": ["input", "agent_scratchpad", "chat_history"]}
            )
        print("agent_chain: ", type(agent_chain))    # <class 'langchain.agents.agent.AgentExecutor'>
        # for msg_template in agent_chain.agent.llm_chain.prompt.messages:
        #     print("msg_template: ", msg_template)
        #     print()
        
        start_time = time.time()
        output = agent_chain.run(message)
        print("output:", type(output), output)
        print("推理耗时：", time.time() - start_time)
    
    ## 统计init_agent的耗时
    # spend_time_list = []
    # for i in tqdm(range(100000)):
    #     start_time = time.time()
    #     chat_history = MessagesPlaceholder(variable_name="chat_history")

    #     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    #     agent_chain35 = initialize_agent(
    #         tools, 
    #         llm35,
    #         agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,     # gpt-4下使用STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION默认是英文的，需手动加上“说中文”之类的
    #         verbose=True, 
    #         memory=memory,
    #         agent_kwargs = {
    #         "memory_prompts": [chat_history],
    #         "input_variables": ["input", "agent_scratchpad", "chat_history"]}
    #         )
    #     spend_time_list.append(time.time() - start_time)

    # print("平均耗时：", np.mean(spend_time_list))
    # print("耗时标准差：", np.std(spend_time_list))
    # print("最大耗时：", np.max(spend_time_list))
    # print("最小耗时：", np.min(spend_time_list))
    