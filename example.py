from BaseThreading import BaseThreading


class NumbersThreading(BaseThreading):
    def process(self, row):
       pass
       # Do Something here !!


nt = NumbersThreading(
    raw_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], number_of_threads=28,options={})
nt.start()
