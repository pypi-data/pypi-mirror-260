def is_equal_ones_zeros(input_string):
    state, one_count, zero_count = (False, 0, 0)

    for char in input_string:
        if char == '1':
            one_count += 1
        elif char == '0':
            zero_count += 1
        else:
            return False
    if one_count == zero_count:
        state = True
    return state

def main():
    input_string = input("Enter a string of 1s and 0s: ")
    if is_equal_ones_zeros(input_string):
        print("The string has an equal number of 1s and 0s.")
    else:
        print("The string does not have an equal number of 1s and 0s.")
    print('Coded By Durani Mohammed Zaeem, Roll No: 557')

if __name__ == "__main__":
    main()
