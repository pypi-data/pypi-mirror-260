from lightningrobot import message,log
import asyncio

"""
闪电机器人-主模块
"""

async def start(path,host):
    if not host:
        host = 2727
        log.warrning("未提供主机端口！已使用默认端口2727！")
    global botpath
    botpath = path
    await message.main(path,host)
    log.info("成功启动机器人！")
    
async def send(text):
    #使用启动时存储的botpath发送消息而不需要开发者提供path。
    asyncio.run(message.send(botpath,text))