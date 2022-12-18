import threading
from . models import *

class CreateItemThread(threading.Thread):

    def __init__(self , total ):
        self.total = total
        threading.Thread.__init__(self)

    def run(self):
        try:
            print('Thread Execution Started')

        except Execution as e:
            print(e)