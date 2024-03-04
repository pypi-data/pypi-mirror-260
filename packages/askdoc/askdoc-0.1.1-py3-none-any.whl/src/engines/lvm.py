"""
Simple wrapper class around GPT API
"""
import sys
import openai
import backoff

from typing import Optional, List
from loguru import logger


logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')


class LVM():
    def __init__(self, model_id: str, messages: List = [], uri: str = None) -> None:
        from dotenv import load_dotenv
        load_dotenv()

        self.client = openai.OpenAI(base_url=uri)
        self.model_id = model_id
        self.messages = messages
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_time=300)
    def __call__(
        self,
        message: str,
        image: str = None,
        max_tokens: int = 4096,
        **kwargs
    ) -> str:

        self._add_usr_msg(message, image)

        completions = self.client.chat.completions.create(
            model=self.model_id,
            messages=self.messages,
            max_tokens=max_tokens,
            **kwargs
        )

        op = completions.choices[0].message.content

        logger.debug(f'Prompts: {message}, output: {op}')
        logger.debug(
            f'Tokens used in generation using {self.model_id}: {completions.usage}')

        self._add_assistant_msg(op)

        self.total_tokens += completions.usage.total_tokens
        self.input_tokens += completions.usage.prompt_tokens
        self.output_tokens += completions.usage.completion_tokens

        return op

    def _add_usr_msg(self, msg: str, img: str = None):

        content = [{'type': 'text', 'text': msg}]
        if img:
            logger.info('Added image to the message')
            content.append({
                'type': 'image_url',
                'image_url': {'url': f"data:image/jpeg;base64,{img}"}
            })

        self.messages.append({
            'role': 'user',
            'content': content
        })

    def _add_assistant_msg(self, msg: str, role: str = 'assistant'):
        self.messages.append({
            'role': role,
            'content': [{'type': 'text', 'text': msg}]
        })
