from menglingtool.time_tool import TimeTool, getNowTime


class Status:
    colmap = {'task': 'varchar',
              'next_time': 'varchar',
              'fault_err_num': 'int',
              'status': 'varchar'}

    def __init__(self, task, fault_err_num, next_time, status, **_):
        self.task = task
        self.next_time = next_time or getNowTime()
        self.fault_err_num = int(fault_err_num or 0)
        self.status = status or '等待'

    def get(self) -> dict:
        return {
            'task': self.task,
            'next_time': self.next_time,
            'fault_err_num': self.fault_err_num,
            'status': self.status,
        }

    # 状态切换
    def running(self):
        self.status = '执行'
        print(f"\x1b[33m{self.task} 开始执行...\x1b[0m")

    def error(self, week, running_seconds):
        self.fault_err_num += 1
        self.status = '错误'
        self.next_time = TimeTool(self.next_time).next(0, sn=week)
        print(f"\x1b[31m{self.task} 出现错误-执行结束!\n"
              f"执行时间:{running_seconds:.4f}s"
              f"\n下次执行:{self.next_time}\x1b[0m")

    def wait(self, next_time, running_seconds, iferr=False):
        self.status = '等待'
        self.fault_err_num = 0
        self.next_time = next_time
        print(f"\x1b[{31 if iferr else 32}m {self.task} {'出现错误-' if iferr else ''}执行结束!\n"
              f"执行时间:{running_seconds:.4f}s"
              f"\n下次执行:{self.next_time}\x1b[0m")
