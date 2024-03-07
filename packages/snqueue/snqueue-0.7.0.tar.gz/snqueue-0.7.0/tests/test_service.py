import asyncio
import concurrent.futures
import time

from concurrent.futures import Future, ThreadPoolExecutor
from pydantic import BaseModel
from threading import Thread

from tests.settings import settings

from snqueue.service import (
  SnQueueRequest,
  SnQueueResponse,
  SnQueueServer,
  SqsVirtualQueueClient,
)
from snqueue.service.helper import (
  dev_info,
  parse_response,
  SqsConfig,
)

class Task(BaseModel):
  id: int
  processing_time: int

def back_service_fn(
    req: SnQueueRequest,
    res: SnQueueResponse
) -> None:
  try:
    dev_info(f"Request received for back service:\n{req.data}")

    request_metadata = req.attributes.get("SnQueueRequestMetadata")
    response_topic_arn = request_metadata.get('ResponseTopicArn')

    task = Task.model_validate(req.data)
    time.sleep(task.processing_time)

    res.status(200).send(response_topic_arn, data=task.model_dump())

  except Exception as e:
    req.app.logger.exception(e)

    if response_topic_arn:
      res.status(500).send(response_topic_arn, data=str(e))

  finally:
    ...

async def _front_service_fn(
    req: SnQueueRequest,
    res: SnQueueResponse
) -> None:
  try:
    req.app.logger.info(f"Request received for front service:\n{req.data}")

    request_metadata = req.attributes.get("SnQueueRequestMetadata")
    response_topic_arn = request_metadata.get('ResponseTopicArn')

    task = Task.model_validate(req.data)

    async with SqsVirtualQueueClient(
      settings.RESPONSE_SQS_URL,
      settings.AWS_PROFILE_NAME
    ) as client:
      response = await client.request(
        settings.BACK_SERVICE_TOPIC_ARN,
        task.model_dump(),
        response_topic_arn=settings.RESPONSE_TOPIC_ARN,
        timeout=15
      )

    status_code, message, _ = parse_response(response)

    req.app.logger.info(f"Response received from back service:\nstatus code: {status_code}; message: {message}")

    if not status_code == 200:
      req.app.logger.error({
        'error_code': status_code,
        'error_message': message
      })
      res.status(status_code).send(
        response_topic_arn, data=message
      )
    else:
      res.status(200).send(response_topic_arn, data=task.model_dump())
    
  except TimeoutError as e:
    if response_topic_arn:
      res.status(408).send(response_topic_arn, data=str(e))

  except Exception as e:
    req.app.logger.exception(e)

    if response_topic_arn:
      res.status(500).send(response_topic_arn, data=str(e))

  finally:
    ...

def front_service_fn(
    req: SnQueueRequest,
    res: SnQueueResponse
) -> None:
  dev_info(f"Request received for front service:\n{req.data}")
  asyncio.run(_front_service_fn(req, res))

def setup_server() -> SnQueueServer:
  server = SnQueueServer(
    settings.AWS_PROFILE_NAME,
    sqs_config=SqsConfig(WaitTimeSeconds=1)
  )

  server.use(settings.BACK_SERVICE_SQS_URL, back_service_fn)
  server.use(settings.FRONT_SERVICE_SQS_URL, front_service_fn)

  return server

async def on_task_arrival(task: Task) -> bool:
  async with SqsVirtualQueueClient(
    settings.RESPONSE_SQS_URL,
    settings.AWS_PROFILE_NAME
  ) as client:
    response = await client.request(
      settings.FRONT_SERVICE_TOPIC_ARN,
      data=task.model_dump(),
      response_topic_arn=settings.RESPONSE_TOPIC_ARN
    )

  status_code = parse_response(response)[0]
  dev_info(f"{task} is done with status code {status_code}.")

  return True if status_code == 200 else False

def simulate_task_arrivals(
    tasks: list[Task],
    interval: int
) -> list[bool]:
  futures: list[Future] = []

  with ThreadPoolExecutor() as executor:
    for task in tasks:
      dev_info(f"Task arrived: {task}")
      future = executor.submit(asyncio.run, on_task_arrival(task))
      futures.append(future)
      time.sleep(interval)

  results = []

  for future in concurrent.futures.as_completed(futures):
    results.append(future.result())

  return results

def test():
  server = setup_server()
  thread = Thread(target=server.start)
  thread.start()

  tasks = []

  for i in range(30):
    tasks.append(Task(id=i, processing_time=1 if i%2==0 else 20))

  results = simulate_task_arrivals(tasks, 3)
  dev_info(results)

  server.shutdown()

  assert True

if __name__ == '__main__':
  test()