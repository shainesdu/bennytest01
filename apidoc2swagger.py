import json
import sys


# 定义swagger 数据框架
def apidoc_to_swagger3(apidoc_json):
    swagger = {
        "openapi": "3.0.0",
        "info": {
            "version": "1.0.0",
            "title": "Swagger APIs Document",
            "description": "Swagger APIs Document"
        },
        "paths": {}
    }

    for api in apidoc_json:
        path = api['url']
        method = api['type'].lower()
        if path not in swagger['paths']:
            swagger['paths'][path] = {}
        # apidoc中api的description为空时，统一置为“no description”
        if 'description' not in api:
            api_desc = 'no description'
        else:
            api_desc = api['description']
        # apidoc中api的title为空时，统一置为“no title”
        if 'title' not in api:
            api_title = 'no title'
        else:
            api_title = api['title']

        swagger['paths'][path][method] = {
            "tags": [api['group']],
            "summary": api_title,
            "description": api_desc,
            "parameters": [],
            "responses": {}
        }

        if 'parameter' in api and 'fields' in api['parameter']:
            for param in api['parameter']['fields']['Parameter']:
                # apidoc中api中parameter的type为空时，统一置为“string”
                if 'type' not in param:
                    para_type = 'string'
                else:
                    para_type = param['type']

                swagger_param = {
                    "name": param['field'],
                    "in": "query",
                    "description": param['description'],
                    "required": not param['optional'],
                    "schema": {
                        "type": para_type
                    }
                }
                swagger['paths'][path][method]['parameters'].append(swagger_param)

        if 'success' in api and 'fields' in api['success']:
            for code, responses in api['success']['fields'].items():
                for response in responses:
                    # apidoc中api中响应的type为空时，统一置为“string”
                    if 'type' not in responses:
                        resp_type = 'string'
                    else:
                        resp_type = responses['type']
                    swagger_response = {
                        "description": response['description'],
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": resp_type
                                }
                            }
                        }
                    }
                    swagger['paths'][path][method]['responses'][str(code)] = swagger_response
    return swagger


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#参数是输入的apidoc json文件
input_file = sys.argv[1]
apidoc_json = load_json(input_file)
swagger = apidoc_to_swagger3(apidoc_json)
save_to_json(swagger, "swagger.json")