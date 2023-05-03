from rmrkl import ChatZeroShotAgent, RetryAgentExecutor
from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools


def test_agent_init():
    tools = load_tools(["terminal"])
    responses = [
        "I should use the REPL tool",
        "Action: Python REPL\nAction Input: print(2 + 2)",
        "Final Answer: 4",
    ]
    llm = FakeListLLM(responses=responses)

    agent = RetryAgentExecutor.from_agent_and_tools(
        tools=tools,
        agent=ChatZeroShotAgent.from_llm_and_tools(llm, tools),
        verbose=True,
    )
    agent.run("What is 2 + 2")
