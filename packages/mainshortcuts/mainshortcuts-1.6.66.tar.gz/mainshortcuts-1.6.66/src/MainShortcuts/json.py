import MainShortcuts.path as m_path
import MainShortcuts.file as m_file
import json as _json
_print=print
def encode(data,mode="c",indent=2,sort=True,**kwargs): # Данные в текст
  if mode in ["c","compress","min","zip"]: # Сжатый
    t=_json.dumps(data,separators=[",",":"],sort_keys=sort,**kwargs)
  elif mode in ["pretty","p","print","max"]: # Развёрнутый
    t=_json.dumps(data,indent=int(indent),sort_keys=sort,**kwargs)
  else: # Без параметров
    t=_json.dumps(data,sort_keys=sort,**kwargs)
  return t
def decode(text,**kwargs): # Текст в данные
  return _json.loads(str(text),**kwargs)
def write(path,data,encoding="utf-8",force=False,**kwargs): # Данные в файл
  if m_path.info(path)["type"]=="dir" and force:
    m_path.rm(path)
  return m_file.write(path,encode(data,**kwargs),encoding=encoding)
def read(path,encoding="utf-8",**kwargs): # Данные из файла
  return decode(m_file.read(path,encoding=encoding),**kwargs)
def print(data,mode="p",**kwargs): # Вывести JSON в консоль
  _print(encode(data,mode=mode,**kwargs))
def sort(data): # Сортировать ключи словарей ({"b":1,"c":2,"a":3} -> {"a":3,"b":1,"c":2})
  return decode(encode(data,mode="c",sort=True))
def rebuild(text,**kwargs): # Перестроить JSON в тексте
  return encode(decode(text),**kwargs)
def rewrite(path,encoding="utf-8",**kwargs): # Перестроить JSON в файле
  return write(path,read(path,encoding=encoding),encoding=encoding,**kwargs)
