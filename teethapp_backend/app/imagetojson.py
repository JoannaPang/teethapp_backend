from base64 import b64encode
from json import dumps

def imagetojson(resultpath, ratio):
    ENCODING = 'utf-8'
    with open(resultpath, 'rb') as jpg_file :
        byte_content = jpg_file.read()
    base64_bytes = b64encode(byte_content)
    base64_string = base64_bytes.decode(ENCODING)

    raw_data = {}
    raw_data["name"] = resultpath.split('\\')[len(resultpath.split('\\'))-1]
    raw_data["image_base64_string"] = base64_string
    raw_data["ratio"] = ratio

    json_data = dumps(raw_data, indent=2)
    jsonpath = resultpath.split('.jpg')[0] + '.json'

    with open(jsonpath, 'w') as json_file:
        json_file.write(json_data)

    return jsonpath

def res_json(token):
    raw_data = {}
    raw_data["status"] = "login successfully"
    raw_data["token"] = token
    json_data = dumps(raw_data, indent=2)
    return json_data