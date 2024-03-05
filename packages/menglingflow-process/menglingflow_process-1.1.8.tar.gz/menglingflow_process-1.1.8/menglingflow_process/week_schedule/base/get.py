from .config.sqlt import get_sqlt, STATUS, ARG, sqlRetryFunc
from menglingtool.time_tool import getNowTime
from .config.status import Status
from .config.arg import Arg


# def getStratArgs() -> list[Arg]:
#     with get_sqlt() as sqlt:
#         return [Arg(**dt) for dt in sqlt.select('*', ARG, where='stop=0')]


# 获取当前需要执行的任务组
@sqlRetryFunc
def getWaits() -> list:
    with get_sqlt() as sqlt:
        sqlt.run(f'''
            select b.*,a.*
            from arg a left JOIN status b on a.task=b.task
            where not stop and (next_time<'{getNowTime()}' or next_time is null)
            ORDER BY power desc ''')
        results = sqlt.getResult(data_class='dts')[1]
        args_status = [(Arg(**dt), Status(**dt)) for dt in results]
        return args_status


@sqlRetryFunc
def getAllArgs() -> list:
    with get_sqlt() as sqlt:
        if sqlt.ifExist(ARG):
            return sqlt.select('*', ARG)
        else:
            return []


@sqlRetryFunc
def getAllStatus() -> list:
    with get_sqlt() as sqlt:
        if sqlt.ifExist(STATUS):
            return sqlt.select('*', STATUS)
        else:
            return []
