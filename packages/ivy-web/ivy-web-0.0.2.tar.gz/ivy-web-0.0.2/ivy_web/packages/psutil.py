import js


class Process(object):
    def __init__(self, pid=None):
        raise NotImplementedError

def virtual_memory():
    raise NotImplementedError

def cpu_percent():
    raise NotImplementedError

def cpu_count(logical=True):
    return js.navigator.hardwareConcurrency
