"""MainShortcuts - \u043D\u0435\u0431\u043E\u043B\u044C\u0448\u0430\u044F \u0431\u0438\u0431\u043B\u0438\u043E\u0442\u0435\u043A\u0430 \u0434\u043B\u044F \u0443\u043F\u0440\u043E\u0449\u0435\u043D\u0438\u044F \u043D\u0430\u043F\u0438\u0441\u0430\u043D\u0438\u044F \u043A\u043E\u0434\u0430
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlay_InfoCh"""

__version_tuple__=(1,6,66)
__import_data__={
  "import MainShortcuts.{name} as {name}":[
    "dict",
    "dir",
    "file",
    "json",
    "list",
    "os",
    "path",
    "proc",
    "str",
    ],
  "from MainShortcuts.{name} import {name}":[
    "cfg",
    "dictplus",
    "fileobj",
    ],
  "{name}=main.{name}":[
    "cd",
    "clear",
    "cls",
    "exit",
    "pwd",
    ]
  }
__depends__={
  "required":[
    "json",
    "os",
    "platform",
    "shutil",
    "subprocess",
    "sys",
    ],
  "optional":[
    "colorama",
    "cPickle",
    "hashlib",
    "pickle",
    "toml",
    ]
  }
__scripts__=[
  "MS-getCore",
  "MS-getCoreMini",
  "MS-jsonC",
  "MS-jsonP",
  "MS-mkdir",
  ]
__all__=[]
__import_errors__={}
import MainShortcuts.main as main
for code,names in __import_data__.items():
  for name in names:
    try:
      exec(code.format(name=name))
      __all__.append(name)
    except Exception as e:
      __import_errors__[name]=e
__all__.sort()
__version__="{}.{}.{}".format(*__version_tuple__)
del code,names,name
