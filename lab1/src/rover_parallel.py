import rover_utils as rvr
import threading


def map_rover_moves(thread_index: int, rover_moves: str, map_contents: list):
    resulting_map = rvr.draw_rover_path(rover_moves, map_contents)
    rvr.print_path_to_file('../parallel/part1', thread_index, resulting_map)


def parallel_rovers(rover_moves: list, map_contents: list):
    threads = []
    for thread_index in range(1, 11):
        curr_thread = threading.Thread(target=map_rover_moves, args=(thread_index, rover_moves[thread_index-1], map_contents))
        threads.append(curr_thread)
        curr_thread.start()
    for t in threads:
        t.join()
    return
