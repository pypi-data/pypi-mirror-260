import requests

user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
              "Safari/537.36")
def get_areaID(cookies, area_name):
    """
    获取服务器区域ID
    :return: int
    """
    getAreaAndGroupListUrl = "https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/getAreaAndGroupList"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    areaAndGroupList = requests.get(getAreaAndGroupListUrl, headers=headers).json()["data"]
    for area in areaAndGroupList:
        if area["AreaName"] == area_name:
            return area["AreaID"]


def get_characterID(cookies, areaID, character_name,group_name):
    """
    获取角色ID
    :return: str
    """
    getCharacterListUrl = f"https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/getFF14Characters?AreaID={areaID}"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    characterList = requests.get(getCharacterListUrl, headers=headers).json()["data"]
    for character in characterList:
        if character["character_name"] == character_name:
            if character['group_name'] == group_name:
                return str(character["character_id"])


def rs_character_bind(cookies,rs_character,rs_area,group_name):
    """
    绑定石之家角色
    :param cookies: str cookies
    :param rs_character: str 角色名
    :param rs_area: str 大区名
    :param group_name: str 服务器名
    :return: bindResult
    """


    bindUrl = "https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/bindCharacterInfo"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    areaID = get_areaID(cookies, rs_area)
    characterID = get_characterID(cookies, areaID, rs_character,group_name)
    payload = {
        "character_id": characterID,
        "platform": 1,
        "device_id": "IOS20230530",
    }
    bindResult = requests.post(bindUrl, headers=headers, data=payload)
    return bindResult