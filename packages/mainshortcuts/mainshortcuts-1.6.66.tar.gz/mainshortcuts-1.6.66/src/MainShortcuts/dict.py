def path(v,path,sep="/"):
  for k in path.split(sep):
    if isinstance(v,dict):
      v=v[k]
    else:
      v=v[int(k)]
  return v
def swap(i):
  r={}
  for k,v in i.items():
    r[v]=k
  return r
def sort(d,*args,**kwargs):
  keys=list(d.keys)
  keys.sort(*args,**kwargs)
  r={}
  for k in keys:
    r[k]=d[k]
  return r
def reverse(d):
  keys=list(d.keys())[::-1]
  r={}
  for k in keys:
    r[k]=d[k]
  return r
