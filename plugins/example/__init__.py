from nonebot.adapters.onebot.v12 import GroupMessageEvent,MessageSegment,Bot
from nonebot.message import event_preprocessor
from nonebot.plugin import on_regex
from nonebot.exception import IgnoredException
from nonebot import get_bot, get_driver,logger
from os import getcwd
from os.path import join

# 按照正则表达式匹配，别的匹配方式会在暂时不存在的文档里面提及
# 是大佬就直接读nonebot2的文档，里面有一个on_command的函数，更符合snaphack对于微信机器人的想象
matcher = on_regex(r"^example$")

# hook函数例子，大概率不用学
# 这个例子的作用是过滤群
@event_preprocessor
async def whitelist(event: GroupMessageEvent):
    if event.group_id != "23278031443@chatroom":
        raise IgnoredException("not in needed group")

# 不需要进行对于群的过滤，已经使用上面hook例子函数过滤了
# 这里的matcher就是上面的on_regex定义的
@matcher.handle()
async def abcd(event:GroupMessageEvent): # GroupMessageEvent代表收到的是群消息

    # 使用nonebot的logger输出信息而非使用print
    logger.info("example start!")

    # 获取当前适配器的bot
    bot = get_bot()
    
    # 上传图片，直接输入相对路径貌似会有问题，所以采用os.getcwd -> 默认获取到wechat文件夹的路径
    file_id = await bot.upload_file(type = "path",
                            name = "setu.png",
                            path = join(getcwd(), r"data\setu.png")
                            ) 
    
    # 构造需要发送的消息，可以直接用+连接文本
    message = MessageSegment.text("芝士测试函数") + MessageSegment.image(file_id=file_id["file_id"])

    # 发送消息，由于微信没法像qq一样图片与文字一起发送，所以上面构造出来的消息会分开了发送
    # event变量可以通过读源码或者ide提示的方式了解里面有啥东西
    await bot.send_message(detail_type="group", group_id=event.group_id, message=message)

    # 表明此事件结束
    matcher.finish()