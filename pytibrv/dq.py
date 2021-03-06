##
# pytibrv/cm.py
#   tibrvcmTransport_XXX
#
# LAST MODIFIED : V1.1 20170220 ARIEN
#
# DESCRIPTIONS
# ------------------------------------------------------
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvcmTransport_CreateDistributedQueueEx
#   tibrvcmTransport_GetCompleteTime
#   tibrvcmTransport_GetUnassignedMessageCount
#   tibrvcmTransport_GetWorkerWeight
#   tibrvcmTransport_GetWorkerTasks
#   tibrvcmTransport_SetCompleteTime
#   tibrvcmTransport_SetTaskBacklogLimit
#   tibrvcmTransport_SetWorkerWeight
#   tibrvcmTransport_SetWorkerTasks
#
#
# CHANGED LOGS
# ------------------------------------------------------
# 20170220 V1.1 ARIEN arien.chen@gmail.com
#   REMOVE TIBRV C Header
#
# 20161226 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes

from .types import tibrv_status, tibrvTransport

from . import _load

from .api import _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvTransport, \
                 _c_tibrv_u16, _c_tibrv_u32, _c_tibrv_f64, \
                 _c_tibrv_str

from .status import TIBRV_INVALID_TRANSPORT, TIBRV_INVALID_ARG

from .cm import _c_tibrvcmTransport, tibrvcmTransport


# module variable
_rvdq = _load('tibrvcmq')


##-----------------------------------------------------------------------------
# CONSTANT
##-----------------------------------------------------------------------------
TIBRVCM_DEFAULT_COMPLETE_TIME       = 0
TIBRVCM_DEFAULT_WORKER_WEIGHT       = 1
TIBRVCM_DEFAULT_WORKER_TASKS        = 1
TIBRVCM_DEFAULT_SCHEDULER_WEIGHT    = 1
TIBRVCM_DEFAULT_SCHEDULER_HB        = 1.0
TIBRVCM_DEFAULT_SCHEDULER_ACTIVE    = 3.5
TIBRVCMQ_LIMIT_MSGS                 = 0
TIBRVCMQ_LIMIT_BYTES                = 1


##-----------------------------------------------------------------------------
# TIBRV API : tibrv/cm.h
##-----------------------------------------------------------------------------

##
_rvdq.tibrvcmTransport_CreateDistributedQueueEx.argtypes = [_ctypes.POINTER(_c_tibrvcmTransport),
                                                            _c_tibrvTransport,
                                                            _c_tibrv_str,
                                                            _c_tibrv_u32,
                                                            _c_tibrv_u32,
                                                            _c_tibrv_u16,
                                                            _c_tibrv_f64,
                                                            _c_tibrv_f64]

_rvdq.tibrvcmTransport_CreateDistributedQueueEx.restype = _c_tibrv_status

def tibrvcmTransport_CreateDistributedQueueEx(
        tx: tibrvTransport, cmName: str, workerWeight: int, workerTasks: int,
        schedulerWeight: int, schedulerHeartbeat: float,
        schedulerActivation: float) -> (tibrv_status, tibrvcmTransport):

    if tx is None or tx == 0:
        return TIBRV_INVALID_TRANSPORT, None

    if cmName is None or workerWeight is None or workerTasks is None \
       or schedulerWeight is None or schedulerHeartbeat is None \
       or schedulerActivation is None:
        return TIBRV_INVALID_ARG, None

    cmtx = _c_tibrvcmTransport(0)

    try:
        tx = _c_tibrvTransport(tx)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        name = _cstr(cmName)
        wrk_wt = _c_tibrv_u32(workerWeight)
        wrk_tasks = _c_tibrv_u32(workerTasks)
        sch_wt = _c_tibrv_u16(schedulerWeight)
        sch_hbt = _c_tibrv_f64(schedulerHeartbeat)
        sch_act = _c_tibrv_f64(schedulerActivation)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvdq.tibrvcmTransport_CreateDistributedQueueEx(
                    _ctypes.byref(cmtx), tx, name,
                    wrk_wt, wrk_tasks, sch_wt, sch_hbt, sch_act)

    return status, cmtx.value


def tibrvcmTransport_CreateDistributedQueue(tx: tibrvTransport, cmName: str) \
                            -> (tibrv_status, tibrvcmTransport):

    return tibrvcmTransport_CreateDistributedQueueEx(
                    tx, cmName,
                    TIBRVCM_DEFAULT_WORKER_WEIGHT,
                    TIBRVCM_DEFAULT_WORKER_TASKS,
                    TIBRVCM_DEFAULT_SCHEDULER_WEIGHT,
                    TIBRVCM_DEFAULT_SCHEDULER_HB,
                    TIBRVCM_DEFAULT_SCHEDULER_ACTIVE)


##
_rvdq.tibrvcmTransport_SetCompleteTime.argtypes = [_c_tibrvcmTransport, _c_tibrv_f64]
_rvdq.tibrvcmTransport_SetCompleteTime.restype = _c_tibrv_status

def tibrvcmTransport_SetCompleteTime(cmTransport: tibrvcmTransport, completeTime: float) -> tibrv_status:

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT

    if completeTime is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        tt = _c_tibrv_f64(completeTime)
    except:
        return TIBRV_INVALID_ARG

    status = _rvdq.tibrvcmTransport_SetCompleteTime(cmtx, tt)

    return status


##
_rvdq.tibrvcmTransport_GetCompleteTime.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_f64)]
_rvdq.tibrvcmTransport_GetCompleteTime.restype = _c_tibrv_status

def tibrvcmTransport_GetCompleteTime(cmTransport: tibrvcmTransport) -> (tibrv_status, float):

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    ret = _c_tibrv_f64(0)

    status = _rvdq.tibrvcmTransport_GetCompleteTime(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
_rvdq.tibrvcmTransport_SetWorkerWeight.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetWorkerWeight.restype = _c_tibrv_status

def tibrvcmTransport_SetWorkerWeight(cmTransport: tibrvcmTransport, workerWeight: int) -> tibrv_status:

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT

    if workerWeight is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        val = _c_tibrv_u32(workerWeight)
    except:
        return TIBRV_INVALID_ARG

    status = _rvdq.tibrvcmTransport_SetWorkerWeight(cmtx, val)

    return status


##
_rvdq.tibrvcmTransport_GetWorkerWeight.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetWorkerWeight.restype = _c_tibrv_status

def tibrvcmTransport_GetWorkerWeight(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT, None


    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetWorkerWeight(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
_rvdq.tibrvcmTransport_SetWorkerTasks.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetWorkerTasks.restype = _c_tibrv_status

def tibrvcmTransport_SetWorkerTasks(cmTransport: tibrvcmTransport, listenerTasks: int) -> tibrv_status:

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT

    if listenerTasks is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        val = _c_tibrv_u32(listenerTasks)
    except:
        return TIBRV_INVALID_ARG

    status = _rvdq.tibrvcmTransport_SetWorkerTasks(cmtx, val)

    return status


##
_rvdq.tibrvcmTransport_GetWorkerTasks.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetWorkerTasks.restype = _c_tibrv_status

def tibrvcmTransport_GetWorkerTasks(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetWorkerTasks(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
_rvdq.tibrvcmTransport_SetTaskBacklogLimit.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetTaskBacklogLimit.restype = _c_tibrv_status

def tibrvcmTransport_SetTaskBacklogLimit(cmTransport: tibrvcmTransport, limitType: int,
                                         limitValue: int) -> tibrv_status:

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT

    if limitValue is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        ty = _c_tibrv_u32(limitType)
        val = _c_tibrv_u32(limitValue)
    except:
        return TIBRV_INVALID_ARG

    status = _rvdq.tibrvcmTransport_SetTaskBacklogLimit(cmtx, ty, val)

    return status


def tibrvcmTransport_SetTaskBacklogLimitInBytes(cmTransport: tibrvcmTransport,
                                                limitBySizeInBytes: int) -> tibrv_status:

    return tibrvcmTransport_SetTaskBacklogLimit(cmTransport, TIBRVCMQ_LIMIT_BYTES, limitBySizeInBytes)


def tibrvcmTransport_SetTaskBacklogLimitInMessages(cmTransport: tibrvcmTransport,
                                                   limitByMessages: int) -> tibrv_status:

    return tibrvcmTransport_SetTaskBacklogLimit(cmTransport, TIBRVCMQ_LIMIT_MSGS, limitByMessages)


##
_rvdq.tibrvcmTransport_GetUnassignedMessageCount.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetUnassignedMessageCount.restype = _c_tibrv_status

def tibrvcmTransport_GetUnassignedMessageCount(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    if cmTransport is None or cmTransport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetUnassignedMessageCount(cmtx, _ctypes.byref(ret))

    return status, ret.value
