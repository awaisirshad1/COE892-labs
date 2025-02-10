import rover_utils as rvr


def sequential_rovers_part1(rover_moves: list, map_contents: list):
    resulting_maps = []
    for i in range(1, 11):
        resulting_maps.append(rvr.draw_rover_path_part1(rover_moves[i-1], map_contents))
    # print(f'resulting maps:{resulting_maps}')
    for i in range(1, 11):
        rvr.print_path_to_file('../sequential/part1', i, resulting_maps[i-1])
    return


def sequential_rovers_part2(rover_moves: list, map_contents: list):
    resulting_map, valid_pins = rvr.draw_rover_path_part2(rover_moves[0], map_contents, False)
    # for i in range(1, 11):
    #     resulting_maps.append(rvr.draw_rover_path_part2(rover_moves[i-1], map_contents))
    # # print(f'resulting maps:{resulting_maps}')
    # for i in range(1, 11):
    rvr.print_path_to_file('../sequential/part2', 1, resulting_map)
    print(f'valid pins for sequential computation:{valid_pins}')
    return
