import os, json
import time
import traceback
from menglingtool_sqltools.mysql import Mysql, Action, SqlData
from menglingtool_sqltools.sqlite import Sqlite
from menglingtool_sqltools.pgsql import Pgsql

# from menglingtool_sqltools.sqlserver import Sqlserver

CONF = f'{os.path.expanduser("~")}/mlflow_week.conf'

ARG = 'arg'
STATUS = 'status'
OUT = 'result'
ERR = 'error'

# 调度器名称及管理员信息
SCHEDULE_NAME = None
EM = None

# 全局域仅本文件中有效
_sqlt = None


def get_sqlt() -> Action:
    assert _sqlt, '未初始化数据库连接方法'
    return _sqlt()


def sqlt_init(if_tz=True):
    global _sqlt, SCHEDULE_NAME, EM
    with (open(CONF, encoding='utf8', mode='r') as file):
        cf = json.loads(file.read())
        SCHEDULE_NAME, EM = cf['schedule_name'], cf['em']
        sqlt, host, user, port, pwd, dbname = \
            cf['sqlt'], cf['host'], cf.get('user'), cf.get('port'), cf.get('pwd'), cf.get('dbname')
        if if_tz: print('加载数据库参数:',
                        {'sqlt': sqlt, 'host': host, 'user': user, 'port': port, 'pwd': pwd, 'dbname': dbname})
        if sqlt == 'pgsql':
            _sqlt = lambda: Pgsql(dbname=dbname, user=user, pwd=pwd, host=host, port=port)
        elif sqlt == 'sqlite':
            _sqlt = lambda: Sqlite(dbfilepath=host)
        elif sqlt == 'mysql':
            _sqlt = lambda: Mysql(dbname=dbname, user=user, pwd=pwd, host=host, port=port)
        # elif sqlt == 'sqlserver':
        #     _sqlt = lambda: Sqlserver(dbname=dbname, user=user, pwd=pwd, host=host, port=port)
        else:
            raise ValueError(f'没有数据库类型sqlt:{sqlt}')


def sqlRetryFunc(func):
    def temp(*args, **kwargs):
        for _ in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('数据库连接错误:\n', traceback.format_exc())
                time.sleep(3)
        raise e

    return temp
