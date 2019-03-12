#Import threading to do multithreading and time to calculate time of execution
import asyncio
import dateutil.relativedelta
import datetime
from abc import ABCMeta, abstractmethod
import threading
import time
#Import Queue which is a List but it is more efficient, we will use it in multithreading
from queue import Queue
# Lock Threads to avoid GIL Problem
thrlock = threading.Lock()


class BaseThreading:
    __metaclass__ = ABCMeta

    def __init__(self, raw_list, number_of_threads=4):
        self.raw_list = raw_list
        self.num_rows = len(list(raw_list))
        self.rowsQueue = Queue()
        self.number_of_threads = number_of_threads
        self.dead = False
        self.counter = 0
        self.start_at = time.time()
        self.loop = asyncio.get_event_loop()

    @abstractmethod
    def process(self, row):
        pass

    def start(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.progress(self.counter, self.num_rows, self.counter)
        self.create_jobs()
        self.create_workers()
        self.summary()

    def work(self):
        while not self.dead and not self.rowsQueue.empty():
            #Get the first
            row = self.rowsQueue.get()
            #Handle it
            self.process(row)
            #Informe others that this task is finished
            self.rowsQueue.task_done()
            self.counter += 1
            self.progress(self.counter, self.num_rows, self.counter)
            #Wait for 50ms

    def create_workers(self):
        #Loop to create the threads
        for i in range(self.number_of_threads):
            #Initiate a thread and associate it with work function
            worker = threading.Thread(target=self.work)
            #Make it alive until you kill it manually (Apply for difference between setDaemon true or false)
            worker.setDaemon(True)
            #Start the Thread
            worker.start()
            #Wait for 300ms, just for caution
            time.sleep(.3)
            worker.join()

    def create_jobs(self):
        for row in self.raw_list:
            self.rowsQueue.put(row)
        #self.rowsQueue.join()

    def summary(self):
        finished_at = time.time()
        dt1 = datetime.datetime.fromtimestamp(
            self.start_at)  # 1973-11-29 22:33:09
        dt2 = datetime.datetime.fromtimestamp(
            finished_at)  # 1977-06-07 23:44:50
        rd = dateutil.relativedelta.relativedelta(dt2, dt1)
        seconds_past = finished_at - self.start_at
        print("\nHere is your task summary :")
        print("Your task finished in %d hours, %d minutes and %d seconds" %
              (rd.hours, rd.minutes, rd.seconds))
        print(str(round(rd.seconds / seconds_past, 2))+" seconds per task")

    def progress(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()
