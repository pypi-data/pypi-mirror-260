def gen_lang(productions, current_string):
    if not any(production[0] in current_string for production in productions):
        print(current_string)
        return
    for production in productions:
        if production[0] in current_string:
            new_string = current_string.replace(
                production[0], production[1], 1)
            gen_lang(productions, new_string)


productions = [('S', 'AB'), ('A', 'a'), ('B', 'b')]
start_symbol = 'S'
initial_string = start_symbol
gen_lang(productions, initial_string)
