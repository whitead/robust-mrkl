from __future__ import annotations
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackManager
from .prompts import FORMAT_INSTRUCTIONS, SUFFIX, QUESTION_PROMPT, PREFIX
from langchain.agents.agent import Agent, AgentOutputParser
from typing import Any, Optional, Sequence, List
from langchain.tools import BaseTool
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from .output_parser import ChatZeroShotOutputParser


class ChatZeroShotAgent(ZeroShotAgent):
    """Agent for the MRKL chain."""

    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        question_prompt: str = QUESTION_PROMPT,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        """Create prompt in the style of the zero shot agent.

        Args:
            tools: List of tools the agent will have access to, used to format the
                prompt.
            prefix: String to put before the list of tools.
            suffix: String to put after the list of tools.
            input_variables: List of input variables the final prompt will expect.

        Returns:
            A PromptTemplate with the template assembled from the pieces here.
        """
        tool_strings = "\n".join(
            [f"    {tool.name}: {tool.description}" for tool in tools]
        )
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(
            tool_names=tool_names, tool_strings=tool_strings
        )
        human_prompt = PromptTemplate(
            template=question_prompt,
            input_variables=["input"],
            partial_variables={"tool_strings": tool_strings},
        )
        human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)
        if input_variables is not None:
            suffix_prompt = PromptTemplate(
                template=suffix,
                input_variables=input_variables,
            )
            ai_message_prompt = AIMessagePromptTemplate(prompt=suffix_prompt)
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                '\n\n'.join(
                    [
                        prefix,
                        format_instructions
                    ]
                )
            )
        else:
            ai_message_prompt = AIMessagePromptTemplate.from_template(suffix)
            system_message_prompt = SystemMessagePromptTemplate.from_template(
            '\n\n'.join(
                [
                    prefix,
                    format_instructions
                ]
            )
        )
        # ignore suffix
        return ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt, ai_message_prompt]
        )

    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseChatModel,
        tools: Sequence[BaseTool],
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = ChatZeroShotOutputParser(),
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        question_prompt: str = QUESTION_PROMPT,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)
        prompt = cls.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            format_instructions=format_instructions,
            question_prompt=question_prompt,
            input_variables=input_variables,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser()

 
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )
