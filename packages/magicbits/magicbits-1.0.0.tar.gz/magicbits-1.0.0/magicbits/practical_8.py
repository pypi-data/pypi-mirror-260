class PDA:
    def __init__(self):
        self.stack = []
        self.transitions = {
            ('q0', 'w', 'Z'): [('q1', 'Zw')],
            ('q1', 'w', 'w'): [('q1', 'ww')],
            ('q1', 'C', 'w'): [('q2', '')],
            ('q2', 'w', 'w'): [('q2', '')],
            ('q2', '', 'Z'): [('q_accept', '')],
            # Add more transitions as needed
        }
        self.accept_states = {'q_accept'}
        self.current_state = 'q0'

    def process_input(self, input_str):
        for symbol in input_str:
            if (self.current_state, symbol, self.stack[-1] if self.stack else 'Z') in self.transitions:
                transition = self.transitions[(self.current_state, symbol, self.stack[-1] if self.stack else 'Z')][0]
                self.current_state, stack_update = transition
                if stack_update:
                    self.stack.extend(stack_update)
                else:
                    self.stack.pop()
            else:
                return False
        return self.current_state in self.accept_states

# Example usage:
pda = PDA()
input_str = 'wcw'  # Replace with any string in WCWR
result = pda.process_input(input_str)
print("Result:", result)
print('Coded By Durani Mohammed Zaeem, Roll No: 557')