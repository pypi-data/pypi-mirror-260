import web
from plugin import conmand
urls = (
    '/(.*)', 'index',
    '/message/(.*)', 'message'
)

class index:
    def GET(self):
        return "欢迎使用 ⚡闪电机器人⚡"
    
class message:
    def GET(self, message):
        return conmand.message(message)

def run():
    app = web.application(urls, globals())
    app.run()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()