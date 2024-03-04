# init env
import logging

import configparser

# 配置日志
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 设置环境变量
API_KEY = config.get('ENVIRONMENT', 'API_KEY')
BASE_URL = config.get('ENVIRONMENT', 'BASE_URL')

# 在包被导入时输出环境变量
# 输出日志消息
logging.info(f"API_KEY: {API_KEY}")
logging.info(f"BASE_URL: {BASE_URL}")

# 继续添加其他初始化的操作
from . import notifications
from . import risingStones
from . import sdoLogin
from . import sqMall

