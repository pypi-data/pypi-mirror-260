from lightningrobot import log
import asyncio
import websockets
import sys

async def main(path,host):
    global serverhost
    serverhost = host
    sys.path.append(path)
    import plugins
    async def main(websocket, path):
        async for message in websocket:
            log.info(f"收到消息：: {message}")
            await websocket.send(plugins.main(message))

    start_server = websockets.serve(main, "localhost", host)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
async def send(path,text):
    sys.path.append(path)
    import plugins
    async with websockets.connect("ws://localhost:" + serverhost) as websocket:
        await websocket.send(text)
        log.info(f"发送: {text}")
    asyncio.run(send())