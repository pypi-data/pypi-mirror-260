from .config.sqlt import get_sqlt, STATUS, ARG, OUT, ERR, SqlData, sqlRetryFunc
from .config.status import Status
from .config.arg import Arg
from .config.out import Out, Err


@sqlRetryFunc
def table_init():
    with get_sqlt() as sqlt:
        sqlt.createTable(ARG, Arg.colmap.keys(), Arg.colmap, key='task')
        sqlt.createTable(STATUS, Status.colmap.keys(), Status.colmap, key='task')
        sqlt.commit()


@sqlRetryFunc
def set_arg(arg, reload_status):
    with get_sqlt() as sqlt:
        sqlt.delete(ARG, where=f"task='{arg.task}'")
        sqlt.insert(ARG, SqlData([arg.get()]))
        if reload_status:
            sqlt.delete(STATUS, where=f"task='{arg.task}'")
        sqlt.commit()

@sqlRetryFunc
def saveOut(task, sd, ed, running_seconds, out):
    with get_sqlt() as sqlt:
        outer = Out(task, sd, ed, running_seconds, out)
        sqlt.create_insert(OUT, [outer.get()], colmap=Out.colmap)
        sqlt.commit()

@sqlRetryFunc
def saveErr(task, i, sd, ed, running_seconds, outerr):
    with get_sqlt() as sqlt:
        errer = Err(i, task, sd, ed, running_seconds, outerr)
        sqlt.create_insert(ERR, [errer.get()], colmap=Err.colmap)
        sqlt.commit()

@sqlRetryFunc
def setStatus(status):
    with get_sqlt() as sqlt:
        sqlt.delete(STATUS, where=f"task='{status.task}'")
        sqlt.insert(STATUS, SqlData([status.get()]))
        sqlt.commit()

@sqlRetryFunc
def restartTask(task):
    with get_sqlt() as sqlt:
        sqlt.delete(STATUS, where=f"task='{task}'")
        sqlt.commit()
