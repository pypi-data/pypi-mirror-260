import subprocess
import time
import traceback
from .base.config.sqlt import EM, SCHEDULE_NAME
from .base.set import *
from .base.get import *
from menglingtool.time_tool import getNowTime, TimeTool
from menglingtool.notice import emailSend

'''
用于执行任务情况
'''


def _run(command, timeout) -> (str, str):
    sd = getNowTime()
    try:
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        # 获取命令执行的输出
        output = process.stdout.decode('utf-8')
        outerr = process.stderr.decode('utf-8')
        return sd, getNowTime(), output, outerr
    except subprocess.TimeoutExpired:
        return sd, getNowTime(), '', f'代码执行超时-{timeout}s'


def _getNextTime(week) -> str:
    week_schedule = int(week.get('week_schedule', 0))
    times = week.get('times')
    week_dates = week.get('week_dates', '1,2,3,4,5,6,7')
    mon_dates = week.get('mon_dates')
    if week_schedule:
        return getNowTime(ifreturn_str=False).next(0, sn=week_schedule)
    elif times:
        times = sorted(times.split(','))
        t0 = getNowTime(ifreturn_str=False, gs='%Y-%m-%d')
        now = getNowTime()
        if mon_dates: mon_dates = set(mon_dates.split(','))
        week_dates = set(map(int, week_dates.split(',')))
        while True:
            if (mon_dates and t0.to_txt(gs='%d') not in mon_dates) \
                    or (t0.isoweekday() not in week_dates):
                t0.next(1, if_replace=True)
            else:
                for td in times:
                    td = TimeTool(f'{t0.to_txt()} {td}')
                    if td > now: return td.to_txt()
                t0.next(1, if_replace=True)
    else:
        print(f'\x1b[31m时间参数配置有误,week_schedule和times不能都为空！\n任务时间设置为最大...\x1b[0m')
        return '9999-01-01 00:00:00'


def _errFunc(func):
    def temp():
        try:
            return func()
        except Exception as e:
            emailSend(F'调度器-{SCHEDULE_NAME}  执行错误!', traceback.format_exc(), EM)
            raise e

    return temp


@_errFunc
def start_schedule():
    while True:
        for arg, status in getWaits():
            status.running()
            setStatus(status)
            sd, ed, output, outerr = _run(arg.ml, arg.timeout)
            running_seconds = TimeTool(ed) - TimeTool(sd)
            if outerr:
                if output: outerr = f'{output}\n{outerr}'
                status.error(arg.err_week, running_seconds)
                saveErr(arg.task, status.fault_err_num, sd, ed, running_seconds, outerr)
                # 超出最大错误则进行通知
                if status.fault_err_num >= arg.max_err_num:
                    emailSend('任务执行错误', f'任务-{arg.task} 错误！\n{outerr}', arg.emails)
                    next_time = _getNextTime(arg.week)
                    status.wait(next_time, running_seconds, iferr=True)
            else:
                next_time = _getNextTime(arg.week)
                status.wait(next_time, running_seconds)
                saveOut(arg.task, sd, ed, running_seconds, output)
            setStatus(status)
        time.sleep(1)
