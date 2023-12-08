import os
import sys
import botpy

from pathlib import Path

from botpy.message import Message, DirectMessage, MessageAudit
from botpy.reaction import Reaction
from botpy.guild import Guild
from botpy.channel import Channel
from botpy.user import Member
from botpy.interaction import Interaction
from botpy.forum import Thread
from botpy.types.forum import Post, Reply, AuditResult
from botpy.audio import Audio

from config import Config
from app import HandlerInterface, Colors, load_all_plugins


logger = botpy.logging.get_logger()


class BotClient(botpy.Client):
    """全局对象，用来管理所有插件的响应器

    Args:
        botpy (botpy.Client): Client基类
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.all_apis = (
            "on_ready",
            "on_at_message_create",
            "on_public_message_delete",
            "on_message_create",
            "on_message_delete",
            "on_direct_message_create",
            "on_direct_message_delete",
            "on_message_reaction_add",
            "on_message_reaction_remove",
            "on_guild_create",
            "on_guild_update",
            "on_guild_delete",
            "on_channel_create",
            "on_channel_update",
            "on_channel_delete",
            "on_guild_member_add",
            "on_guild_member_update",
            "on_guild_member_remove",
            "on_interaction_create",
            "on_message_audit_pass",
            "on_message_audit_reject",
            "on_forum_thread_create",
            "on_forum_thread_update",
            "on_forum_thread_delete",
            "on_forum_post_create",
            "on_forum_post_delete",
            "on_forum_reply_create",
            "on_forum_reply_delete",
            "on_forum_publish_audit_result",
            "on_audio_start",
            "on_audio_finish",
            "on_audio_on_mic",
            "on_audio_off_mic"
        )
        self.handlers = {}
        for api in self.all_apis:
            self.handlers[api] = []

    def register(self, handler: HandlerInterface) -> None:
        """注册响应器

        Args:
            handler (HandlerInterface): 继承响应器接口的响应器类
        """
        for api in self.all_apis:
            if hasattr(handler, api):
                self.handlers[api].append((handler.priority, handler.name, getattr(handler, api)))

    async def on_ready(self) -> None:
        """机器人准备好时调用"""
        for api in self.all_apis:
            self.handlers[api].sort(key=lambda x: x[0])
        for handler in self.handlers["on_ready"]:
            await handler[2](self)
        logger.info(f"机器人 「{Colors.green}{self.robot.name}{Colors.escape}」 加载完成!")

    #############################################
    # 公域消息事件，需订阅事件 public_guild_messages
    #############################################

    async def on_at_message_create(self, message: Message):
        """@机器人的消息事件

        Args:
            message (Message): 消息对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    async def on_public_message_delete(self, message: Message):
        """频道的消息被删除公域事件

        Args:
            message (Message): 消息对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break
        
    #######################################################
    # 私域消息事件，仅私域机器人可用，需订阅事件 guild_messages
    #######################################################

    async def on_message_create(self, message: Message):
        """发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。

        Args:
            message (Message): 消息对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    async def on_message_delete(self, message: Message):
        """删除（撤回）消息事件

        Args:
            message (Message): 消息对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    ###################################
    # 私信事件，需订阅事件 direct_message
    ###################################

    async def on_direct_message_create(self, message: DirectMessage):
        """私信消息事件

        Args:
            message (DirectMessage): 私信会话对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    async def on_direct_message_delete(self, message: DirectMessage):
        """私信删除（撤回）消息事件

        Args:
            message (DirectMessage): 私信会话对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    ##################################################
    # 消息相关互动事件，需订阅事件 guild_message_reactions
    ##################################################

    async def on_message_reaction_add(self, reaction: Reaction):
        """为消息添加表情表态事件

        Args:
            reaction (Reaction): 表情表态对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, reaction)
            if do_continue:
                break

    async def on_message_reaction_remove(self, reaction: Reaction):
        """为消息删除表情表态事件

        Args:
            reaction (Reaction): 表情表态对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, reaction)
            if do_continue:
                break

    ###########################
    # 频道事件，需订阅事件 guilds
    ###########################

    async def on_guild_create(self, guild: Guild):
        """机器人加入新guild事件

        Args:
            guild (Guild): 频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, guild)
            if do_continue:
                break

    async def on_guild_update(self, guild: Guild):
        """guild资料发生变更事件

        Args:
            guild (Guild): 频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, guild)
            if do_continue:
                break

    async def on_guild_delete(self, guild: Guild):
        """机器人退出guild事件

        Args:
            guild (Guild): 频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, guild)
            if do_continue:
                break
    
    async def on_channel_create(self, channel: Channel):
        """channel被创建事件

        Args:
            channel (Channel): 子频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, channel)
            if do_continue:
                break

    async def on_channel_update(self, channel: Channel):
        """channel被更新事件

        Args:
            channel (Channel): 子频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, channel)
            if do_continue:
                break

    async def on_channel_delete(self, channel: Channel):
        """channel被删除事件

        Args:
            channel (Channel): 子频道对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, channel)
            if do_continue:
                break

    #####################################
    # 频道成员事件，需订阅事件 guild_members
    #####################################

    async def on_guild_member_add(self, member: Member):
        """成员加入事件

        Args:
            member (Member): 成员对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, member)
            if do_continue:
                break

    async def on_guild_member_update(self, member: Member):
        """成员资料发生变更事件

        Args:
            member (Member): 成员对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, member)
            if do_continue:
                break

    async def on_guild_member_remove(self, member: Member):
        """成员被移除事件

        Args:
            member (Member): 成员对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, member)
            if do_continue:
                break

    ################################
    # 互动事件，需订阅事件 interaction
    ################################

    async def on_interaction_create(self, interaction: Interaction):
        """收到用户发给机器人的私信消息

        Args:
            interaction (Interaction): 互动事件
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, interaction)
            if do_continue:
                break

    #####################################
    # 消息审核事件，需订阅事件 message_audit
    #####################################

    async def on_message_audit_pass(self, message: MessageAudit):
        """消息审核通过事件

        Args:
            message (MessageAudit): 消息审核事件
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    async def on_message_audit_reject(self, message: MessageAudit):
        """消息审核不通过事件

        Args:
            message (MessageAudit): 消息审核事件
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, message)
            if do_continue:
                break

    ##########################################
    # 论坛事件，仅私域机器人可用，需订阅事件 forums
    ##########################################

    async def on_forum_thread_create(self, thread: Thread):
        """用户创建主题事件

        Args:
            thread (Thread): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, thread)
            if do_continue:
                break

    async def on_forum_thread_update(self, thread: Thread):
        """用户更新主题事件

        Args:
            thread (Thread): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, thread)
            if do_continue:
                break

    async def on_forum_thread_delete(self, thread: Thread):
        """用户删除主题事件

        Args:
            thread (Thread): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, thread)
            if do_continue:
                break

    async def on_forum_post_create(self, post: Post):
        """用户创建帖子事件

        Args:
            post (Post): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, post)
            if do_continue:
                break

    async def on_forum_post_delete(self, post: Post):
        """用户删除帖子事件

        Args:
            post (Post): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, post)
            if do_continue:
                break

    async def on_forum_reply_create(self, reply: Reply):
        """用户回复评论事件

        Args:
            reply (Reply): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, reply)
            if do_continue:
                break

    async def on_forum_reply_delete(self, reply: Reply):
        """用户删除评论事件

        Args:
            reply (Reply): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, reply)
            if do_continue:
                break

    async def on_forum_publish_audit_result(self, auditresult: AuditResult):
        """用户发表审核通过事件

        Args:
            auditresult (AuditResult): 论坛对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, auditresult)
            if do_continue:
                break

    ##############################
    # 音频事件，需订阅 audio_action
    ##############################

    async def on_audio_start(self, audio: Audio):
        """音频开始播放事件

        Args:
            audio (Audio): 音频对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, audio)
            if do_continue:
                break

    async def on_audio_finish(self, audio: Audio):
        """音频播放结束事件

        Args:
            audio (Audio): 音频对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, audio)
            if do_continue:
                break

    async def on_audio_on_mic(self, audio: Audio):
        """上麦事件

        Args:
            audio (Audio): 音频对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, audio)
            if do_continue:
                break

    async def on_audio_off_mic(self, audio: Audio):
        """下麦事件

        Args:
            audio (Audio): 音频对象
        """
        func_name = sys._getframe().f_code.co_name
        logger.info(f"收到事件 {Colors.light_blue}{func_name}{Colors.escape}!")
        for handler in self.handlers[func_name]:
            logger.info(f"事件将被 {Colors.yellow}{handler[1]}{Colors.escape}.{Colors.light_blue}{func_name}{Colors.escape} 响应器处理 (优先级：{Colors.green}{handler[0]}{Colors.escape})...")
            do_continue = await handler[2](self, audio)
            if do_continue:
                break


if __name__ == "__main__":
    try:
        os.remove(os.path.dirname(__file__) + "/botpy.log")
    except FileNotFoundError:
        pass
    client = BotClient(intents=Config.intents)
    load_all_plugins(
        client,
        launcher_path=Path(os.path.dirname(os.path.abspath(__file__))).resolve(),
        plugin_dir=[os.path.dirname(__file__) + '/app/plugins']
    )
    client.run(appid=Config.appid, token=Config.token)
