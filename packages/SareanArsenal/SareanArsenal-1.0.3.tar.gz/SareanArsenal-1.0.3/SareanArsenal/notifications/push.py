import requests


# 发送 bark 通知
def bark_send(title: str, content: str, pushkey: str):
    """
    发送 bark 通知
    :param title: 通知标题
    :param content: 通知内容
    :param pushkey: 推送key
    :return:  {'status': 'success'} 或 {'status': 'failed'}
    """
    url = 'https://api.day.app/' + pushkey
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    # bark通知将被分组到“FF14”，并且会自动保存
    load = {
        "title": title,
        "body": content,
        "badge": 1,
        "sound": "minuet.caf",
        "icon": "https://huiji-thumb.huijistatic.com/ff14/uploads/thumb/3/33/000030.png/30px-000030.png",
        "group": "FF14",
        "isArchive": 1,
    }
    response = requests.post(url, headers=headers, json=load)
    if response.status_code == 200:
        return {'status': 'success'}
    else:
        return {'status': 'failed', 'error': response.text}


# 发送 pushdeer 通知
def pushdeer_send(title: str, content: str, pushkey: str):
    """
    发送 pushdeer 通知
    :param title: 通知标题
    :param content: 通知内容
    :param pushkey: 推送key
    :return:  {'status': 'success'} 或 {'status': 'failed', 'error': 'error message'}
    """
    postdata = {
        "text": title,
        "desp": content,
        "type": "markdown"
    }
    url = f'https://api2.pushdeer.com/message/push?pushkey={pushkey}'
    response = requests.post(url, data=postdata)
    if response.status_code == 200:
        return {'status': 'success'}
    else:
        return {'status': 'failed', 'error': response.text}


# 发送 serverchan 通知
def serverchan_send(title: str, content: str, pushkey: str):
    """
    发送 serverchan 通知
    :param title: 通知标题
    :param content: 通知内容
    :param pushkey: 推送key
    :return:  {'status': 'success', 'response': 'response message'} 或 {'status': 'failed', 'error': 'error message'}
    """
    url = f'https://sctapi.ftqq.com/{pushkey}.send' + '?title=' + title + '&desp=' + content
    response = requests.get(url)
    if response.status_code == 200:
        return {'status': 'success', 'response': response.text}
    else:
        return {'status': 'failed', 'error': response.text}


def push(title, content,method,pushkey):
    """
    Push推送
    :param title: 通知标题
    :param content: 通知内容
    :param method: 推送方式，可选值有: bark, pushdeer, serverchan
    :param pushkey: 推送key
    :return: 推送结果，如：{'status': 'success'} 或 {'status': 'failed', 'error': 'error message'}
    """
    if method == 'bark':
        return bark_send(title, content, pushkey)
    elif method == 'pushdeer':
        return pushdeer_send(title, content, pushkey)
    elif method == 'serverchan':
        return serverchan_send(title, content, pushkey)
    else:
        return {'status': 'failed', 'error': 'method error!'}
