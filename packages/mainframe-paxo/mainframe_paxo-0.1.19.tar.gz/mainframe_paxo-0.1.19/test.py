import subprocess
import threading
import time
from queue import Empty, SimpleQueue

p = subprocess.Popen(
    [
        "python",
        "-c",
        'import time; time.sleep(0.01);print("hello");time.sleep(0.01);print("bob")',
    ],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if p.stdout is not None:
    q = SimpleQueue()

    def enqueue_output(out, queue):
        for line in iter(out.readline, b""):
            print(f"got: {line!r}")
            queue.put(line)
            if not line:
                break
        queue.put(None)

    t = threading.Thread(target=enqueue_output, args=(p.stdout, q))
    t.start()
    while True:
        try:
            dude = q.get_nowait()
            print(f"got: {dude!r}")
            if dude is None:
                break
        except Empty:
            time.sleep(0.01)
