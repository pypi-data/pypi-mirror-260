"""
Base generator class for all content generators.
"""
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Optional

from langchain.chains import LLMChain
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               SystemMessagePromptTemplate)

from .prompt_helper import PromptHelper


class GenBaseV3(ABC):
    PROMPT_NAME = None

    def __init__(self, llm, lang: Optional[str], verbose: bool = False, logger: Logger = None):
        self.logger = logger
        prompt_helper = PromptHelper()
        self.prompt_info = prompt_helper.get_prompt(self.PROMPT_NAME, lang)
        chat_prompt = ChatPromptTemplate.from_messages([
            self._get_system_prompt(),
            self._get_human_prompt(),
        ])
        self._chain = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=verbose,
        )

    def _get_system_prompt(self):
        return SystemMessagePromptTemplate.from_template(self.prompt_info.system_prompt)

    def _get_human_prompt(self):
        return HumanMessagePromptTemplate.from_template(self.prompt_info.user_prompt)

    @abstractmethod
    def parse_output(self, output: str) -> Any:
        raise NotImplementedError

    def generate_output(self, **kwargs) -> Any:
        output = self._chain.run(**kwargs)
        return self.parse_output(output)
