"""import winreg as _winreg
class open:
  def __init__(self,path):
    self.path=path
  def __setattr__(self,k,v):
    if k=="path":
      v=v.replace("/","\\")
      self._root=getattr(_winreg,v.split("\\")[0].upper())
      self._path="\\".join(v.split("\\")[1:])
      self.key=_winreg.OpenKey(self._root,self._path,0,_winreg.KEY_ALL_ACCESS)
    self.__dict__[k]=v
# Создаем строковую запись
winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, "C:\\Program Files\\Python39")

# Закрываем реестр
winreg.CloseKey(key)
"""
