from botpy import Intents

class Config:
    """请在指定的位置填写自己的机器人id和机器人令牌，并凭需求自行调整监听事件类型的设置"""

    intents = Intents(
        public_guild_messages=True,                 # 公域消息事件
        guild_messages=False,                       # 消息事件 (仅 私域 机器人能够设置此 intents)
        direct_message=True,                        # 私信事件
        guild_message_reactions=True,               # 消息相关互动事件
        guilds=True,                                # 频道事件
        guild_members=True,                         # 频道成员事件
        interaction=True,                           # 互动事件
        message_audit=True,                         # 消息审核事件
        forums=False,                               # 论坛事件 (仅 私域 机器人能够设置此 intents)
        audio_action=True                           # 音频事件
    )

    appid = "your_id"                               # 机器人id
    token = "your_token"                            # 机器人令牌
