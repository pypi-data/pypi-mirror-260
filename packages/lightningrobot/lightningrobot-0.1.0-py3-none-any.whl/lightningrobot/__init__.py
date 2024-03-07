import asyncio
import message

"""
闪电机器人-主模块
"""

async def start():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, message.main)
    print("[信息/Info]启动成功！")

async def print_message(text):
    print(text)