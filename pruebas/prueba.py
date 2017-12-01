import multiprocessing
import time

class Test:
    muestra = 0
    def __init__(self):
        self.pool = multiprocessing.Pool(1)
        m = multiprocessing.Manager()
        self.queue = m.Queue()

    def subprocess(self):
        for i in range(10):
            print("Running",self.muestra)
            self.muestra += 1
            time.sleep(1)
        print("Subprocess Completed")

    def subprocess2(self):
        for i in range(10):
            print("Running2",self.muestra)
            self.muestra += 1
            time.sleep(1)
        print("Subprocess Completed")

    def start(self):
        self.pool.apply_async(func=self.subprocess)
        self.pool.apply_async(func=self.subprocess2)
        self.pool.apply_async(func=self.subprocess2)
        print("Subprocess has been started")
        self.pool.close()
        self.pool.join()

    def __getstate__(self):
        print("holii")
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        print("holii_2")
        self.__dict__.update(state)

if __name__ == '__main__':
    test = Test()
    test.start()