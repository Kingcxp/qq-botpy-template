from abc import ABCMeta, abstractmethod


class HandlerInterface(metaclass=ABCMeta):
    """事件响应器接口类

    必须实现的内容：
    ```python
    @property
    def priority(self, client: botpy.Client) -> int:
        # 返回事件响应器优先级，值越小越优先

    @property
        client (botpy.Client): 机器人端对象，用来调用机器人api
    def name(self, client: botpy.Client) -> str:
        # 返回事件响应器名称，用来记录日志
    ```

    client (botpy.Client): 机器人端对象，用来调用机器人api
    可以使用的接口及其规范约定：
    ```python
    async def on_ready(self, client: botpy.Client) -> None:
        '''机器人准备好时调用'''

    #############################################
        client (botpy.Client): 机器人端对象，用来调用机器人api
    # 公域消息事件，需订阅事件 public_guild_messages
    #############################################

    async def on_at_message_create(self, client: botpy.Client, message: Message) -> bool:
        '''@机器人的消息事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (Message): 消息对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_public_message_delete(self, client: botpy.Client, message: Message) -> bool:
        '''频道的消息被删除公域事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (Message): 消息对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''
        
    #######################################################
    # 私域消息事件，仅私域机器人可用，需订阅事件 guild_messages
    #######################################################

    async def on_message_create(self, client: botpy.Client, message: Message) -> bool:
        '''发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (Message): 消息对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_message_delete(self, client: botpy.Client, message: Message) -> bool:
        '''删除（撤回）消息事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (Message): 消息对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ###################################
    # 私信事件，需订阅事件 direct_message
    ###################################

    async def on_direct_message_create(self, client: botpy.Client, message: DirectMessage) -> bool:
        '''私信消息事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (DirectMessage): 私信会话对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_direct_message_delete(self, client: botpy.Client, message: DirectMessage) -> bool:
        '''私信删除（撤回）消息事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (DirectMessage): 私信会话对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ##################################################
    # 消息相关互动事件，需订阅事件 guild_message_reactions
    ##################################################

    async def on_message_reaction_add(self, client: botpy.Client, reaction: Reaction) -> bool:
        '''为消息添加表情表态事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            reaction (Reaction): 表情表态对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_message_reaction_remove(self, client: botpy.Client, reaction: Reaction) -> bool:
        '''为消息删除表情表态事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            reaction (Reaction): 表情表态对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ###########################
    # 频道事件，需订阅事件 guilds
    ###########################

    async def on_guild_create(self, client: botpy.Client, guild: Guild) -> bool:
        '''机器人加入新guild事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            guild (Guild): 频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_guild_update(self, client: botpy.Client, guild: Guild) -> bool:
        '''guild资料发生变更事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            guild (Guild): 频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_guild_delete(self, client: botpy.Client, guild: Guild) -> bool:
        '''机器人退出guild事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            guild (Guild): 频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''
    
    async def on_channel_create(self, client: botpy.Client, channel: Channel) -> bool:
        '''channel被创建事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            channel (Channel): 子频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_channel_update(self, client: botpy.Client, channel: Channel) -> bool:
        '''channel被更新事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            channel (Channel): 子频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_channel_delete(self, client: botpy.Client, channel: Channel) -> bool:
        '''channel被删除事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            channel (Channel): 子频道对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    #####################################
    # 频道成员事件，需订阅事件 guild_members
    #####################################

    async def on_guild_member_add(self, client: botpy.Client, member: Member) -> bool:
        '''成员加入事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            member (Member): 成员对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_guild_member_update(self, client: botpy.Client, member: Member) -> bool:
        '''成员资料发生变更事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            member (Member): 成员对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_guild_member_remove(self, client: botpy.Client, member: Member) -> bool:
        '''成员被移除事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            member (Member): 成员对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ################################
    # 互动事件，需订阅事件 interaction
    ################################

    async def on_interaction_create(self, client: botpy.Client, interaction: Interaction) -> bool:
        '''收到用户发给机器人的私信消息

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            interaction (Interaction): 互动事件

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    #####################################
    # 消息审核事件，需订阅事件 message_audit
    #####################################

    async def on_message_audit_pass(self, client: botpy.Client, message: MessageAudit) -> bool:
        '''消息审核通过事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (MessageAudit): 消息审核事件

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_message_audit_reject(self, client: botpy.Client, message: MessageAudit) -> bool:
        '''消息审核不通过事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            message (MessageAudit): 消息审核事件

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ##########################################
    # 论坛事件，仅私域机器人可用，需订阅事件 forums
    ##########################################

    async def on_forum_thread_create(self, client: botpy.Client, thread: Thread) -> bool:
        '''用户创建主题事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            thread (Thread): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_thread_update(self, client: botpy.Client, thread: Thread) -> bool:
        '''用户更新主题事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            thread (Thread): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_thread_delete(self, client: botpy.Client, thread: Thread) -> bool:
        '''用户删除主题事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            thread (Thread): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_post_create(self, client: botpy.Client, post: Post) -> bool:
        '''用户创建帖子事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            post (Post): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_post_delete(self, client: botpy.Client, post: Post) -> bool:
        '''用户删除帖子事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            post (Post): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_reply_create(self, client: botpy.Client, reply: Reply) -> bool:
        '''用户回复评论事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            reply (Reply): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_reply_delete(self, client: botpy.Client, reply: Reply) -> bool:
        '''用户删除评论事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            reply (Reply): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_forum_publish_audit_result(self, client: botpy.Client, auditresult: AuditResult) -> bool:
        '''用户发表审核通过事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            auditresult (AuditResult): 论坛对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    ##############################
    # 音频事件，需订阅 audio_action
    ##############################

    async def on_audio_start(self, client: botpy.Client, audio: Audio) -> bool:
        '''音频开始播放事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            audio (Audio): 音频对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_audio_finish(self, client: botpy.Client, audio: Audio) -> bool:
        '''音频播放结束事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            audio (Audio): 音频对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_audio_on_mic(self, client: botpy.Client, audio: Audio) -> bool:
        '''上麦事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            audio (Audio): 音频对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''

    async def on_audio_off_mic(self, client: botpy.Client, audio: Audio) -> bool:
        '''下麦事件

        Args:
            client (botpy.Client): 机器人端对象，用来调用机器人api
            audio (Audio): 音频对象

        Returns:
            (bool): 消息是否继续向之后的事件响应器传递, 是为False, 否为True
        '''
    ```
    """

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        """返回优先级，值越低越先执行，尽量避免相同值"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """返回事件响应器名称，用来记录日志"""
        pass
