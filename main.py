from astrbot.api.event import filter
from astrbot.api.all import Star, Context, Plain, Reply, logger
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent


class 表情ID(Star):
    """表情ID查询与发送插件"""

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("表情ID")
    @filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP)
    async def 表情ID(self, event: AiocqhttpMessageEvent, text: str = None):
        """查询或发送指定ID的表情"""
        event.stop_event()
        if isinstance(text, int) or (isinstance(text, str) and text.isdigit()):
            if event.get_group_id():
                结果 = await event.bot.send_msg(
                    group_id=int(event.get_group_id()),
                    message=f"[CQ:face,id={text}]"
                )
            else:
                结果 = await event.bot.send_msg(
                    user_id=int(event.get_sender_id()),
                    message=f"[CQ:face,id={text}]"
                )
            logger.debug(f"[表情ID] 表情发送结果：{结果}")
            return
        yield event.chain_result([
            Reply(id=event.message_obj.message_id),
            Plain(text=find_face_id(event))
        ])


def find_face_id(event: AiocqhttpMessageEvent) -> str:
    """从消息中提取表情ID"""
    try:
        raw_message = event.message_obj.raw_message
        message = raw_message.get('message')
        if message:
            for i in message:
                if i.get('type') == 'face':
                    if 'data' in i and i['data'].get('id'):
                        return str(i['data']['id'])
    except Exception as e:
        logger.warning(f"[表情ID] 查找表情出现错误：{str(e)}", exc_info=True)
        return "查找表情出现错误"

    return "未找到表情ID"
