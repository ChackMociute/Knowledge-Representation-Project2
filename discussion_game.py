import os

from argumentation import ArgumentationFramework
from random import choice

class DiscussionGame:
    def __init__(self, af: ArgumentationFramework):
        self.af = af
        self.in_, self.out = set(), set()
    
    def play(self, argument=None):
        argument = choice(list(af.args)) if argument is None else argument
        while not self.termination(argument):
            os.system('cls')
            argument = self.turn(argument)
        self.display_winner()
    
    def termination(self, arg):
        self.find_valid_opp_arguments()
        if len(self.in_.intersection(self.out)) > 0 or arg in self.out or arg is None:
            self.win = True
            return True
        elif len(self.valid) == 0 and len(self.in_) > 0:
            self.win = False
            return True
        return False

    def turn(self, arg):
        self.prop_turn(arg)
        self.opp_turn()
        return self.select_arg()
    
    def prop_turn(self, arg):
        print("------------------------PROPONENT'S ARGUMENT------------------------")
        print(f"({arg}): {self.af.args[arg]}\n")
        self.in_.add(arg)
    
    def opp_turn(self):
        self.find_valid_opp_arguments()
        self.last_opp_arg = self.get_and_validate_input()
        self.out.add(self.last_opp_arg)
        print()
    
    def find_valid_opp_arguments(self):
        all_attacking_arguments = {
            b if a == arg else a for arg in self.in_ 
            for a, b in self.af.ar if a == arg or b == arg
        }
        self.valid = set(self.af.args).difference(self.out).intersection(all_attacking_arguments)
    
    def get_and_validate_input(self):
        self.display_valid()
        while True:
            inp = input("Your choice: ")
            if inp in self.valid: return inp
            print("\nInput does not match available options. Enter one of the following:\n\t", end='')
            print(' '.join([f"({a})" for a in self.valid]))
            print()
    
    def display_valid(self):
        print("----------------------------YOUR OPTIONS----------------------------")
        for val in self.valid:
            print(f"({val}): {self.af.args[val]}")
        print()
    
    def select_arg(self):
        attacking = {a for a, b in self.af.ar if b == self.last_opp_arg}
        if len(attacking) == 0: return
        attacking_not_out = {a for a in attacking if not a in self.out}
        return choice(list(attacking_not_out if len(attacking_not_out) > 0 else attacking))
    
    def display_winner(self):
        if self.win:
            print("Congratulations, you won the argument!")
        else:
            print("You have lost the argument within this argument framework.")
        


if __name__ == "__main__":
    import json

    # af = json.load(open('example-argumentation-framework.json'))
    af = json.load(open('argumentation3.json'))

    af = ArgumentationFramework(arguments=af['Arguments'], attack_relations=af['Attack Relations'])
    dg = DiscussionGame(af)
    dg.play()