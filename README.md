<div align="center">

# qq-botpy-template

_✨ 简易的插件加载式QQ机器人框架 ✨_

</div>

### 简介：

qq-botpy-template 是为了更方便地使用[QQ开放平台](https://q.qq.com/)提供的 `Python SDK`而在此基础上进一步搭建的插件加载式框架。你能够编写若干个插件将机器人的不同功能分开编写，并在机器人启动时统一加载，十分的方便有效。

### 即刻开始：

使用git克隆此项目：

```sh
git clone https://github.com/Kingcxp/qq-botpy-template.git
```

安装依赖：

```sh
pip install -r requirements.txt
```

配置config.py：

```python
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

```

启动项目：

```sh
cd qq-botpy-template
python launcher.py
```

大功告成！

### 开发插件：

可以阅读 `app/interface.py`中对 `HandlerInterface`的注解并参照 `app/plugins/echo`中的实例插件内容进行插件的编写
代码编写上手十分简单，很容易就能学会！

---

Plz give me a star! OTZ
