from typing import Dict, List, Tuple, Union

from langchain.agents import AgentExecutor
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.tools import BaseTool


class ExceptionTool(BaseTool):
    name = "_Exception"
    description = "Exception tool"

    def _run(self, query: str) -> str:
        return query

    async def _arun(self, query: str) -> str:
        return query


class RetryAgentExecutor(AgentExecutor):
    """Agent executor that retries on output parser exceptions."""

    def _take_next_step(
        self,
        name_to_tool_map: Dict[str, BaseTool],
        color_mapping: Dict[str, str],
        inputs: Dict[str, str],
        intermediate_steps: List[Tuple[AgentAction, str]],
    ) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]:
        try:
            return super()._take_next_step(
                name_to_tool_map, color_mapping, inputs, intermediate_steps
            )
        except OutputParserException as e:
            # ok, this isn't great - I agree
            # but not sure of a more clean way to get this
            text = str(e).split("`")[1]
            observation = "Invalid or incomplete response"
            agent_action = AgentAction("_Exception", observation, text)
            self.callback_manager.on_agent_action(
                agent_action, verbose=self.verbose, color="red"
            )
            tool_run_kwargs = self.agent.tool_run_logging_kwargs()
            # trigger run to get bookkeeping on basetool callback manager
            ExceptionTool().run(
                observation, verbose=self.verbose, color="red", **tool_run_kwargs
            )
            return [(agent_action, observation)]
