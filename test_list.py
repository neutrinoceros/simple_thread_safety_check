# run with pytest + pytest-repeat as
# pytest --count 100 test_list.py

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

N_THREADS = 4

def test_list_append():
    barrier = Barrier(N_THREADS)
    lst = []

    def closure():
        item = uuid4()
        barrier.wait()
        lst.append(item)
        return item

    with ThreadPoolExecutor(max_workers=N_THREADS) as exc:
        futures = [exc.submit(closure) for _ in range(N_THREADS)]

    results = [f.result() for f in futures]
    assert len(lst) == len(results) == N_THREADS


def test_list_plusequal():
    barrier = Barrier(N_THREADS)
    lst = []

    def closure():
        nonlocal lst
        item = uuid4()
        barrier.wait()
        lst += [item]
        return item

    with ThreadPoolExecutor(max_workers=N_THREADS) as exc:
        futures = [exc.submit(closure) for _ in range(N_THREADS)]

    results = [f.result() for f in futures]
    assert len(lst) == len(results) == N_THREADS
