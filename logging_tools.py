import time


def log(*args):
    print(
        f"[{time.strftime('%y-%m-%d_%H:%M:%S')}]",
        ' '.join(map(lambda x: str(x), list(args)))
    )
