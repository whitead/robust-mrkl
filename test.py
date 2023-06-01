import langchain
from langchain import agents
from rmrkl import ChatZeroShotAgent, RetryAgentExecutor


sllm = langchain.chat_models.ChatOpenAI(
    temperature=0.1,
    model_name='gpt-3.5-turbo',
    request_timeout=1000,
    max_tokens=2000
)

llm = langchain.chat_models.ChatOpenAI(
    temperature=0.1,
    model_name='gpt-4',
    request_timeout=1000,
    max_tokens=2000
)


tools = agents.load_tools(['python_repl'], sllm)

agent = RetryAgentExecutor.from_agent_and_tools(
    tools=tools,
    agent=ChatZeroShotAgent.from_llm_and_tools(
        llm,
        tools,
        prefix="You are a witty AI system that follows instructions but talks in a funny way, using words like Dang!, Mate, and holy molly, whenever you can."),
    verbose=True,
)
agent.run("What is two plus two minus one times 11. Do it step by step.")

