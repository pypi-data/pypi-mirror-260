import json
from dotenv import load_dotenv
from mediqbox.abc.async2sync import Async2Sync
from mediqbox.gptchat.chat import (
  Chat,
  ChatConfig,
  ChatInputData,
  ChatMessage
)

load_dotenv()

from tests.settings import settings

def test_chat():
  chat = Async2Sync(
    async_component=Chat(
      config=ChatConfig(
        aws_profile_name=settings.AWS_PROFILE_NAME,
        request_topic_arn=settings.GPTCHAT_TOPIC_ARN,
        response_topic_arn=settings.TEST_TOPIC_ARN,
        response_sqs_url=settings.TEST_SQS_URL
  )))

  result = json.loads(chat.process(ChatInputData(
    messages = [ChatMessage(
      role='user',
      content='Hello!'
    )]
  )))

  assert (result.get('choices') and len(result['choices']) and
          result['choices'][0].get('message') and
          result['choices'][0]['message'].get('content'))