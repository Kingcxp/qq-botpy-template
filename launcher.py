import botpy
from botpy import logging

from botpy.message import DirectMessage

from config import Config


_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人 「{self.robot.name}」 加载完成!")

    async def on_direct_message_create(self, message: DirectMessage):
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=f"机器人{self.robot.name}收到你的私信了: {message.content}",
            msg_id=message.id,
        )


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(
        public_guild_messages=False,    # 公域消息事件
        guild_messages=False,           # 消息事件 (仅 私域 机器人能够设置此 intents)
        direct_message=True,            # 私信事件
        guild_message_reactions=False,  # 消息相关互动事件
        guilds=False,                   # 频道事件
        guild_members=False,            # 频道成员事件
        interaction=False,              # 互动事件
        message_audit=False,            # 消息审核事件
        forums=False,                   # 论坛事件 (仅 私域 机器人能够设置此 intents)
        audio_action=False              # 音频事件
    )
    client = MyClient(intents=intents)
    client.run(appid=Config.appid, token=Config.token)