import json


class Arg:
    colmap = {'task': 'varchar',
              'stop': 'bool',
              'max_err_num': 'int',
              'emails': 'varchar',
              'err_week': 'int',
              'timeout': 'int',
              'power': 'int',
              'ml': 'text',
              'week': 'text'}

    def __init__(self, task, stop, max_err_num, emails, err_week, timeout, power, ml, week, **_):
        self.task = task
        self.stop = stop in ['true', 'True']
        self.max_err_num = int(max_err_num)
        self.emails = emails.split(',')
        self.err_week = int(err_week)
        self.timeout = int(timeout)
        self.power = int(power)
        self.ml = ml
        self.week = json.loads(week) if type(week) == str else dict(week)

    def get(self) -> dict:
        return {
            'task': self.task,
            'stop': self.stop,
            'max_err_num': self.max_err_num,
            'emails': self.emails,
            'err_week': self.err_week,
            'timeout': self.timeout,
            'power': self.power,
            'ml': self.ml,
            'week': self.week
        }
