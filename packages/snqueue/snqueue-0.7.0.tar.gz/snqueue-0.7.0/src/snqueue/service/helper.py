import json
import logging
import numbers

from pydantic import BaseModel, Field, model_validator
from typing import Any, Literal

from snqueue.settings import settings

# config default logging
logging.basicConfig(
  level=logging.INFO,
  format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s"
)

def get_logger(name: str) -> logging.Logger:
  return logging.getLogger(name or 'snqueue.service')

def dev_info(info: Any, logger: logging.Logger = None) -> None:
  if settings.SNQUEUE_ENV == 'dev':
    logger = logger or logging.getLogger()
    logger.info(info)

def convert_attributes(attributes: dict) -> dict:
  msg_attr = {}

  for key, value in attributes.items():
    if isinstance(value, str):
      msg_attr[key] = { "DataType": "String", "StringValue": value }
    elif isinstance(value, numbers.Number):
      msg_attr[key] = { "DataType": "Number", "StringValue": str(value) }
    elif value:
      msg_attr[key] = { "DataType": "String", "StringValue": to_str(value) }
  
  return msg_attr

def to_str(obj: Any) -> str:
  try:
    return json.dumps(
      obj,
      ensure_ascii=False,
      default=str
    ).encode('utf8').decode()
  except:
    return str(obj)

class SqsConfig(BaseModel):
  MaxNumberOfMessages: int = Field(1, ge=1, le=10)
  VisibilityTimeout: int = Field(30, ge=0, le=60*60*12)
  WaitTimeSeconds: int = Field(20, ge=1, le=20) # enforce SQS long polling

class SqsMessageAttribute(BaseModel):
  Type: Literal["String", "Number", "Binary"]
  Value: str

class SqsMessageBody(BaseModel):
  MessageId: str
  TopicArn: str
  Message: str
  Timestamp: str
  MessageAttributes: dict[str, SqsMessageAttribute] = {}

class SqsMessage(BaseModel):
  MessageId: str
  ReceiptHandle: str
  #Body: str # Be carefule, changing the type to SqsMessageBody may cause issues
  Body: SqsMessageBody

  @model_validator(mode='before')
  @classmethod
  def convert_body(cls, data: Any) -> Any:
    if (isinstance(data, dict) and
        data.get('Body') and
        isinstance(data['Body'], str)):
      data['Body'] = json.loads(data['Body'])

    return data

def parse_message_attributes(attributes: dict[str, SqsMessageAttribute]) -> dict:
  result = {}

  for key, value in attributes.items():
    try:
      parsed_value = json.loads(value.Value)
    except:
      parsed_value = value.Value
    result[key] = parsed_value

  return result

def parse_raw_sqs_message(raw_message: dict) -> SqsMessage:
  sqs_message = SqsMessage(**raw_message)
  #sqs_message.Body = SqsMessageBody(**json.loads(sqs_message.Body))
  return sqs_message

def parse_response(response: dict) -> tuple[int, str, dict]:
  res = parse_raw_sqs_message(response)
  attributes = parse_message_attributes(res.Body.MessageAttributes)
  status_code = attributes['SnQueueResponseMetadata']['StatusCode']
  return status_code, res.Body.Message, attributes