from botpy import Client
from botpy.message import DirectMessage

from ...interface import HandlerInterface
from ...manager import Colors, logger

class Echo(HandlerInterface):

    @property
    def priority(self) -> int:
        return 0
    
    @property
    def name(self) -> str:
        return "Echo"
    
    async def on_ready(self, client: Client):
        logger.info(f'\t插件"{Colors.light_blue}echo{Colors.escape}"加载完成！')
    
    async def on_direct_message_create(self, client: Client, message: DirectMessage) -> bool:
        await client.api.post_dms(
            guild_id=message.guild_id,
            content=f"机器人{client.robot.name}收到你的私信了: {message.content}",
            msg_id=message.id,
        )
        return True