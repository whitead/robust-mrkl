from typing import Dict, List, Tuple, Union, Optional

from langchain.agents import AgentExecutor
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForChainRun


class ExceptionTool(BaseTool):
    name = "_Exception"
    description = "Exception tool"

    def _run(self, query: str) -> str:
        return query

    async def _arun(self, query: str) -> str:
        return query


class RetryAgentExecutor(AgentExecutor):
    """Agent executor that retries on output parser exceptions."""
    # for backwards compatibility
    handle_parsing_errors: bool = True
