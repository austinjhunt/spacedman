import requests 
from django.conf import settings 
from .models import * 
import json 
def testPostRequestWithKey(): 
    context = {
        'RENDER_QUESTION_ENDPOINT': settings.RENDER_QUESTION_ENDPOINT,
        'CREATE_QUESTION_ENDPOINT': settings.CREATE_QUESTION_ENDPOINT,
        'GET_ANSWER_ENDPOINT': settings.GET_ANSWER_ENDPOINT,
        'CHECK_ANSWER_ENDPOINT': settings.CHECK_ANSWER_ENDPOINT,
    }

    body = "{\"question_template\": \"What is the {{my_len}}-bit 2's complement binary representation of the decimal {{my_num}}?\", \"answer_template\": \"{{ans}}\", \"subject_area\": \"number_systems\", \"code\": \"from random import *\\nmy_len= randint(4,8)\\nmy_num = randint(-10,10)\\n\\nif my_num >= 0:\\n\\tmy_bin=bin(my_num).split('0b')[1]\\n\\twhile len(my_bin) < my_len:\\n\\t\\tmy_bin = '0' + my_bin\\nelse:\\n\\tmy_bin = -1 * my_num\\n\\tmy_bin = bin(my_bin - pow(2, my_len)).split('0b')[1]\", \"code_context\": \"{'my_len': my_len,'my_num': my_num, 'ans': my_bin}\", \"apikey\": \"randompostapikeyforaustinhuntuser\"}"
    body = json.loads(body)
    api_key = User.objects.get(username="huntaj").profile.cud_api_key
    body['apikey'] = api_key
    headers = {'X-Api-Key': api_key}
    response = requests.post(context['CREATE_QUESTION_ENDPOINT'], headers=headers,json=body)
    return response

def testPostRequestWithoutKey():
    context = {
        'RENDER_QUESTION_ENDPOINT': settings.RENDER_QUESTION_ENDPOINT,
        'CREATE_QUESTION_ENDPOINT': settings.CREATE_QUESTION_ENDPOINT,
        'GET_ANSWER_ENDPOINT': settings.GET_ANSWER_ENDPOINT,
        'CHECK_ANSWER_ENDPOINT': settings.CHECK_ANSWER_ENDPOINT,
    }

    body = "{\"question_template\": \"What is the {{my_len}}-bit 2's complement binary representation of the decimal {{my_num}}?\", \"answer_template\": \"{{ans}}\", \"subject_area\": \"number_systems\", \"code\": \"from random import *\\nmy_len= randint(4,8)\\nmy_num = randint(-10,10)\\n\\nif my_num >= 0:\\n\\tmy_bin=bin(my_num).split('0b')[1]\\n\\twhile len(my_bin) < my_len:\\n\\t\\tmy_bin = '0' + my_bin\\nelse:\\n\\tmy_bin = -1 * my_num\\n\\tmy_bin = bin(my_bin - pow(2, my_len)).split('0b')[1]\", \"code_context\": \"{'my_len': my_len,'my_num': my_num, 'ans': my_bin}\", \"apikey\": \"randompostapikeyforaustinhuntuser\"}"
    body = json.loads(body)
    api_key = User.objects.get(username="huntaj").profile.cud_api_key
    body['apikey'] = api_key 
    response = requests.post(context['CREATE_QUESTION_ENDPOINT'],json=body)
    print(response.headers)
    return response

""" Successful response headers 
{'Content-Type': 'application/json', 
'Content-Length': '81', 'Connection': 
'keep-alive', 'Date': 'Tue, 23 Mar 2021 01:39:06 GMT', 
'x-amzn-RequestId': 'dca785f8-0a3a-4082-9da9-1de7a79dd1e8', 
'Access-Control-Allow-Origin': '*', 
'Access-Control-Allow-Headers': 
'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token', 
'x-amz-apigw-id': 'cnf9FHEToAMFxUg=', 
'X-Amzn-Trace-Id': 'Root=1-605946ba-5224230e107a00517ce8af30;Sampled=0', 
'Access-Control-Allow-Credentials': 'true', 'X-Cache': 'Miss from cloudfront',
 'Via': '1.1 b5e84d5e033cdf1a3129ccc858468a28.cloudfront.net (CloudFront)',
  'X-Amz-Cf-Pop': 'ATL56-C3', 'X-Amz-Cf-Id': 
  '1VlOMwNlBY4FmSjo_0R3TArJt7odGp0AijClX8saGaxuefMR22KoHA=='}

  Successful request headers
  {'User-Agent': 'python-requests/2.25.1', 
  'Accept-Encoding': 'gzip, deflate', 
  'Accept': '*/*', 
  'Connection': 'keep-alive', 
  'X-Api-Key': 'J1FZi6NJ3kZSL88S90PVrL69g86W648UJ3FN464X0SvupS2U323NLpNr75oLSPxN88854Xijo6TamoUZ2axNmS2aLo6j0xmap5jk3gF4LnF1Sp4C27Sd0ftrGZnbVkkx', 
  'Content-Length': '672', 
  'Content-Type': 'application/json'} """