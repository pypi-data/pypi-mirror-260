import sys
import os
import web

# 获取当前脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir not in sys.path:
    sys.path.append(script_dir)

import plugins
import lightningrobot
urls = (
    '/', 'index',
    '/message/(.*)', 'message',
)

class index:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        return "<h1>欢迎使用 ⚡闪电机器人⚡</h1>"
    
class message:
    def GET(self,text):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        lightningrobot.print_message(text)
        message = plugins.message(text)
        return message

def main():
    app = web.application(urls, globals())
    app.run()