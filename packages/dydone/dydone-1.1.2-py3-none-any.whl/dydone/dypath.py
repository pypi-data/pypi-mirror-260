import os
import shutil

from dydone import dycli

def norm(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))

def join(*paths: str) -> str:
    return norm(os.path.join(*map(norm, paths)))

def filename(path: str) -> str:
    return os.path.splitext(norm(path))[0]

def basename(path: str) -> str:
    return filename(os.path.basename(norm(path)))

def isdir(path: str) -> bool:
    return os.path.isdir(norm(path))

def isfile(path: str) -> bool:
    return os.path.isfile(norm(path))

def collide(path: str) -> bool:
    path = norm(path)
    return isfile(path) or (isdir(path) and len(os.listdir(path)) > 0)

def remove(path: str) -> None:
    path = norm(path)
    shutil.rmtree(path) if os.path.isdir(path) else os.unlink(path)

def removeall(*paths: str) -> None:
    for path in paths: remove(path)

def reconcile(*paths: str) -> None:
    conflicts = list(filter(collide, paths))
    if len(conflicts) > 0:
        prompt = f"Agree to {dycli.warn('remove')} conflicts?" + 2*os.linesep
        if dycli.dilemma(prompt + dycli.indent(os.linesep.join(conflicts))):
            removeall(*conflicts)
        else: exit()

def secure(*paths: str) -> None:
    reconcile(*paths)
    for path in paths:
        os.makedirs(path, exist_ok=True)
