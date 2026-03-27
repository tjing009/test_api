
import requests
import pytest

url_login = "http://test.manage.douge.club/admin/login"
url_insertGR = 'http://test.manage.douge.club/admin/insertGrayReleased'
url_select ='http://test.manage.douge.club/admin/selectGrayReleased'
url_delete = 'http://test.manage.douge.club/admin/deleteGrayReleased'
payload_login = {"userName":"123456","passWord":"youma6688@"}


#先登录
@pytest.fixture(scope="session")
def login():
    response = requests.post(url_login,payload_login)
    print(response.text)
    try:
        res= response.json()
    except:
        assert False,f"返回格式不正确"

    token =res.get("data", {}).get("token")
    assert token ,f"无法获取到token"
    return token


#封装发送请求函数
def post_insert_gray(token,payload):
    # token = login()
    headers = {
        "content-type": "application/json",
        "x-access-token": token
    }
    response = requests.post(url_insertGR,headers=headers,json=payload)
    return response
#封装查询请求
def post_select_gray(token,payload_a):
    headers = {
        "content-type": "application/json",
        "x-access-token": token
    }
    response = requests.post(url_select,headers=headers,json=payload_a)
    return response
# 删除灰度用户
def post_delete_gray(token,payload_b):
    headers = {
        "content-type": "application/json",
        "x-access-token": token
    }
    response = requests.post(url_delete,headers=headers,json=payload_b)
    return response



#断言新增
def response_assert(response,expected_code,expected_msg):
    assert response.status_code == 200,f"请求状态码错误"

    try:
        res = response.json()
    except:
        assert False,f"返回数据不符合json格式"
    assert res.get("code")==expected_code,f"返回code值错误，实际返回{res.get('code')}"
    assert expected_msg in str(res.get("msg")),f"返回实际为{expected_msg}"

#断言查询
def select_assert(response,expected_msg):
    assert response.status_code == 200,f"请求状态码错误"
    try:
        res = response.json()
    except:
        assert False,f"返回结果非json格式"

    assert expected_msg in str(res.get("msg")),f"实际返回结果为{res.get('msg')}"

# 断言删除：永远不要直接 res.get("msg") 做 in 判断！！！
# → 改为 str(res.get("msg", ""))
def dele_assert(response,expected_msg):
    assert response.status_code == 200,f"请求状态码错误"
    try:
        res = response.json()
    except:
        assert False,f"返回内容非json格式"

    a= res.get("msg")
    assert  expected_msg in str({a}),f"响应错误，实际为{a}"


#新增数据准备
@pytest.mark.parametrize(
    "payload,expected_code,expected_msg",
    [
        # 正常成功添加 brand值为：all、wx、web、app
        ({"brand":"all","grayReleasedId":9,"probability":0,"type":2,"unionId":"0001"},
         0,
         "成功"),
        ({"brand":"wx","grayReleasedId":9,"probability":0,"type":2,"unionId":"0002"},
         0,
         "成功"),
        ({"brand": "web", "grayReleasedId": 9, "probability": 0, "type": 2, "unionId": "0003"},
         0,
         "成功"),
        ({"brand":"app","grayReleasedId":9,"probability":0,"type":2,"unionId":"0004"},
         0,
         "成功"),
        #异常值，brand为空、参数缺失
        ({"brand":"","grayReleasedId":9,"probability":0,"type":2,"unionId":"0005"},
         0,
         "失败"),
        ({"grayReleasedId":9,"probability":0,"type":2,"unionId":"0006"},
         0,
         "失败"),
        #用户ID缺失
        ({"grayReleasedId":9,"probability":0,"type":2,"unionId":""},
         0,
         "失败")
    ],
    ids=["全局all","success_wx","success_web","success_app","brand值为空","brand参数缺失","用户ID不填"]
)



def test_insert_gray(login,payload,expected_code,expected_msg):
    response = post_insert_gray(login,payload)
    print(f"实际请求：{payload}")
    print(f"返回值：{response.text}")

    response_assert(response,expected_code,expected_msg)

#查询数据准备
@pytest.mark.parametrize(
    "payload_a,expected_msg",
    [({"businessName":"newYear","current_page":1,"grayReleasedId": 10,"page_size":8,"probability":0,"type":2},"查询成功"),
    ({"businessName":"official","current_page":1,"grayReleasedId": 9,"page_size":8,"probability":0,"type":2},"查询成功"),
    ({"businessName":"doubleFestivalActiveSendHeadPicture","current_page":1,"grayReleasedId": 11,"page_size":8,"probability":0,"type":2},"查询成功"),
    ({"businessName":"","current_page":1,"grayReleasedId": 9,"page_size":8,"probability":0,"type":2},"查询成功"),
     ],
    ids=["查询新年活动","查询官方活动","查询双节头像活动","活动名为空"]
)

def test_select_gray(login,payload_a,expected_msg):
    response = post_select_gray(login,payload_a)
    print(f"实际请求：{payload_a}")
    print(f"返回值：{response.text}")
    select_assert(response,expected_msg)


# 删除数据准备
@pytest.mark.parametrize(
    "payload_b,expected_msg",
    [({"id":88},"删除成功"),
     ({"id":92},"失败"),
     ({},"失败")
     ],
    ids=["删除成功","删除不存在的id","id参数为空"]
)

def test_dele_gray(login,payload_b,expected_msg):
    response = post_delete_gray(login,payload_b)
    print(f"请求id为：{payload_b.get("id")}")
    print(f"返回结果：{response.text}")
    dele_assert(response,expected_msg)
