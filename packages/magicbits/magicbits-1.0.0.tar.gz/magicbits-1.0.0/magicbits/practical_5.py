def check_string_endswith_101(input_string):
    state = 0
    for bit in input_string[-1:-4:-1]:
        if state == 0 and bit == '1':
            state = 1
        elif state == 1 and bit == '0':
            state = 2
        elif state == 2 and bit == '1':
            state = 3

    return state == 3

def main():
    inp = input('Enter the bits to check: ') 
    if check_string_endswith_101(inp):
        print('The bits ends with 101...')
    else:
        print('The bits doesn\'t ends with 101...')

    print('Coded By Durani Mohammed Zaeem, Roll No: 557')

if  __name__=='__main__':
    main()