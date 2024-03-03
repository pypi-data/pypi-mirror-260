import requests
import json
from .xclass_helpers import render_template, load_template_from_file
from pkg_resources import resource_filename

class ProfileApp:
  __apiKey = None
  isProd = True
  __API_PATH="https://2c1fsxykqc.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"
  __API_PATH_DEV="https://jsfzxuwv3b.execute-api.ap-southeast-1.amazonaws.com/resource/aws-s3/uploader"

  def __init__(self, apiKey, isProd=True):
    self.__apiKey = apiKey
    self.isProd = isProd

  def buildProfile(self, class_name='class_name', **kwargs):
    url = self.__API_PATH if self.isProd else self.__API_PATH_DEV
    headers = {
      'api-key': self.__apiKey,
    }
    data=dict(**kwargs)

    template_file = resource_filename(__name__, "views/profile.mustache")
    mustache_template = load_template_from_file(template_file)

    data["class"] = class_name
    if "education" in data:
      for edu in data["education"]:
        edu["from"] = edu["from_time"]
        edu["to"] = edu["to_time"]
      data["education"] = json.dumps(data["education"])
    if "prizes" in data:
      data["prizes"] = json.dumps(data["prizes"])
    if "links" in data:
      data["links"] = json.dumps(data["links"])
    if "futurePlan" in data:
      data["futurePlan"] = json.dumps(data["futurePlan"])

    rendered_html = render_template(mustache_template, data)

    files = {'file': ('index.html', rendered_html)}
    response = requests.post(url, files=files, data={ 'folderName': 'profile', 'contentType': 'text/html' }, headers=headers)
    result_data = {'path': response.json().get('fileUrl', 'Wrong API key!').replace('s3.ap-southeast-1.amazonaws.com', '')}

    print(result_data)