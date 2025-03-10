import rover_utils as rvr

def deminer_compute_pin():



def main():
    demine_numbers = [1, 2]
    while(True):
        uinput = input('Enter the deminer number (1/2),  enter \'exit\' to exit:')
        if int(uinput) not in demine_numbers:
            print('incorrect demine number or input, please try again')
            continue
        elif str(uinput).lower() == 'exit':
            print('Goodbye!')
            break





if __name__ == '__main__':
    main()