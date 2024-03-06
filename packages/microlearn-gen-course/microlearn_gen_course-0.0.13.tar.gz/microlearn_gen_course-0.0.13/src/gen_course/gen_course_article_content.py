"""
Generator for course's article's content.
"""
import json
import logging
from typing import Any, List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .gen_base import GenBase
from .gen_base_v2 import GenBaseV2
from .gen_base_v3 import GenBaseV3


logger = logging.getLogger(__name__)


class CourseArticleModel(BaseModel):
    content: str = Field(description="Article content")
    questions: List[str] = Field(
        description="List of questions related to the article")

    def get_article_content(self) -> str:
        return f"""{self.content}

Questions the reader may be interested in making after reading the article:
1. {self.questions[0]}
2. {self.questions[1]}
3. {self.questions[2]}"""


class CourseArticleWTitleModel(CourseArticleModel):
    title: str = Field(description="Article title")

    def to_plain_text(self):
        result = ""
        result += f"-- Title: {self.title}"
        result += f"\n-- Content: {self.content}"
        result += f"\n-- Questions:"
        for q in self.questions:
            result += f"\n--- {q}"
        return result + "\n"


class GenCourseArticleContent(GenBase):
    """
    Generator class for course's article's content'.
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
---
Write a short article of maximum {content_length_words} for this title: "{article_title}". Do not repeat the title in the article content. Write 3 questions about the article that the reader might be interested in asking after reading the article."""

    def __init__(self, llm, verbose: bool = False):
        super().__init__(llm, verbose)

    def get_output_parser(self):
        return PydanticOutputParser(pydantic_object=CourseArticleModel)

    def generate(self,
                 course_title: str,
                 course_description: str,
                 article_title: str,
                 content_length_words: int = 150,
                 ) -> CourseArticleModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            article_title=article_title,
            content_length_words=content_length_words,
        )


class GenCourseArticleContentUsingPreviousArticles(GenBaseV2):
    """
    Generator class for course's article's content'.
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
---
{previous_articles}
Write a short article of maximum {content_length_words} for this title: "{article_title}". Do not repeat the title in the article content. Do not include previous articles content in the article content. Write 3 questions about the article that the reader might be interested in asking after reading the article.

Strictly output in JSON format. The JSON should have the following format:
{{
   "content": "...",
   "questions": [
      "...",
      "...",
      "..."
   ]
}}"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> CourseArticleModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            article = json.loads(output)
            return CourseArticleModel(**article)
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_title: str,
                 course_description: str,
                 article_title: str,
                 previous_articles: List[str],
                 content_length_words: int = 150,
                 ) -> CourseArticleModel:
        if len(previous_articles) == 0:
            previous_articles_str = ""
        else:
            previous_articles_str = """Following are the previous articles generated in the course delimited by 2 newlines:
---
{articles}
---
"""
            previous_articles_str = previous_articles_str.format(
                articles="\n\n".join(previous_articles))
        self.logger.debug(f"previous_articles_str: {previous_articles_str}")

        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            article_title=article_title,
            previous_articles=previous_articles_str,
            content_length_words=content_length_words,
        )


class GenCourseArticleContentInBatchWPrevArticles(GenBaseV2):
    """
    Generator class for course's article's content in batch using previous articles.
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
{previous_articles_title_list}
---
Write short articles each of maximum {content_length_words} words for the above course for the following titles:
---
{title_list}
---
Do not repeat the title in the article content. Write 3 questions about the article that the reader might be interested in asking after reading the article.
Strictly output in JSON format. The JSON should have the following format:
[
    {{
        "title": "...",
        "content": "...",
        "questions": [
            "...",
            "...",
            "..."
        ]
    }}
]"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> List[CourseArticleWTitleModel]:
        try:
            self.logger.debug(f"Parsing output: {output}")
            articles = json.loads(output)
            return [CourseArticleWTitleModel(**article) for article in articles]
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def _build_str_list(self, str_list: List[str]) -> str:
        res = ""
        for item in str_list:
            res += "- " + item + "\n"
        return res[:-1]

    def generate(self,
                 course_title: str,
                 course_description: str,
                 title_list: List[str],
                 previous_articles_title_list: List[str],
                 content_length_words: int = 150,
                 ) -> List[CourseArticleWTitleModel]:
        if len(previous_articles_title_list) == 0:
            previous_articles_title_list_str = ""
        else:
            previous_articles_title_list_str = """Previously generated titles:\n{titles}"""
            previous_articles_title_list_str = previous_articles_title_list_str.format(
                titles=self._build_str_list(previous_articles_title_list))
        self.logger.debug(
            f"previous_articles_title_list_str: {previous_articles_title_list_str}")
        title_list_str = self._build_str_list(title_list)
        self.logger.debug(
            f"title_list_str: {title_list_str}")

        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            title_list=title_list_str,
            previous_articles_title_list=previous_articles_title_list_str,
            content_length_words=content_length_words,
        )


class GenCourseContentForAllArticles(GenBaseV3):
    """
    Generator class for course's article's content in batch using previous articles.
    """
    PROMPT_NAME = "gen_course_content_for_all_articles"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str) -> List[CourseArticleWTitleModel]:
        try:
            self.logger.debug(f"Parsing output: {output}")
            articles = json.loads(output)
            return [CourseArticleWTitleModel(**article) for article in articles]
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_title: str,
                 course_description: str,
                 articles_count: int = 10,
                 article_title_length_words: int = 8,
                 content_length_words: int = 150,
                 ) -> List[CourseArticleWTitleModel]:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            articles_count=articles_count,
            article_title_length_words=article_title_length_words,
            content_length_words=content_length_words,
        )


class GenCourseContentForAllArticlesCoherently(GenBaseV3):
    PROMPT_NAME = "gen_course_content_coherently"
    
    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)
        self.generator_base = GenCourseContentForAllArticles(llm, lang, verbose)

    def parse_output(self, output: str) -> List[CourseArticleWTitleModel]:
        return self.generator_base.parse_output(output)

    def generate(self,
                 course_title: str,
                 course_description: str,
                 articles_count: int = 10,
                 article_title_length_words: int = 8,
                 content_length_words: int = 150,
                 ) -> List[CourseArticleWTitleModel]:
        article_list = self.generator_base.generate(
            course_title=course_title,
            course_description=course_description,
            articles_count=articles_count,
            article_title_length_words=article_title_length_words,
            content_length_words=content_length_words,
        )

        articles_text = ""
        for i, article in enumerate(article_list, start=1):
            articles_text += f"- Article {i}\n"
            articles_text += article.to_plain_text()
            articles_text += "\n"

        return self.generate_output(
            articles_text=articles_text,
        )
