import asyncio
import json
import logging
import threading

from datetime import datetime, timezone
from typing import Any, Protocol, Hashable

from snqueue.boto3_clients import SqsClient, SnsClient
from snqueue.service.helper import (
  dev_info,
  to_str,
  SqsConfig
)

logger = logging.getLogger('snqueue.service.client')

class MatchFn(Protocol):
  def __call__(
      self,
      message_id: str,
      raw_sqs_message: dict
  ) -> bool: ...

def default_match_fn(
    message_id: str,
    raw_sqs_message: dict
) -> bool:
  body = json.loads(raw_sqs_message.get('Body', {}))
  attributes = body.get('MessageAttributes', {})
  snqueue_response_metadata = json.loads(attributes.get('SnQueueResponseMetadata', {}).get('Value', ""))
  if not snqueue_response_metadata:
    return False
  
  return message_id == snqueue_response_metadata.get('RequestId')

class ResourceSingleton(type):
  _resource_instances = {}
  _lock = threading.Lock() # for thread safe purpose

  def __call__(cls, resource: Hashable, *args, **kwargs):
    if not isinstance(resource, Hashable):
      raise TypeError("Invalid arguments: `resource` must be hashable.")
    
    if resource not in cls._resource_instances:
      with cls._lock: # expensive operation, that's why need two checks for the instance
        if resource not in cls._resource_instances:
          cls._resource_instances[resource] = super(ResourceSingleton, cls).__call__(resource, *args, **kwargs)

    return cls._resource_instances[resource]
  
class SqsVirtualQueueClient(metaclass=ResourceSingleton):
  
  def __init__(
      self,
      sqs_url: str,
      aws_profile_name: str,
      sqs_config: SqsConfig = SqsConfig(),
      expiration: int = 3600
  ):
    self._sqs_url = sqs_url
    self._aws_profile_name = aws_profile_name
    self._sqs_args = dict(sqs_config)
    self._expiration = expiration

    self._lock = threading.Lock()

    """
    self._polled: list[dict] = []
    self._processed: list[dict] = []
    self._errored: set = set()
    self._waiting_for: set = set()
    """
    self._polled: list[tuple[dict, datetime]] = []
    self._waiting_for: list[tuple[str, datetime]] = []
    self._errored: list[tuple[str, datetime]] = []


  async def __aenter__(self) -> 'SqsVirtualQueueClient':
    dev_info("On __aenter__:")
    dev_info(f"waiting for: {len(self._waiting_for)}; polled: {len(self._polled)}; errored: {len(self._errored)}.")
    return self

  async def __aexit__(self, *_) -> None:
    dev_info("On __aexit__:")
    dev_info(f"waiting for: {len(self._waiting_for)}; polled: {len(self._polled)}; errored: {len(self._errored)}.")

  @property
  def sqs_url(self) -> str:
    return self._sqs_url

  @property
  def aws_profile_name(self) -> str:
    return self._aws_profile_name
  
  def check_and_clean(self, match_fn: MatchFn) -> None:
    with self._lock:
      # Check self._errored against self._polled
      if len(self._errored) and len(self._polled):
        i = 0
        while i < len(self._errored):
          message_id = self._errored[i][0]
          matched = [j for j in range(len(self._polled)) if match_fn(message_id, self._polled[j][0])]
          if len(matched):
            self._polled = [self._polled[j] for j in range(len(self._polled)) if not j in matched]
            self._errored.pop(i)
          else:
            i += 1
    
      # Expire old items in self._errored, self._waiting_for as well as self._polled
      now = datetime.now(tz=timezone.utc)
      self._errored = [self._errored[i] for i in range(len(self._errored)) if (now - self._errored[i][1]).total_seconds() < self._expiration]
      self._waiting_for = [self._waiting_for[i] for i in range(len(self._waiting_for)) if (now - self._waiting_for[i][1]).total_seconds() < self._expiration]
      self._polled = [self._polled[i] for i in range(len(self._polled)) if (now - self._polled[i][1]).total_seconds() < self._expiration]
    
    """
    if len(self._processed):
      with SqsClient(self.aws_profile_name) as sqs:
        result = sqs.delete_messages(
          self.sqs_url,
          self._processed
        )

      for suc in result['Successful']:
        found = next((x for x in self._processed if x['MessageId'][:80] == suc['Id']), None)
        if found:
          self._processed.remove(found)

      if len(result['Failed']):
        logger.warn(result['Failed'])
    """
    ...

  def poll_messages(self) -> None:
    #if not len(self._waiting_for) and not len(self._errored):
    #  return

    try:
      # check and clean errored requests and processed messages
      #self.check_and_clean(match_fn)
      with SqsClient(self.aws_profile_name) as sqs:
        messages = sqs.pull_messages(self.sqs_url, **self._sqs_args)

      if len(messages):
        with self._lock:
          now = datetime.now(tz=timezone.utc)
          self._polled.extend([(message, now) for message in messages])

        # Delete messages from SQS.
        # Always remove messages from SQS promptly to avoid "traffic jam". 
        with SqsClient(self.aws_profile_name) as sqs:
          result = sqs.delete_messages(
            self.sqs_url,
            messages
          )

        if len(result['Failed']):
          logger.warn(result['Failed'])

    except Exception as e:
      logger.exception(e)

    finally:
      ...
    
  async def get_response(
      self,
      message_id: str,
      match_fn: MatchFn
  ) -> dict:
    with self._lock:
      now = datetime.now(tz=timezone.utc)
      self._waiting_for.append((message_id, now))

    while True:
      self.poll_messages()

      # check and clean queues
      self.check_and_clean(match_fn)

      # check polled messages
      with self._lock:
        matched = [i for i in range(len(self._polled)) if match_fn(message_id, self._polled[i][0])]
      
        if len(matched):
          message = self._polled[matched[0]][0]
          self._waiting_for = [w for w in self._waiting_for if not w[0] == message_id]
          self._polled = [self._polled[i] for i in range(len(self._polled)) if not i in matched]
          return message
        
      await asyncio.sleep(1e-6) # allow switching to other coroutines
  
  async def request(
      self,
      topic_arn: str,
      data: Any,
      response_topic_arn: str = None,
      timeout: int = 600,
      match_fn: MatchFn = default_match_fn,
      **kwargs
  ) -> dict:
    try:
      if response_topic_arn:
        message_attributes = {
          "SnQueueRequestMetadata": {
            "DataType": "String",
            "StringValue": json.dumps({ "ResponseTopicArn": response_topic_arn })
          }
        }
        kwargs['MessageAttributes'] = kwargs.get('MessageAttributes', {}) | message_attributes

      with SnsClient(self.aws_profile_name) as sns:
        res = sns.publish(
          topic_arn,
          to_str(data),
          **kwargs
        )

      r_topic_arn = json.loads(kwargs.get('MessageAttributes', {}).get('SnQueueRequestMetadata', {}).get('StringValue', "{}")).get('ResponseTopicArn')
      if not r_topic_arn:
        # No response_topic_arn, return response from sns.publish immediately
        return res

      message_id = res["MessageId"]

      return await asyncio.wait_for(
        self.get_response(message_id, match_fn), timeout
      )
      
    except Exception as e:
      if message_id:
        with self._lock:
          now = datetime.now(tz=timezone.utc)
          self._errored.append((message_id, now))
          self._waiting_for = [w for w in self._waiting_for if not w[0] == message_id]
      raise e
    
    finally:
      ...