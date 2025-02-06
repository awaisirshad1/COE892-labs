import rover_utils as rvr
import threading


def map_rover_moves(thread_index: int, rover_moves: str, map_contents: list, disarm_all_mines: bool, path_for_ouput: str):
    resulting_map = rvr.draw_rover_path(rover_moves, map_contents, disarm_all_mines)
    rvr.print_path_to_file(path_for_ouput, thread_index, resulting_map)


def parallel_rovers_part1(rover_moves: list, map_contents: list):
    threads = []
    for thread_index in range(1, 11):
        curr_thread = threading.Thread(target=map_rover_moves, args=(thread_index, rover_moves[thread_index-1], map_contents, False, '../parallel/part1'))
        threads.append(curr_thread)
        curr_thread.start()
    for t in threads:
        t.join()
    return


def parallel_rovers_part2(rover_moves: list, map_contents: list):
    threads = []
    for thread_index in range(1, 11):
        curr_thread = threading.Thread(target=map_rover_moves,
                                       args=(thread_index, rover_moves[thread_index - 1], map_contents, True, '../parallel/part2'))
        threads.append(curr_thread)
        curr_thread.start()
    for t in threads:
        t.join()
    return
