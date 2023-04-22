# flake8: noqa
FORMAT_INSTRUCTIONS = """You are an AI running a loop of actions to answer a question.

Format Instructions:

    Respond with a complete Thought/Action/Action Input format OR a single Final Answer format:

    Thought: (reflect on your progress and decide what to do next)
    Action: (the action name, should be one of [{tool_names}])
    Action Input: (the input string to the action)

    OR

    Final Answer: (the final answer to the original input question)

Tool Descriptions:

{tool_strings}
"""
SUFFIX = """

Question: {input}
{agent_scratchpad}"""
