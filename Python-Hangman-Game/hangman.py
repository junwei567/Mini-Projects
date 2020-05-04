from libdw import sm
import random
import copy
random.seed(567)

selection = [['b','a','n','a','n','a'],['a','p','p','l','e'],['g','r','a','p','e'],
['o','r','a','n','g','e'],['m','e','l','o','n']]
random_no = random.randint(0,4)
selected_fruit = selection[random_no]
masked_ans = []

for i in range(len(selected_fruit)):
    masked_ans.append("_")

# print(selected_fruit)

class Hangman(sm.SM):

    def __init__(self):
        self.start_state = [selected_fruit,masked_ans]
        print("Let's play Hangman! Guess a fruit by typing in single letters one at a time.")
        print("You have one hint. You can activate it by typing hint.")
        for i in self.start_state[1]:
            print(i,end=' ')
        print(" ")

    def get_next_values(self, state, inp):
        next_state = copy.deepcopy(state)
        if inp in next_state[1]:
            print("Guess another letter.")
        
        elif inp in next_state[0]:
            print("Correct!")

        else:
            print("Incorrect, try again.")

        counter = 0
        for i in next_state[0]:
            if inp == i:
                next_state[1][counter] = inp  
            counter += 1    

        for i in next_state[1]:
            print(i,end=' ')
        print(" ")

        output = next_state[1]
        return next_state, output

    def hint(self):
        #ONLY ONE HINT
        pass

    def done(self, state):
        if state[0] == state[1]:
            return True

        else:
            return False

    def run(self):
        self.start()
        while True:
            if (not self.done(self.state)):
                guess = input("Guess: ").lower()
                if guess == "hint":
                    self.hint()
                elif len(guess) != 1:
                    print("Invalid! Guess a single letter only!")
                elif guess.isalpha():
                    self.step(guess)
                else:
                    print("Invalid! Guess a letter!")

            else:
                break

        print("Good Game! Thanks for playing!")

game = Hangman()
game.run()


