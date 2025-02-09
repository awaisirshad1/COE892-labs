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
    # SEQUENTIAL EXECUTION FOR PART 1
    start = time.time()
    rover_sequential.sequential_rovers_part1(rover_moves, map1_contents)
    end = time.time()
    sequential_execution_time_part1 = end - start
    print(f'Question 1 sequential execution time total:{sequential_execution_time_part1}s')

    # PARALLEL EXECUTION FOR PART 1
    start = time.time()
    rover_parallel.parallel_rovers_part1(rover_moves, map1_contents)
    end = time.time()
    parallel_q1_execution_time = end - start
    print(f'Question 1 parallel execution time total:{parallel_q1_execution_time}s')


    diff_computation_times_part1 = abs(sequential_execution_time_part1 - parallel_q1_execution_time)
    percentage_diff_comp_times_part1 = (diff_computation_times_part1/((sequential_execution_time_part1 + parallel_q1_execution_time)/2)) * 100
    msg = f'The threading approach is faster by {percentage_diff_comp_times_part1}%, with a difference of {diff_computation_times_part1} seconds' \
        if sequential_execution_time_part1 > parallel_q1_execution_time \
        else f'The sequential approach is faster by {percentage_diff_comp_times_part1}%, with a difference of {diff_computation_times_part1} seconds'
    print(msg)

    # SEQUENTIAL EXECUTION FOR PART 2
    start = time.time()
    rover_sequential.sequential_rovers_part2(rover_moves, map1_contents)
    end = time.time()
    sequential_execution_time_part2 = end - start
    print(f'Question 2 sequential execution time total:{sequential_execution_time_part2}s')

    # PARALLEL EXECUTION FOR PART 2
    start = time.time()
    rover_parallel.parallel_rovers_part2(rover_moves, map1_contents)
    end = time.time()
    parallel_execution_time_part2 = end - start
    print(f'Question 2 parallel execution time total:{parallel_execution_time_part2}s')

    diff_computation_times_part2 = abs(sequential_execution_time_part2 - parallel_execution_time_part2)
    percentage_diff_comp_times_part2 = (diff_computation_times_part2 / (
                (sequential_execution_time_part2 + parallel_execution_time_part2) / 2)) * 100
    msg = f'The threading approach is faster by {percentage_diff_comp_times_part2}%, with a difference of {diff_computation_times_part2} seconds' \
        if sequential_execution_time_part2 > parallel_q1_execution_time \
        else f'The sequential approach is faster by {percentage_diff_comp_times_part2}%, with a difference of {diff_computation_times_part2} seconds'
    print(msg)


if __name__ == '__main__':
    main()
    exit(0)
