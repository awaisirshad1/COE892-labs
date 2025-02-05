import rover_utils as rvr


def sequential_rovers_part1(rover_moves: list, map_contents: list):
    resulting_maps = []
    for i in range(1, 11):
        resulting_maps.append(rvr.draw_rover_path(rover_moves[i-1], map_contents, False))
    # print(f'resulting maps:{resulting_maps}')
    for i in range(1, 11):
        rvr.print_path_to_file('../sequential/part1', i, resulting_maps[i-1])
    return


def sequential_rovers_part2(rover_moves: list, map_contents: list):
    resulting_maps = []
    for i in range(1, 11):
        resulting_maps.append(rvr.draw_rover_path(rover_moves[i-1], map_contents, True))
    # print(f'resulting maps:{resulting_maps}')
    for i in range(1, 11):
        rvr.print_path_to_file('../sequential/part2', i, resulting_maps[i-1])
    return