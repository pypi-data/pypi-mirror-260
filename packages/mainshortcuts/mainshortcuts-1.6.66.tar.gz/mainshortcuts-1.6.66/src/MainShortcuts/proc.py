import os as _os
import subprocess as _subprocess
import sys as _sys
args=_sys.argv # Аргументы запуска программы
pid=_os.getpid() # PID текущего процесса
var=_os.environ # Переменные всего процесса
def run(a,*args,**kwargs): # Запустить процесс ("nano example.txt" -> ["nano","example.txt"])
  p=_subprocess.Popen(a,*args,stdout=_subprocess.PIPE,stderr=_subprocess.PIPE,**kwargs)
  code=p.wait()
  out,err=p.communicate()
  if type(out)==bytes:
    out=out.decode("utf-8")
  out=str(out)
  if type(err)==bytes:
    err=err.decode("utf-8")
  err=str(err)
  r={
    "code":code,
    "output":out,
    "out":out,
    "error":err,
    "err":err,
    "stdout":out,
    "stderr":err,
    "c":code,
    "o":out,
    "e":err,
    }
  return r
