import os
import click
import json
from menglingtool_sqltools.tools import encrypt
from configparser import ConfigParser
from .base.config.sqlt import CONF, sqlt_init
from .base.get import getAllArgs, getAllStatus
from .base.set import table_init, set_arg, restartTask
from .base.config.arg import Arg
from .schedule import start_schedule


# 设置数据库访问
def _setSqlt(em, sname, sqlt, host, user, port, pwd, dbname):
    if os.path.exists(CONF):
        with open(CONF, encoding='utf8', mode='r') as file:
            cf = json.loads(file.read() or '{}')
    else:
        cf = {}
    with open(CONF, encoding='utf8', mode='w') as file:
        if em: cf['em'] = em
        if sname: cf['schedule_name'] = sname
        if sqlt: cf['sqlt'] = sqlt
        if host: cf['host'] = host
        if port: cf['port'] = port
        if user: cf['user'] = user
        if pwd: cf['pwd'] = encrypt(user, pwd)
        if dbname: cf['dbname'] = dbname
        file.write(json.dumps(cf))


# 插入任务配置
def _put_week_task(task_path):
    sqlt_init()
    table_init()
    config = ConfigParser()
    config.read(task_path, encoding='utf8')
    arg = Arg(**config['base'], week=config['week_schedule'])
    set_arg(arg, config['start']['reload_status'] in ['true', 'True'])


# 任务启动
def _start():
    sqlt_init()
    table_init()
    start_schedule()


# 参数查看
def _look(is_q, is_a, is_s):
    if is_a or is_s: sqlt_init(if_tz=False)
    if is_q:
        with (open(CONF, encoding='utf8', mode='r+') as file):
            cf = json.loads(file.read() or '{}')
            print('调度器配置:', cf)
    if is_a:
        print('任务参数:')
        [print(dt) for dt in getAllArgs()]
    if is_s:
        print('任务状态:')
        [print(dt) for dt in getAllStatus()]


_example = '''
#基础配置
[base]
task = 任务名称
stop = false
max_err_num = 3
emails = 1321443305@qq.com
err_week = 3600
timeout = 1800
power = 5
ml = cd .. && python conf.py

#启动配置
[start]
reload_status = true

#任务执行周期配置
[week_schedule]
#周期配置(s),此项不为空则以下配置均无效
week_schedule = 3600

#指定日期
#times = 10:20:00,18:20:00

#设置日期执行
#mon_dates = 1
#week_dates = 2,4,6
'''


# 导出任务配置文件

@click.command()
@click.argument('act')
# 设置通知邮箱及调度器名称
@click.option('--em', help='通知邮箱')
@click.option('--sname', help='调度器名称')
# 设置数据库访问
@click.option('--sqlt', help='数据库类型')
@click.option('--host')
@click.option('--user')
@click.option('--port')
@click.option('--pwd')
@click.option('--dbname')
# 装载任务
@click.option('-tp', '--task-path', help='任务配置文件路径')
# 立即启动任务
@click.option('-st', '--start-task', help='设置立即开始任务')
# 查看参数
@click.option('-q', 'is_q', is_flag=True, help='查看当前连接配置')
@click.option('-a', 'is_a', is_flag=True, help='查看当前参数')
@click.option('-s', 'is_s', is_flag=True, help='查看当前状态')
def transfer(act, em, sname,
             sqlt, host, user, port, pwd, dbname,
             task_path, start_task,
             is_q, is_a, is_s):
    if act == 'download':
        # 下载配置文件
        with open('./example.ini', mode='w+', encoding='utf8') as file:
            file.write(_example)
        print('已下载配置参考文件 example.ini')
    elif act == 'start':
        # 任务启动
        _start()
    elif act == 'set':
        # 保存配置信息
        if em or sname or sqlt or host or user or port or pwd:
            _setSqlt(em, sname, sqlt, host, user, port, pwd, dbname)
        if task_path: _put_week_task(task_path)
        if start_task:
            print(f'重置任务状态-{start_task}')
            restartTask(start_task)
    elif act == 'look':
        _look(is_q, is_a, is_s)
    else:
        print('命令错误,仅 look set start download')
