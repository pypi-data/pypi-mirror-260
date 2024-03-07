#import os
import tempfile

#from email import message_from_string
from snqueue.boto3_clients import S3Client, KmsClient
from snqueue.utils.email import *

from tests.settings import settings

#data_dir = os.path.join(os.path.dirname(__file__), 'data')
#decrypted_email = os.path.join(data_dir, 'gb2312_decrypted')

bucket_name = 'mediq-test'
object_key = 'email-routing/raw/89k0p2bqakgm7gje0ffpquqleiaifbostspq37o1'

def test_decode_gb2312():
  #with open(decrypted_email, 'r') as fp:
  #  content = fp.read()
  
  #content = content.replace('?GB2312?', '?GB18030?')

  #email_message: EmailMessage = message_from_string(
  #  content, _class=EmailMessage, policy=policy.default
  #)
  
  #with tempfile.TemporaryDirectory() as tmpdir:
  #  email = parse_email_message(email_message, tmpdir)

  profile_name = settings.AWS_PROFILE_NAME
  with S3Client(profile_name) as s3, KmsClient(profile_name) as kms:
    with get_s3_email(s3, kms, bucket_name, object_key) as email:
      print(email)
      assert email.From.name == '王清湲'

if __name__ == '__main__':
  test_decode_gb2312()