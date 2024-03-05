import json
from menglingtool.progress import jdprint
from menglingtool_sqltools.mysql import Mysql
from menglingtool_sqltools.pgsql import Pgsql
from menglingtool_sqltools.tools import SqlData
from menglingtool.time_tool import runTimeFunc
from menglingtool.thread import getTasks, threads_run
from pandas import DataFrame
import warnings


# 数量检查
def checknum(dtgoods, name, name_wait):
    r = dtgoods.getThreadKeyGood('r')
    assert r.getLen(name, _class='hash') == r.getLen(name_wait), \
        f'数量不一致,不执行插入数据库任务! {r.getLen(name, _class="hash")}/{r.getLen(name_wait)}'


# 获取全部列
def _getLies(r, dts):
    if dts:
        lies = list(DataFrame(data=dts).columns)
        return lies
    else:
        return []


# 数据迭代器
def _datait(r, name, n, if_auto_data=True, nowday=None):
    allkeys = r.hkeys(name)
    for i in range(0, len(allkeys), n):
        redts = list()
        for txt in r.hmget(name, allkeys[i:i + n]):
            for dt in json.loads(txt):
                for k in dt.keys():
                    # 格式清洗
                    if if_auto_data and type(dt[k]) in (tuple, list, dict):
                        dt[k] = json.dumps(dt[k], ensure_ascii=False)
                    dt[k] = str(dt[k]).strip().replace('\x00', '')
                # 添加更新日期
                if nowday:  dt['更新日期'] = nowday
                redts.append(dt)
        yield redts
    yield None


def _ch_insert(dbname, connect, table, lies, dts, cig):
    with Mysql(dbname, **connect) as myt:
        try:
            data = SqlData(dts)
            myt.insert(table, lies, data.getDts(lies))
            myt.commit()
        except Exception as e:
            myt.rollback()
            cig['error'] = e


@runTimeFunc
def inMysql(name, dbname, table, connect, lies, threadnum, n, dtgoods,
            nowday, if_auto_data, ifdeltable, key=None, coldt=None):
    connect = connect.copy()
    connect['ifassert'] = True
    r = dtgoods.getThreadKeyGood('r')
    # 数据准备
    jdprint('读取及处理redis数据...')
    datait = _datait(r, name, n, if_auto_data, nowday)
    datadts = next(datait)
    if lies is None: lies = _getLies(r, datadts)
    if len(lies) == 0:
        warnings.warn(f'{name} 没有获的列,不执行插入操作!')
        return
    with Mysql(dbname, **connect) as myt:
        # 处理结果表
        if nowday and myt.ifExist(table):
            myt.delete(table, f"`更新日期`='{nowday}'")
        else:
            if ifdeltable: myt.deleteTable(table)
            myt.createTable(table, lies, colmap=coldt, key=key)
        myt.commit()

    all_value_len = 0
    cig = dict()
    # 插入
    while True:
        if datadts:
            all_value_len += len(datadts)
        else:
            break
        jdprint('插入mysql...%s' % n)
        tasks = getTasks(threadnum, datadts)
        threads_run(_ch_insert, [[dbname, connect, table, lies, dts, cig] for dts in tasks], ifone=False)
        # 子任务出现错误抛出
        if cig.get('error'):
            raise cig['error']
        else:
            datadts = next(datait)
    if all_value_len == 0: print('没有数据插入数据库!')


@runTimeFunc
def inMysql_strict(name, dbname, table, connect, lies, threadnum, n,
                   dtgoods, nowday, if_auto_data, ifdeltable,
                   key=None, coldt=None):
    temp_table = table + '_datatemp'
    connect = connect.copy()
    connect['ifassert'] = True
    r = dtgoods.getThreadKeyGood('r')
    jdprint('读取及处理redis数据...')
    datait = _datait(r, name, n, if_auto_data, nowday)
    datadts = next(datait)
    if lies is None: lies = _getLies(r, datadts)
    if len(lies) == 0:
        warnings.warn(f'{name} 没有获的列,不执行插入操作!')
        return
    all_value_len = 0
    cig = dict()
    with Mysql(dbname, **connect) as myt:
        # 删除临时表
        myt.deleteTable(temp_table)
        # 创建临时表
        myt.createTable(temp_table, lies, colmap=coldt, key=key)
        # 插入临时表
        while True:
            if datadts:
                all_value_len += len(datadts)
            else:
                break
            jdprint('插入mysql...%s' % n)
            tasks = getTasks(threadnum, datadts)
            threads_run(_ch_insert, [[dbname, connect, temp_table, lies, dts, cig] for dts in tasks], ifone=False)
            if cig.get('error'):
                raise cig['error']
            else:
                datadts = next(datait)
        if all_value_len == 0: print('没有数据插入数据库!')
        # 处理结果表
        if myt.ifExist(table):
            if ifdeltable:
                if nowday is None:
                    myt.deleteTable(table)
                else:
                    myt.delete(table, f"`更新日期`='{nowday}'")
                    myt.commit()
        else:
            myt.createTable(table, lies, colmap=coldt, key=key)
        # 同步数据
        try:
            myt.run(f'INSERT INTO `{table}` select * from `{temp_table}`')
        except Exception as e:
            myt.rollback()
            raise e
        myt.deleteTable(temp_table)
        myt.commit()


def _ch_pg_insert(dbname, connect, table, lies, dts, cig):
    with Pgsql(dbname, **connect) as pgt:
        try:
            data = SqlData(dts)
            pgt.insert(table, lies, data.getDts(lies))
            pgt.commit()
        except Exception as e:
            pgt.rollback()
            cig['error'] = e


@runTimeFunc
def inPGsql(name, dbname, table, connect, lies, threadnum, n, dtgoods,
            nowday, if_auto_data, ifdeltable, key=None, colmap=None):
    connect = connect.copy()
    connect['ifassert'] = True
    r = dtgoods.getThreadKeyGood('r')
    # 数据准备
    jdprint('读取及处理redis数据...')
    datait = _datait(r, name, n, if_auto_data, nowday)
    datadts = next(datait)
    if lies is None: lies = _getLies(r, datadts)
    if len(lies) == 0:
        warnings.warn(f'{name} 没有获的列,不执行插入操作!')
        return
    with Pgsql(dbname, **connect) as pgt:
        # 处理结果表
        if nowday and pgt.ifExist(table):
            pgt.delete(table, f"\"更新日期\"='{nowday}'")
        else:
            if ifdeltable: pgt.deleteTable(table)
            pgt.createTable(table, lies, colmap=colmap, key=key)
        pgt.commit()

    all_value_len = 0
    cig = dict()
    # 插入
    while True:
        if datadts:
            all_value_len += len(datadts)
        else:
            break
        jdprint('插入pgsql...%s' % n)
        tasks = getTasks(threadnum, datadts)
        threads_run(_ch_pg_insert, [[dbname, connect, table, lies, dts, cig] for dts in tasks], ifone=False)
        # 子任务出现错误抛出
        if cig.get('error'):
            raise cig['error']
        else:
            datadts = next(datait)
    if all_value_len == 0: print('没有数据插入数据库!')
