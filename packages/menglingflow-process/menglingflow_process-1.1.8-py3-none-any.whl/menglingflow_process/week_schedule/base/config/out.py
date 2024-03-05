from menglingtool.time_tool import TimeTool
import re

class Out:
    colmap = {'task': 'varchar',
              'start_time': 'varchar',
              'end_time': 'varchar',
              'running_time': 'float',
              'out': 'text'}

    def __init__(self, task, start_time, end_time, running_seconds, out):
        self.task = task
        self.sd = TimeTool(start_time)
        self.ed = TimeTool(end_time)
        self.t = float(running_seconds)
        # 清洗异常字符
        self.out = re.sub(r'[\x00-\x1F\x7F]', '', out)

    def get(self):
        return {
            'task': self.task,
            'start_time': self.sd.to_txt(),
            'end_time': self.ed.to_txt(),
            'running_time': self.t,
            'out': self.out
        }


class Err(Out):
    colmap = {
        **Out.colmap,
        'index': 'int'
    }

    def __init__(self, index, task, start_time, end_time, running_seconds, out):
        super().__init__(task, start_time, end_time, running_seconds, out)
        self.index = int(index)

    def get(self):
        return {
            **super().get(),
            'index': self.index
        }
