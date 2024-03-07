from pydantic import BaseModel, Field
from typing import Literal
from snqueue.service import SqsVirtualQueueClient
from snqueue.service.helper import (
  parse_message_attributes,
  parse_raw_sqs_message
)

from mediqbox.abc.abc_component import ComponentConfig, InputData, AbstractComponent

class ChatConfig(ComponentConfig):
  aws_profile_name: str
  request_topic_arn: str
  response_topic_arn: str
  response_sqs_url: str

class ChatMessage(BaseModel):
  role: Literal['system', 'user', 'assistant', 'tool']
  content: str

class ResponseFormat(BaseModel):
  type: Literal['text', 'json_object'] = 'text'

class ChatInputData(InputData):
  messages: list[ChatMessage]
  model: Literal['gpt-4-1106-preview', 'gpt-4', 'gpt-3.5-trubo'] = 'gpt-4-1106-preview'
  temperature: float = Field(default=0.0, ge=0.0, le=2.0)
  response_format: ResponseFormat = ResponseFormat()

class Chat(AbstractComponent):

  async def process(self, input_data: ChatInputData) -> str:
    """
    Asynchronous processing method.
    """
    async with SqsVirtualQueueClient(
      self.config.response_sqs_url,
      self.config.aws_profile_name
    ) as client:
      response = await client.request(
        self.config.request_topic_arn,
        input_data.model_dump(),
        response_topic_arn=self.config.response_topic_arn
      )

    res = parse_raw_sqs_message(response)
    res_attr = parse_message_attributes(res.Body.MessageAttributes)
    status_code = res_attr['SnQueueResponseMetadata']['StatusCode']

    if not status_code == 200:
      raise Exception({
        'error_code': status_code,
        'error_message': res.Body.Message
      })
    
    return res.Body.Message
  