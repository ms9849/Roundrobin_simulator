from enum import Enum
from multiprocessing import Process, Condition
import time
PROC_COND = Enum('PROC_COND', ['RUN', 'WAIT', 'EXIT', 'CREATE'])

"""
Pool과 Process 2가지 클래스를 제공하지만, 새로운 클래스를 작성하는 것이 요구 사항에
포함되어 있었으므로, Process 클래스를 이용하여 생성한 프로세스를 래핑하는 방식으로 작성.
상속은 이용하지 않는 편이 좋다고 판단. is a 관계를 충분히 만족하지만 안쓰고 넘길수 있다면
안쓰는게 낫다는 개인적 견해
"""
# pid는 내부의 process 객체가 갖고있음.
class MyProcess(): 
    def __init__(self, burstTime, num1, num2, sharedValue, prior=1): 
        self.process = Process(target=Job, args= (self, num1, num2, sharedValue))
        
        # 내부에 condition 객체도 가지고 있음.
        self.cond = Condition()
        self.burstTime = burstTime

        # 우선순위를 가지고는 있으나, Round Robin 기법에서는 필요하지 않다고 판단.
        self.prior = prior 

        # 열거형을 이용하여 프로세스의 상태를 나타내도록 함, RUN , WAIT, EXIT, CREATE 4가지 상태가 존재함/
        self.status = PROC_COND.CREATE
        time.sleep(1)

    def start(self):
        self.process.start()
        print("Process just started, PID is",self.getPid())
        time.sleep(1)
        
    def wait(self):
        self.status = PROC_COND.WAIT
        self.cond.wait()
        time.sleep(1)

    def exit(self):
        self.status = PROC_COND.EXIT        
        self.process.terminate()
        print("Bye, Process! PID is",self.getPid(),
              "and process condition is",self.getStatus())
        time.sleep(1)

    def run(self):
        print("Run, PID is",self.getPid())
        with self.cond:
            self.cond.notify_all()
        self.status = PROC_COND.RUN
        time.sleep(1)
    
    def subBurstTime(self, TIME_QUANTUM):
        self.burstTime -= TIME_QUANTUM

    def getBurstTime(self):
        return self.burstTime
    
    def getPid(self):
        return self.process.pid
       
    def getStatus(self):
        return self.status

def Job(self, a, b, sharedValue):
    while True:
        with self.cond:
            # 작업 대기
            print("Job is just now waiting....\n")
            self.wait()

            #작업 공간
            print("Job is doing something..")
            result = a+b
            print("Calculated: ",result)
            sharedValue.value += result



