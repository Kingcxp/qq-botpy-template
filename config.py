from botpy import Intents

class Config:

    intents = Intents(
        public_guild_messages=False,                # 公域消息事件
        guild_messages=False,                       # 消息事件 (仅 私域 机器人能够设置此 intents)
        direct_message=True,                        # 私信事件
        guild_message_reactions=False,              # 消息相关互动事件
        guilds=False,                               # 频道事件
        guild_members=False,                        # 频道成员事件
        interaction=False,                          # 互动事件
        message_audit=False,                        # 消息审核事件
        forums=False,                               # 论坛事件 (仅 私域 机器人能够设置此 intents)
        audio_action=False                          # 音频事件
    )

    appid = "your_id"                               # 机器人id
    token = "your_token"                            # 机器人令牌
