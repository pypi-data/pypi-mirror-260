import json
from pydantic import BaseModel, NameEmail

class Email(BaseModel):
  From: NameEmail

email = Email(From='"a@b.com" <a@b.com>')
print(email)
# output
# From=NameEmail(name='a@b.com', email='a@b.com')

obj = json.loads(email.model_dump_json())
print(obj)
# output
# {'From': 'a@b.com <a@b.com>'}

email = Email(From=obj['From'])
# error messages
#
# Traceback (most recent call last):
#  ...
#    email = Email(From=obj['From'])
#            ^^^^^^^^^^^^^^^^^^^^^^^
#  File "/<some_path>/lib/python3.11/site-packages/pydantic/main.py", line 171, in __init__
#    self.__pydantic_validator__.validate_python(data, self_instance=self) pydantic_core._pydantic_core.ValidationError: 1 validation error for Email From
#  value is not a valid email address: The email address is not valid. It must have exactly one @-sign. [type=value_error, input_value='a@b.com <a@b.com>', input_type=str]