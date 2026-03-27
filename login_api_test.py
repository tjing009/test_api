import pytest
import requests

url = 'http://test.club'

def post_data(url,payload):
    response = requests.post(url, data=payload)
    return response

#断言封装
def assert_response(response,expected_msg_part):
     assert response.status_code == 200,f"请求状态码错误：{response.status_code}"

     #解析json
     try:
         response_json = response.json()
     except:
         assert False,"响应不是有效json"
     # assert response_json.get("code") == expected_code,f"业务错误，期望{expected_code},返回{response_json.get('code')}"
     assert expected_msg_part in response_json.get("msg"),f"msg 不包含{expected_msg_part},实际为{response_json.get('msg')}"

@pytest.mark.parametrize(
    'userName,passWord,expected_msg_part',
    [
        ('123456', 'youma6688@','成功'),
        ('null','youma6688@','失败'),
        ('1234567', 'youma6688@','失败'),
        ('123456', 'null','失败'),
        ('123456', 'youma6688','失败'),
        ('null', 'null','失败'),
    ],
    ids=["正确数据","空账号","账号错误","空密码","密码错误","空参"]
)

def test_login(userName,passWord,expected_msg_part):
    payload = {'userName':userName,'passWord':passWord}
    response = post_data(url,payload)

    print(f"\n【请求】{payload}")
    print(f"【响应】{response.text}")
    print(f"【解析后】{response.json()}")
    assert_response(response,expected_msg_part)



