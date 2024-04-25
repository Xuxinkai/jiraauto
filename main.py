import threading

from tools import Jiratools
from tools.Logger import logs

logger = logs('main.py').getLogger()  # 调用logger接口



def func_task():
    logger.info('执行任务开始...')
    jiratool = Jiratools.JiraTool(username='', password='=')
    jql = ''
    issues = jiratool.search_jira_jql(jql=jql)
    jiratool.jira_response_scan(issues)
    jiratool.close_client()
    logger.info('执行任务结束...')


def func_timer():
    func_task()
    global timer  # 定义全局变量

    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer = threading.Timer(30*50, func_timer)  # sec秒调用一次函数

    # logger.info("线程名称={},\n正在执行的线程列表:{},\n正在执行的线程数量={},\n当前激活线程={}\n".format(
    #     timer.getName(), threading.enumerate(), threading.active_count(), timer.isAlive)
    # )

    timer.start()  # 启用定时器


if __name__ == '__main__':
    func_timer()
