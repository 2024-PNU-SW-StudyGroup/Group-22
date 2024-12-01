# 객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라


# 함수가 전혀 제너릭하지 않다.
class InputData:
    def read(self):
        raise NotImplementedError
    

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
    

    def read(self):
        with open(self.path) as f:
            return f.read()
        

class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
    

    def map(self):
        raise NotImplementedError
    

    def reduce(self, other):
        raise NotImplementedError
    

# class LineCountWorker(Worker):
#     def map(self):
#         data = self.input_data.read()
#         self.result = data.count('\n')
    

#     def reduce(self, other):
#         self.result += other.result


import os

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


from threading import Thread


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


# def mapreduce(data_dir):
#     inputs = generate_inputs(data_dir)
#     workers = create_workers(inputs)
#     return execute(workers)


# 객체를 구성할 수 있는 제너릭한 방법이 필요하다
# 다른 언어에서는 다형성을 활용해 이 문제를 해결할 수 있다.
# 파이썬에서는 생성자 메서드가 __init__ 밖에 없다.
# 이 문제를 해결하는 가장 좋은 방법은 클래스 메서드 다형성을 사용하는 것이다.


class GenericInputData:
    def read(self):
        raise NotImplementedError
    

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError
    

class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
    

    def read(self):
        with open(self.path) as f:
            return f.read()
    
    # @classmethod 데코레이터 사용, 첫번째 인자로 cls를 받는다.
    # 데코레이터: 함수를 인자로 받아 새로운 함수를 반환하는 함수
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
    

    def map(self):
        raise NotImplementedError
    

    def reduce(self, other):
        raise NotImplementedError
    

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers
    

class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    

    def reduce(self, other):
        self.result += other.result

    
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)