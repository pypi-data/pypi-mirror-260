from abc import ABCMeta, abstractmethod, ABC

from afeng_tools.weixin_tool.core import weixin_reply_tool
from afeng_tools.weixin_tool.core.model.item.wx_receive_event_models import WeixinEventItem, WeixinSubscribeEventItem
from afeng_tools.weixin_tool.core.model.item.wx_receive_msg_models import WeixinTextMsgItem, WeixinImageMsgItem, \
    WeixinVoiceMsgItem, WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from afeng_tools.weixin_tool.core.response import XmlResponse


class WeixinMsgHandler(metaclass=ABCMeta):

    def __init__(self,
                 msg_model: WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem):
        self.msg_item = msg_model

    def get_service_list(self) -> list[str]:
        """获取app服务列表"""
        return [f'<a href="{href}">{title}</a>' for title, href in self.get_all_service()]

    def handle(self) -> XmlResponse:
        # 查询是否在黑名单中
        if self.is_in_blacklist():
            return self.handle_in_blacklist()
        if isinstance(self.msg_item, WeixinTextMsgItem):
            return self.handle_text_msg()
        elif isinstance(self.msg_item, WeixinEventItem):
            if isinstance(self.msg_item, WeixinSubscribeEventItem):
                if getattr(self.msg_item, 'event') == 'subscribe':
                    return self.handle_subscribe()
                elif getattr(self.msg_item, 'event') == 'unsubscribe':
                    return self.handle_unsubscribe()
        return self._return_no_handle()

    def _return_no_handle(self) -> XmlResponse:
        resp_msg_list = ['抱歉，暂无相关服务！', '现有如下服务：']
        resp_msg_list.extend(self.get_service_list())
        return weixin_reply_tool.reply_text(self.msg_item, '\n'.join(resp_msg_list))

    def handle_subscribe(self) -> XmlResponse:
        """关注的事件"""
        resp_msg_list = ['终于等到您了，为您提供了如下服务：']
        resp_msg_list.extend(self.get_service_list())
        resp_msg_list.append('（取消关注后，即使重新关注，也将无法使用服务！）')
        return weixin_reply_tool.reply_text(self.msg_item, '\n'.join(resp_msg_list))

    def handle_in_blacklist(self) -> XmlResponse:
        """处理黑名单中"""
        # 处理黑名单
        return weixin_reply_tool.reply_text(self.msg_item,
                                            '抱歉，你曾取消过关注，如果想要继续提供服务，请<a href="mailto:afenghome@aliyun.com" target="_blank">联系管理员</a>！')

    @abstractmethod
    def get_all_service(self) -> list[tuple[str, str]]:
        return []

    @abstractmethod
    def handle_text_msg(self) -> XmlResponse:
        return self._return_no_handle()

    @abstractmethod
    def is_in_blacklist(self) -> bool:
        """是否在黑名单中"""
        return False

    @abstractmethod
    def handle_unsubscribe(self) -> XmlResponse:
        """取消关注的事件"""
        # 将用户加入黑名单
        pass


class DefaultWeixinMsgHandler(WeixinMsgHandler, ABC):

    def get_all_service(self) -> list[tuple[str, str]]:
        return [('阿锋书屋（QQ交流群：644437242）', 'https://www.afengbook.com')]

    def is_in_blacklist(self) -> bool:
        """是否在黑名单中"""
        # black_list = blacklist_service.query_weixin_black_list()
        # # 查询用户黑名单
        # return self.msg_item.from_user in black_list
        return False

    def handle_text_msg(self) -> XmlResponse:
        return self._return_no_handle()

    def handle_unsubscribe(self) -> XmlResponse:
        """取消关注的事件"""
        # 将用户加入黑名单
        pass
