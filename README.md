# robust-mrkl

A [langchain](https://github.com/hwchase17/langchain) agent that retries and utilizes a system prompt

## Install

```sh
pip install rmrkl
```

## Usage

```py
from rmrkl import ChatZeroShotAgent, RetryAgentExecutor

tools = ...
llm = ..

agent = RetryAgentExecutor.from_agent_and_tools(
    tools=tools,
    agent=ChatZeroShotAgent.from_llm_and_tools(llm, tools),
    verbose=True,
)
agent.run(...)

```
