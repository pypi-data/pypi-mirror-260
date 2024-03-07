import time
# from pympler import asizeof
from single.nest import Queue
from single.nest import struct_queue_name
from single.nest import SchedulerInterface, StorerInterface


# class Transceiver:
class Distributor:

    def __init__(self):
        self.seed_queue = Queue()

    @property
    def queue_names(self):
        return tuple(self.__dict__.keys())

    @property
    def used_memory(self):
        return asizeof.asizeof(self)

    def create_queue(self, queue_name: str):
        self.__setattr__(queue_name, Queue())

    def get_queue(self, queue_name: str):
        return self.__getattribute__(queue_name)

    def deal_item(self, item):
        icn = item.__class__.__name__
        if icn == "Seed":
            self.seed_queue.push(item)
        elif getattr(item, "table_name", None):
            queue_name = struct_queue_name(icn, item.table_name)
            getattr(self, queue_name).push(item.serialization)

    def distribute(self, callback, *args, **kwargs):
        iterable = callback(*args, **kwargs)
        if not iterable:
            return None
        for result in iterable:
            self.deal_item(result)
        return True


class Scheduler:

    def schedule_task(self, distribute):

        if not issubclass(self.__class__, SchedulerInterface):
            return None

        if not getattr(self, "schedule", None):
            raise Exception("not have schedule function!")

        while not self.stop:

            if self.queue.length < self.length:
                distribute(self.schedule)

            else:
                print("------------")
                time.sleep(15)


class Spider:

    def __init__(self, queue):
        self.queue = queue
        self.spider_in_progress = Queue()

    def spider_task(self, stop_event, distribute, func, item):
        while not stop_event.is_set():
            seed = self.queue.pop()
            if not seed:
                time.sleep(3)
                continue
            try:
                self.spider_in_progress.push(1)
                distribute(func, item, seed)
            except Exception as e:
                print(e)
            finally:
                self.spider_in_progress.pop()


class Storer:

    def store_task(self, stop_event, last_event, distribute):

        if not issubclass(self.__class__, StorerInterface):
            return None

        if not getattr(self, "store", None):
            raise Exception("not have store function!")

        while not stop_event.is_set():
            if last_event.is_set() or self.queue.length > self.length:
                data_list = []
                data_length = min(self.queue.length, self.length)
                for _ in range(data_length):
                    data = self.queue.pop()
                    data_list.append(data)
                if data_list:
                    distribute(self.store, data_list)
