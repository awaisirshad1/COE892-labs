import rover_utils as rvr
import threading


def map_rover_moves(thread_index: int, rover_moves: str, map_contents: list, path_for_ouput: str):
    resulting_map = rvr.draw_rover_path_part1(rover_moves, map_contents)
    rvr.print_path_to_file(path_for_ouput, thread_index, resulting_map)


def parallel_rovers_part1(rover_moves: list, map_contents: list):
    threads = []
    for thread_index in range(1, 11):
        curr_thread = threading.Thread(target=map_rover_moves, args=(thread_index, rover_moves[thread_index-1], map_contents, '../parallel/part1'))
        threads.append(curr_thread)
        curr_thread.start()
    for t in threads:
        t.join()
    return


def parallel_rovers_part2(rover_moves: list, map_contents: list):
    result, valid_pins = rvr.draw_rover_path_part2(rover_moves[0], map_contents, True)
    rvr.print_path_to_file('../parallel/part2', 1, result)
    print(f'valid pins for parallel computation:{valid_pins}')
    # threads = []
    # for thread_index in range(1, 11):
    #     curr_thread = threading.Thread(target=map_rover_moves,
    #                                    args=(thread_index, rover_moves[thread_index - 1], map_contents, '../parallel/part2'))
    #     threads.append(curr_thread)
    #     curr_thread.start()
    # for t in threads:
    #     t.join()
    # return
