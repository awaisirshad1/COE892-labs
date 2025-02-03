import rover_sequential as sequential
import time


def main():
    start = time.time()
    sequential.sequential_rovers()
    end = time.time()
    sequential_q1_execution_time = end - start
    print(f'Question 1 sequential execution time total:{sequential_q1_execution_time}')




if __name__ == '__main__':
    main()
    exit(0)
