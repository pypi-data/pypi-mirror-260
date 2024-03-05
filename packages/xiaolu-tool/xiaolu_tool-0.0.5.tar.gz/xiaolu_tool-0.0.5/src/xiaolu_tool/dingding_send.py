from dataclasses import dataclass
from commonKit import http_post, to_dict
from log import LogFactory
import hashlib
import hmac
import base64
import urllib.parse
import time
from conf import get_ding_param

logger = LogFactory.logger


@dataclass
class Text:
    content: str

    @classmethod
    def of(cls, content):
        return cls(content)


@dataclass
class Link:
    text: str
    title: str
    picUrl: str
    messageUrl: str

    @classmethod
    def of(cls, text, title, picUrl, messageUrl):
        return cls(text, title, picUrl, messageUrl)


@dataclass
class Markdown:
    text: str
    title: str

    @classmethod
    def of(cls, text, title):
        return cls(text, title)


@dataclass
class Btn:
    title: str  # 按钮标题
    actionURL: str  # 跳转链接

    @classmethod
    def of(cls, title, actionURL):
        return cls(title, actionURL)


@dataclass
class ActionCard:
    title: str
    text: str
    singleTitle: str = None  # 单个按钮的标题。设置此项和singleURL后 btns无效
    singleURL: str = None  # 点击消息跳转的URL
    btnOrientation: str = None  # 0：按钮竖直排列 1：按钮横向排列
    btns: list[Btn] = None


@dataclass
class FeedCard:
    links: list[Link]


@dataclass
class At:
    atMobiles: list[str] = None
    atUserIds: list[str] = None
    isAtAll: bool = False


@dataclass
class SendBody:
    msgtype: str
    text: Text = None
    link: Link = None
    markdown: Markdown = None
    actionCard: ActionCard = None
    feedCard: FeedCard = None
    at: At = None


def hmac_sha256_sign(secret: str, timestamp: str):
    string_to_sign = timestamp + "\n" + secret
    key = secret.encode('utf-8')
    data = string_to_sign.encode('utf-8')

    # 使用HmacSHA256计算签名
    signature = hmac.new(key, data, hashlib.sha256).digest()

    # 使用Base64编码签名
    base64_signature = base64.b64encode(signature).decode('utf-8')

    # 对签名进行URL编码
    url_encoded_signature = urllib.parse.quote(base64_signature, safe='')
    return url_encoded_signature


# 自定义机器人发送
def send_to_customize_robot(body: SendBody, secret: str, webhook: str):
    timestamp = str(int(time.time() * 1000))
    url = webhook + "&timestamp=" + timestamp + "&sign=" + hmac_sha256_sign(secret, timestamp)
    response = http_post(url, json_body=to_dict(body))
    logger.info(f"send to customize robot response = {response}")


# 默认发送到singleflush数据导出群
def send_to_default_robot(body: SendBody):
    param = get_ding_param()
    send_to_customize_robot(body, param['secret'], param['webhook'])


def build_link_body_then_send_to_default(text: str, title: str, messageUrl: str):
    send_link = Link(text, title, None, messageUrl)
    send_body = SendBody("link", link=send_link)
    send_to_default_robot(send_body)


# 构建链接body
def build_link_body(text: str, title: str, messageUrl: str):
    send_link = Link(text, title, None, messageUrl)
    return SendBody("link", link=send_link)


def build_send_body_by_action_card(action_card: ActionCard):
    return SendBody(msgtype="actionCard", actionCard=action_card)


if __name__ == "__main__":
    try:
        build_link_body_then_send_to_default("bugclose", "1111", "https://www.bugclose.com/console.html")
    except Exception:
        logger.warning("error -> ", exc_info=True)
    logger.info("finished")
    exit(0)
