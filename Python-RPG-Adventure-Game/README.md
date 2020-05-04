Digital World 10.009 Final Assignment
===

This is an adventure game made with Python using a library called 'libdw' as a final assignment for the course 10.009 - The Digital World.

Ensure that you run the code below in your command prompt before starting the game.
```
pip install libdw
```

## RPG Adventure

### Table of Contents

1. Objective of the game
2. How to play the game
3. The code

## Game

This game starts out with top-down view of a castle. The # represents the walls while X represents a room in the castle. Player will explore around the castle, where they can go into any room and fight the inhabitants. 

The main objective of this game is to kill the boss of the castle, but in order to enter his room, player has to acquire a key from another room first. 

To play the game, player will type single letters. **W,A,S,D** to move around, **I** to look into their inventory, **Q** to quit the game. 

As a player enters a room, he would transition into combat mode, where he has to type either **L** or **R** to dodge. This means that there is a 50% chance the player will receive no damage from the enemy. After he defeats the enemy, he will go back into travel mode where he can move to other rooms to fight other enemies. The inspiration for this travel and combat modes came from my favourite childhood game, "Pokemon".


The Code
---
I made many classes for the different characters in my game. Below is an example of an enemy:

```codehilite=
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
            print("The slime died.")
            self.alive = False

    def __str__(self):
        return self.name
```
<br />

The class for Knight, which is the avatar the player will be playing as: 

```codehilite=
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
```
<br />



Here is the code for the map. The player's position will be mapped onto a 2D array, where the function checks whether the player hits into a wall or enters a door. The actual travelling code is done in the state machine portion.
```codehilite=
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
```
<br />

Here is the code for combat mode. The sys.exit command ends this program immediately when the player dies. I thought of having it go back to the state machine to go through the **done** function, but ultimately this was the easiest way.
```codehilite=
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

```
<br />

I wrote most of the decision as a state machine with the libdw library. It has 3 parts, excluding the initiatise function. The **done** function checks whether the game is finished, which will be happen either when the player wins or quits. The **run** function keeps the state machine looping to get the player's input as well as check if it is valid.

The main part of this code is the **get_next_values** function, where the state machine decides the next state/sequence based on player's input and player's location. 

The player starts at position [1,1] which represents the y,x position on the map. [1,1] will be the second index in the second list. If he moves left/right then code-wise he will stay in the same list, so pos[1] decrease/increase. If he moves up/down, then he will move into adjacent lists, so pos[0] decrease/increase. 

```codehilite=
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
```
<br />


All in all, i had a lot of fun making this game. The hardest part of this mini project was linking the travelling mode and combat mode together and ensuring that everything went well together. I learnt a lot more about object-oriented programming through this and how to properly structure my code.
Hope you had fun playing!


> Video of gameplay: https://youtu.be/wyiPxqHdHes



