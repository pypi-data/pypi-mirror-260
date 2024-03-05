def check_consecuitve_1s(input_string):
    state = 0
    for bit in input_string:
        if state == 0 and bit == '1':
            state = 1
        elif state == 1 and bit == '1':
            state = 2
        elif state == 2 and bit == '1':
            state = 3
            break
        else:
            state = 0  # Reset state to 0 if the bit is : 0
    return state == 3

def main():
    inp = input('Enter the bit to check consecutive 1\'s: ')
    if check_consecuitve_1s(inp):
        print('The bits contains consecutive 1\'s three times')
    else:
        print('The bits not contains consecutive 1\'s three times')

if  __name__=='__main__':
    main()