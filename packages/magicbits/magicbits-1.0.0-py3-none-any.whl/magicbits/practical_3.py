import re

def generate_regex(grammar):
    regex_dict = {}
    for production in grammar:
        non_terminal, expression = production.split(' -> ')
        regex_dict[non_terminal] = expression

    def replace_non_terminals(match: re.Match):
        non_terminal = match.group(1)   
        return '(' + regex_dict[non_terminal] + ')'

    for non_terminal, expression in regex_dict.items():
        regex_dict[non_terminal] = re.sub(
            r'([A-Z]+)', replace_non_terminals, expression)

    final_regex = '^' + regex_dict['S'] + '$'
    return final_regex


# Example usage
grammar = [
    'S -> aA | bB',
    'A -> aA | bB | ε',
    'B -> bB | ε'
]

regex = generate_regex(grammar)
print("Regular Expression:", regex)
print("Coded By Durani Mohammed Zaeem, Roll No: 557")
