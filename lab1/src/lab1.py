import rover_utils as rvr
import rover_sequential
import rover_parallel
import time


def main():
    # preprocessing: get all our rover's moves and the contents of the map file
    rover_path_url = "https://coe892.reev.dev/lab1/rover"
    map1_contents = rvr.extract_map_into_array('../map1.txt')
    # print(f'map1_contents:{map1_contents}')
    rover_moves = []
    # get paths of all rovers, store in an array
    for i in range(1, 11):
        rover_moves.append(rvr.extract_rover_moves(rover_path_url, i))
    # print(f'rover_moves:{rover_moves}')
    # SEQUENTIAL EXECUTION FOR QUESTION 1 PART 1
    start = time.time()
    rover_sequential.sequential_rovers(rover_moves, map1_contents)
    end = time.time()
    sequential_q1_execution_time = end - start
    print(f'Question 1 sequential execution time total:{sequential_q1_execution_time}s')
    # PARALLEL EXECUTION FOR QUESTION 1 PART 2
    start = time.time()
    rover_parallel.parallel_rovers(rover_moves, map1_contents)
    end = time.time()
    parallel_q1_execution_time = end - start
    print(f'Question 1 parallel execution time total:{parallel_q1_execution_time}s')




if __name__ == '__main__':
    main()
    exit(0)
