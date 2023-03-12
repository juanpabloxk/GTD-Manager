import time

def log(*args):
  args_joined = ' '.join(map(lambda x: str(x), list(args)))
  print(f"[{time.strftime('%y-%m-%d_%H:%M:%S')}]", args_joined)
