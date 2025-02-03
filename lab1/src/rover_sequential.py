import rover_utils as rvr


def sequential_rovers():
    rover_path_url = "https://coe892.reev.dev/lab1/rover"
    map1_contents = rvr.extract_map_into_array('../map1.txt')
    print(f'map1_contents:{map1_contents}')
    rover_moves = []
    # get paths of all rovers, store in an array
    for i in range(1, 11):
        rover_moves.append(rvr.extract_rover_moves(rover_path_url, i))
    print(f'rover_moves:{rover_moves}')
    resulting_maps = []
    for i in range(1, 11):
        resulting_maps.append(rvr.draw_rover_path(rover_moves[i-1], map1_contents))
    print(f'resulting maps:{resulting_maps}')
    for i in range(1, 11):
        rvr.print_path_to_file('../sequential', i, resulting_maps[i-1])
    return
