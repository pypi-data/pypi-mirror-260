import requests
from .xclass_helpers import render_template, load_template_from_file
from pkg_resources import resource_filename

class MathApp:
    __apiKey = None
    __API_PATH="https://2c1fsxykqc.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"
    __API_PATH_DEV="https://jsfzxuwv3b.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"

    isProd = True

    def __init__(self, api_key):
        self.__apiKey = api_key
        self.listInput = []

    def process_content(self, content):
        if 'xclass_sdk.' in content:
            content = content.replace('xclass_sdk.', '')
            content = content.replace('__file__', '')
        contentFile = {'file': ('general_app.py', content)}
        url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
        response = requests.post(url, files=contentFile, headers={'api-key': self.__apiKey})
        return response.json().get('fileUrl', '')

    def createInput(self, prompt):
        self.listInput.append({
        'id': f'id-{len(self.listInput)}',
        'label': prompt
    })
        return prompt

    def getValue(self, input_id):
        return 1

    def display(self, message, value):
        return 0

    def build(self, filePath):
        url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
        headers = {
            'api-key': self.__apiKey,
        }
        with open(filePath, 'r', encoding='utf-8') as file:
            content = self.process_content(file.read())
            data = {
                'inputs': self.listInput,
                'filePath': content
            }
            template_file = resource_filename(__name__, "views/math_app.mustache")
            mustache_template = load_template_from_file(template_file)
            rendered_html = render_template(mustache_template, data)
            files = {'file': ('index.html', rendered_html)}
            response = requests.post(url, files=files, data={ 'folderName': 'math_app', 'contentType': 'text/html' }, headers=headers)
            result_data = {'path': response.json().get('fileUrl', 'Wrong API key!').replace('s3.ap-southeast-1.amazonaws.com', '')}

            print(result_data)