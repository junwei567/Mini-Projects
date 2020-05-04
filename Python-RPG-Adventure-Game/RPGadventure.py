from libdw import sm
import random
import copy
import sys
from os import system, name


def travelling(pos):
    cave =[ ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], 
            ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|', 'X', 'X'], 
            ['#', '#', '#', '#', '#', ' ', ' ', '|', 'X', 'X'], 
            ['X', 'X', '|', ' ', '#', ' ', '#', '#', '#', '#'], 
            ['X', 'X', '|', ' ', '#', ' ', '#', '#', '#', '#'], 
            ['#', '#', '#', ' ', ' ', ' ', ' ', '|', 'X', 'X'], 
            ['#', '#', '#', ' ', ' ', ' ', ' ', '|', 'X', 'X'], 
            ['X', 'X', '|', '#', ' ', '#', ' ', '#', '#', '#'], 
            ['X', 'X', '|', ' ', ' ', '#', ' ', '#', '#', '#'], 
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'] ]
    
    if cave[pos[0]][pos[1]] == "#":
        return False
    elif cave[pos[0]][pos[1]] == "|":
        return "door"
    else:
        cave[pos[0]][pos[1]] = "$"

    for i in cave:
            print(" ")
            for j in i:
                print(j,end=" ") 
    print("\n")
    return True

def clear():
    if name == "nt":
        _ = system("cls")

def battle(knight,enemy):
    print("\nYou have entered a battle with " + str(enemy))
    while enemy.survival():
        if knight.hp() <= 0:
            print("You have perished...")
            sys.exit(0)
        
        print("You ATTACKED the " + str(enemy))
        enemy.defend(knight.attack())
        if enemy.survival():
            knight.dodge(enemy.attack())
    
class Slime:
    def __init__(self):
        self.name = "Slime"
        self.health = 5
        self.alive = True

    def survival(self):
        return self.alive

    def attack(self):
        return 1
    
    def defend(self, dmg):
        self.health -= dmg        
        print("{0} received {1} damage.".format(self.name, dmg))
        if self.health <= 0:
            print("\nThe slime DIED.")
            self.alive = False

    def __str__(self):
        return self.name


class Dragon:
    def __init__(self):
        self.name = "Vicious Dragon"
        self.health = 25
        self.alive = True

    def survival(self):
        return self.alive

    def attack(self):
        dmg = random.randint(3,5)
        return dmg
    
    def defend(self, dmg):
        self.health -= dmg        
        print("{0} received {1} damage.".format(self.name, dmg))
        if self.health <= 0:
            print("\nThe vicious Dragon FELL.")
            self.alive = False

    def __str__(self):
        return self.name


class Grunt:
    def __init__(self):
        self.name = "Skelton Grunt"
        self.health = 10
        self.alive = True

    def survival(self):
        return self.alive

    def attack(self):
        return 2
    
    def defend(self, dmg):
        self.health -= dmg        
        print("{0} received {1} damage.".format(self.name, dmg))
        if self.health <= 0:
            print("\nThe Skelton Grunt DIED.")
            self.alive = False

    def __str__(self):
        return self.name


class Boss:
    def __init__(self):
        self.name = "Skelton King"
        self.health = 30
        self.alive = True

    def survival(self):
        return self.alive

    def attack(self):
        return 5
    
    def defend(self, dmg):
        self.health -= dmg        
        print("{0} received {1} damage.".format(self.name, dmg))
        if self.health <= 0:
            print("\nThe Skelton King was SLAIN.")
            self.alive = False

    def __str__(self):
        return self.name


class Knight:
    def __init__(self):
        self.health = 30
        self.inventory = ["sword","necklace"]

    def ls_inventory(self):
        return self.inventory

    def pickup(self,item):
        self.inventory.append(item)

    def hp(self):
        hp = self.health
        return hp

    def attack(self):        
        if self.inventory[0] == "Legendard Holy Sword":
            dmg = 10
        elif self.inventory[0] == "sword":
            dmg = 5
        return dmg

    def dodge(self,dmg):
        print("\nYou attempt to dodge the enemy's attack!")
        print("Type L to dodge left or R to dodge right.")
        command = input(">>> ").lower()
        random_no = random.randint(0,1)
        if random_no == 0:
            enemy_atk = "l"
        else:
            enemy_atk = "r"

        if command != enemy_atk:
            self.health -= dmg
            print("\nYour dodge FAILED, the enemy struck you.")
            print("Your remaining health is " + str(self.health))
        else:
            print("\nYou DODGED and received no damage.")
    

class Adventure(sm.SM):

    def __init__(self):
        self.pos = [1,1]        
        self.start_state = ["travel",self.pos,Knight()]
        print("\nAnd so, the adventure begins")
        print("You have entered the evil king's lair, in hopes of saving humanity.\n")    
        print("Type W,A,S,D to move.")
        print("The walls are represented by # and the rooms are marked X")
        print("More instructions in README.")
        travelling(self.pos)
        self.TutorialRoom = True
        self.DamageRoom = True
        self.KeyRoom = True
                
    def get_next_values(self, state, inp):        
        next_state = copy.deepcopy(state)
        
        if state[0] == "battle":            
            if state[1] == [1,6] or state[1] == [2,6]:
                if self.TutorialRoom == True:
                    battle(next_state[2],Slime())
                    next_state[0] = "travel"
                    info = "You won! Press Enter to exit battle."
                    self.TutorialRoom = False
                    return next_state, info
                else:
                    next_state[0] = "travel"
                    info = "The room is empty. Press Enter to exit."
                    return next_state, info

            elif state[1] == [5,6] or state[1] == [6,6]:
                if self.KeyRoom == True:
                    battle(next_state[2],Grunt())
                    next_state[0] = "travel"
                    next_state[2].pickup("key")
                    info = "You won! The Grunt dropped a key. Press Enter to exit battle."
                    self.KeyRoom = False
                    return next_state, info
                else:
                    next_state[0] = "travel"
                    info = "The room is empty. Press Enter to exit."
                    return next_state, info

            elif state[1] == [3,3] or state[1] == [4,3]:
                if self.DamageRoom == True:
                    battle(next_state[2],Dragon())
                    next_state[0] = "travel"
                    next_state[2].pickup("Legendard Holy Sword")
                    info = "You won! The dragon dropped a sword. Press Enter to exit battle."
                    self.DamageRoom = False
                    return next_state, info
                else:
                    next_state[0] = "travel"
                    info = "The room is empty. Press Enter to exit."
                    return next_state, info

            elif state[1] == [8,3]:
                if "key" in next_state[2].ls_inventory():
                    battle(next_state[2],Boss())
                    next_state[0] = "victory"
                    info = "You won! Press Enter to exit."
                    return next_state, info 

            elif state[1] == [1,1]:
                next_state = ["quit",None,None]
                info = "You have exited the castle."
                return next_state, info

        elif state[0] == "travel":
            if inp == "d":
                state[1][1] += 1
            elif inp == "w":
                state[1][0] -= 1
            elif inp == "a":
                state[1][1] -= 1
            elif inp == "s":
                state[1][0] += 1
            
            check = travelling(state[1])
            if check == False:
                info = "You cant walk through walls. Press Enter to proceed."
                return next_state, info
            elif check == "door": 

                if state[1] == [8,2]:
                    if "key" in next_state[2].ls_inventory():
                        next_state[0] = "battle"                
                        print("You opened the door.")                        
                        info = "Press Enter to begin battle."
                    else:
                        print("The door is LOCKED.")
                        next_state[0] = "travel"
                        info = "Press Enter to proceed"

                else:
                    next_state[0] = "battle"                
                    print("You opened the door.")                    
                    info = "Press Enter to begin battle."
            else:
                next_state[1] = state[1]
                info = "Type W,A,S,D to move or I to view your inventory."
            

        elif state[0] == "victory":
            next_state = ["quit",None,None]
            print("Congratulations, you have vanquished the evil boss of the castle.")
            print("You have ascended as the new evil boss, cursed to wait for the next challenger to enter...")
            info = " "

        if inp == "q":
            next_state = ["quit",None,None]
            info = "Thanks for playing."
            return next_state, info

        if inp == "i":
            print("Your inventory: ")
            print(next_state[2].ls_inventory())
        
        return next_state, info

    def done(self, state):
        if state[0] == "quit":
            return True
        else:
            return False

    def run(self):
        self.start()
        while True:
            if (not self.done(self.state)):
                command = input(">>> ").lower()
                clear()
                output = self.step(command)
                print(output)

            else:
                break

        print("Good Game! Thanks for playing!")

game = Adventure()
game.run()