from myqueue import MyQueue 
from process import MyProcess
import time
from multiprocessing import Manager

TIME_QUANTUM = 3

def Scheduler() :
    # 내부적으로 Job에서 수행된 덧셈들의 합을 저장할 예정. 예상 출력값은 94
    sharedValue = Manager().Value('i',0) 

    #생성된 프로세스들, 첫번째 인자는 burst_time, 2,3번째 인자는 덧셈을 수행할 두 정수, 4번째 인자는 모든 프로세스가 공유하는 sharedValue
    procs = [ MyProcess(5, 1, 2, sharedValue), MyProcess(11, 3, 4, sharedValue) , MyProcess(8, 5, 6, sharedValue), MyProcess(7, 7, 2, sharedValue) ]

    #프로세스들을 담고 관리할 큐
    queue = MyQueue()

    for i in procs :
        i.start()
        queue.push(i) # 프로세스 생성 후 큐에 등록 

    while not queue.empty(): 
        start = time.time()
        # pop 과 같음. 맨 앞의 프로세스 가져오기
        p = queue.get()

        # 최소한의 실행시간은 보장하는데, 아주 조금 넘길 수 있다는 생각이 든다.
        p.run() 
        while True:
            # TIME_QUANTUM 보다 시간이 더  지났다면, 혹은 내부의 실행시간이 완전히 지났다면.
            if time.time() - start >= TIME_QUANTUM or p.getBurstTime() - (time.time() - start) <= 0: 
                runTime = time.time() - start
                p.subBurstTime(TIME_QUANTUM)
                print("Burst time finished: ",runTime,"seconds\n")
                break

        if p.getBurstTime() <= 0:
            p.exit()
        else:
            queue.push(p)
    
    print("All Job has done!!!!")
    print("Shared Value is ", sharedValue.value)


if __name__ == '__main__':
    Scheduler()