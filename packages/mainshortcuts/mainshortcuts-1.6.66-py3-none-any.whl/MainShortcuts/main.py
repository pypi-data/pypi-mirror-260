# MainShortcuts by MainPlay YT
# https://t.me/MainPlay_YT
import MainShortcuts.os as m_os
import os as _os
import sys as _sys
# Универсальные команды
exit=_sys.exit
cd=_os.chdir
pwd=_os.getcwd
# Команды для разных ОС
if m_os.platform=="Windows": # Windows
  def clear():
    _os.system("cls")
  cls=clear
elif m_os.platform=="Linux": # Linux
  def clear():
    _os.system("clear")
  cls=clear
elif m_os.platform=="Darwin": # MacOS
  def clear():
    raise Exception("This feature is not available on the current operating system")
  cls=clear
else: # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \""+m_os.platform+"\"",file=_sys.stderr)
