import requests
import os
from .xclass_helpers import render_template, load_template_from_file
from pkg_resources import resource_filename

class ChatBotApp:
  __apiKey = None
  __API_PATH="https://2c1fsxykqc.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"
  __API_PATH_DEV="https://jsfzxuwv3b.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"
  name='Chat bot'
  description = 'Default description'
  author='Andrew'
  slug=''
  isProd = True
  greetingMessage="Hello, I'm Chat Bot"
  appLogo= 'https://i.postimg.cc/tT9pn3xQ/class-x-1.png'

  def __init__(self, apiKey, isProd=True):
    self.__apiKey = apiKey
    self.isProd = isProd

  def process_content(self, content):
    if 'xclass_sdk.' in content:
        content = content.replace('xclass_sdk.', '')
        content = content.replace('__file__', '')
    contentFile = {'file': ('chat-bot.py', content)}
    url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
    response = requests.post(url, files=contentFile, data={ 'folderName': f'chat_bot_app/{self.slug}' }, headers={'api-key': self.__apiKey})
    return response.json().get('fileUrl', '')

  def build(self, filePath):
    absPath = os.path.abspath(filePath)
    url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
    headers = {
      'api-key': self.__apiKey,
    }
    with open(absPath, 'r', encoding='utf-8') as file:
            content = self.process_content(file.read())
            data = {
                'filePath': content,
                'appName': self.name,
                'description': self.description,
                'appLogo': self.appLogo,
                'author': self.author,
                'greetingMessage': self.greetingMessage
            }
            template_file = resource_filename(__name__, "views/chat_bot.mustache")
            mustache_template = load_template_from_file(template_file)
            rendered_html = render_template(mustache_template, data)
            files = {'file': ('index.html', rendered_html)}
            response = requests.post(url, files=files, data={ 'folderName': f'chat_bot_app/{self.slug}', 'contentType': 'text/html' }, headers=headers)
            result_data = {'path': response.json().get('fileUrl', 'Wrong API key!').replace('s3.ap-southeast-1.amazonaws.com', '')}

            print(result_data)