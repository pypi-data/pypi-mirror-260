import requests
from .xclass_helpers import render_template, load_template_from_file
from pkg_resources import resource_filename

class Output:
    label = 'Output'
    text = ''
    def __init__(self, label):
        self.label = label
class Input:
    lable = 'Input'
    text = ''
    def __init__(self, label):
        self.lable = label
    def value(self):
        return 1
    
class GeneralApp:
    __apiKey = None
    __API_PATH="https://2c1fsxykqc.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"
    __API_PATH_DEV="https://jsfzxuwv3b.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"

    name='General app'
    description = 'Default description'
    author='Andrew'
    isProd = True
    slug=''
    appLogo= 'https://uploads-ssl.webflow.com/64b02318b9d14ab16e20227a/64b3fda42fdf5ab7222c5a80_logo-xclass.png'
    okButton={
        'text':'Generate',
        'color': '#ea850c',
        'background':'linear-gradient(to bottom right, #ffedd5, #fdba74)',
    }
    resetButton={
        'text':'Reset',
        'color': '#000000',
        'background':'#EFEFEF',
    }
    def __init__(self, api_key, isProd=True):
        self.__apiKey = api_key
        self.isProd = isProd
        self.listInput = []
        self.listOutput = []
    def createInput(self, prompt, type):
        self.listInput.append({
        'id': f'id-input-{len(self.listInput)}',
        'label': prompt,
        'type': type
        })
        return Input(prompt)
    def createOutput(self, prompt):
        self.listOutput.append({
        'id': f'id-output-{len(self.listOutput)}',
        'label': prompt,
        })
        return Output(prompt)
    
    def display(self, output, text):
        return 0
    
    def process_content(self, content):
        if 'xclass_sdk.' in content:
            content = content.replace('xclass_sdk.', '')
            content = content.replace('__file__', '')
        contentFile = {'file': ('general_app.py', content)}
        url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
        response = requests.post(url, files=contentFile, headers={'api-key': self.__apiKey})
        return response.json().get('fileUrl', '')
    
    def process_inputs(self, inputs):
        processed_inputs = [
            {
                **input,
                'isTextArea': input['type'] == 'text-area',
                'isNumber': input['type'] == 'number'
            }
            for input in inputs
        ]
        return processed_inputs

    def upload_logo(self):
        if self.appLogo:
            if self.appLogo.startswith(('http://', 'https://')):
                return self.appLogo
            url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
            logo_files = {'file': ('logo.png', open(self.appLogo, 'rb'))}
            response = requests.post(url, files=logo_files, headers={'api-key': self.__apiKey})
            return response.json().get('fileUrl', '')
        return ""

    def build(self, filePath):
        url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
        headers = {
            'api-key': self.__apiKey,
        }
        appLogo = self.upload_logo()
        
        with open(filePath, 'r', encoding='utf-8') as file:
            content = self.process_content(file.read())
            data = {
                'inputData': self.process_inputs(self.listInput),
                'outputs': self.listOutput,
                'okButton': self.okButton,
                'resetButton': self.resetButton,
                'appName': self.name,
                'description': self.description,
                'appLogo': appLogo,
                'author': self.author,
                'slug': self.slug,
                'filePath': content,
                'browserSdkPath': 'https://app.xclass.edu.vn/prod/general_app.py' if self.isProd else 'https://app.xclass.edu.vn/dev/general_app.py'  
            }
            template_file = resource_filename(__name__, "views/general_app.mustache")
            mustache_template = load_template_from_file(template_file)
            rendered_html = render_template(mustache_template, data)
            files = {'file': ('index.html', rendered_html)}
            response = requests.post(url, files=files, data={ 'folderName': 'general_app', 'contentType': 'text/html' }, headers=headers)
            result_data = {'path': response.json().get('fileUrl', 'Wrong API key!').replace('s3.ap-southeast-1.amazonaws.com', '')}

            print(result_data)
