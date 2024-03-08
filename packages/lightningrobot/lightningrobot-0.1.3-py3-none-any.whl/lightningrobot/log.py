"""
闪电机器人-日志输出
"""
def error(msg):
    print("\033[31m[错误-Error]",msg)

def warrning(msg):
    print("\033[33m[警告-Warrning]\033[0m",msg)

def info(msg):
    print("\033[94m[信息-Info]\033[0m",msg)
