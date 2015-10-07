import os
import uuid
from shutil import rmtree
from tempfile import gettempdir

__author__ = 'elon'


def _randompath(basedir):
    randstr = str(uuid.uuid4())
    path = os.path.join(basedir, randstr)

    if os.path.exists(path):
        path = _randompath(basedir)

    return path

def _make_path(path, basedir):
    if basedir is None:
        basedir = gettempdir()
    path = path
    if path is None:
        path = _randompath(basedir)

    return path


class TempPath(str):
    def __init__(self):
        self.in_context = False
        # super(TempPath, self).__init__(path)

    def close(self):
        raise NotImplementedError()

    def __enter__(self):
        self.in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.in_context:
            self.close()

    def __del__(self):
        self.close()


def temppath(path=None, basedir=None):
    inst = str.__new__(TempPath, _make_path(path, basedir))
    TempPath.__init__(inst)

    return inst


class TempDirPath(TempPath):
    def __new__(cls, *args, **kwargs):
        return super(TempDirPath, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        try:
            os.makedirs(self)
        except OSError:
            pass

        super(TempDirPath, self).__init__()
        self.rmtree = rmtree  # This ensures rmtree is still available when a TempDirPath-instance is destroyed

    def tempfilepath(self, *args, **kwargs):
        return tempfilepath(basedir=self, *args, **kwargs)

    def close(self):
        try:
            self.rmtree(self)
        except OSError:
            pass


def tempdirpath(path=None, basedir=None):
    inst = str.__new__(TempDirPath, _make_path(path, basedir))
    TempDirPath.__init__(inst)

    return inst


class TempFilePath(TempPath):
    def __new__(cls, *args, **kwargs):
        return super(TempFilePath, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super(TempFilePath, self).__init__()
        self.remove = os.remove  # This ensures remove is still available when a TempFilePath-instance is destroyed

    def close(self):
        try:
            self.remove(self)
        except OSError:
            pass


def tempfilepath(path=None, basedir=None):
    inst = str.__new__(TempFilePath, _make_path(path, basedir))
    TempFilePath.__init__(inst)

    return inst

