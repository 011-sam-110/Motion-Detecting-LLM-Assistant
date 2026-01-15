from speechToText import run
import threading
from queue import Queue

q = Queue()
t = threading.Thread(target=run, args=(q,))  
t.start()
t.join()  

result = q.get()
print(result)