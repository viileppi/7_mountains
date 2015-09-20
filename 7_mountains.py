#!/usr/bin/env python3
# -*- coding: UTF-8 -*-  
# 7 mountains text game 
import random
import time
import cmd
import sys
def clearScreen():
    print("%c[2J" % (27) + "%c[;H" % (27))
class Follower():
    def __init__(self, resources, followers):
        self.methods = [self.eat, self.seekshelter, self.sex_and_death, self.rotostele]
        self.resources = resources
        self.followers = followers
        self.alive = True
        self.age = 0
        self.posessions = 0
        self.happiness = 7
        #self.name = ""
        if self.resources["shelter"] < 1:
            self.alive = False
        else:
            self.resources["shelter"] -= 1
    def eat(self):
        if self.resources["food"] > 1:
            self.resources["food"] -= 1
        else:
            self.alive = False
    def seekshelter(self):
        if self.resources["shelter"] > 1:
            pass
        else:
            self.alive = False
    def sex_and_death(self):
        self.age += 1
        if self.age > 40 or self.alive == False:
            return "dead"
        if self.age > 2 and self.age < 35:
            return "kid"
    def rotostele(self):
        for rotos in p.crimes:
            if random.randint(0, int(self.happiness) * 10) == 0:
                p.crimes[rotos] += 1
        self.happiness -= sum(p.crimes.values()) / 4
            
class Farmari(Follower):
    # produces food
    name = "farmer"
    def __init__(self, resources, followers):
        Follower.__init__(self, resources, followers)
        self.methods.append(self.farm)
    def farm(self):
        self.resources["food"] += 8
        self.posessions += 1
class Builder(Follower):
    # produces shelter from bricks
    name = "builder"
    def __init__(self, resources, followers):
        Follower.__init__(self, resources, followers)
        self.methods.append(self.build)
    def build(self):
        if self.resources["brick"] > 0:
            self.resources["shelter"] += 4
            self.resources["brick"] -= 2
            self.posessions += 2

class Soldier(Follower):
    # puolustaa ja sotii
    name = "soldier"
    def __init__(self, resources, followers):
        Follower.__init__(self, resources, followers)
        self.name = "soldier"
    def sodi(self):
        killed = 0
        died = 0
        for Soldier in p.followers:
            if followers[Soldier].name == "soldier":
                r = random.randint(1, 2)
                if r == 1:
                    killed += 1
                    foo = p.enemies.pop()
                else:
                    self.alive = False
                    died += 1
        print(killed, "enemies killed")
        print(died, "soldiers died")
class Merchant(Follower):
    # trades food to resources
    name = "merchant"
    def __init__(self, resources, followers):
        Follower.__init__(self, resources, followers)
        self.methods.append(self.trade)
    def trade(self):
        self.resources["food"] -= 2
        self.resources["brick"] += 4
        self.posessions += 3
class Scout(Follower):
    name = "scout"
    def __init__(self, resources, followers):
        Follower.__init__(self, resources, followers)
        self.methods.append(self.spy)
    def spy(self):
        # Scoutt kuolevat helposti
        if random.randint(1, 2) == 2:
            self.alive = False
        if random.randint(1, 6) == 6:
            if p.informations_index <= len(p.informations):
                p.informations_index += 1
class Pelaaja:
    def __init__(self, resources, followers, professions):
        self.resources = resources
        self.followers = followers
        self.birthrate = 20
        self.professions = professions
        self.profession_names = []
        for profession in self.professions:
            self.profession_names.append(profession.name)
        self.tax = 0.02
        self.taxincome = 0
        self.crimes = {"theft" : 0, "arsony" : 0, "rape" : 0, "murder" : 0, "con" : 0}
        self.informations_index = 0
        self.informations = ["No information. Try training some scouts or pass few turns", "Scouts report: There are angry wildlings in nearby woods. You can start war against them by typing 'war'.", "Scouts report: There is an abandoned mine nearby. You can raid it by typing 'raid' (feature not available yet)"]
        self.punishments = ["jail", "hang", "behead", "scald", "pardon"]
        self.karma = 0

    def bornAndDie(self):
        kuolema = []
        for tyyppi in self.followers:
            for metodi in self.followers[tyyppi].methods:
                a = metodi()
                if a == "kid":
                    self.birthrate += 1
                if a == "dead":
                    kuolema.append(tyyppi)
        for vainaa in kuolema:
            del self.followers[vainaa]
    def collect_tax(self):
        self.taxincome = 0
        for hahmo in self.followers:
            if self.followers[hahmo].posessions - p.tax > 0:
                self.followers[hahmo].posessions -= p.tax
                self.taxincome += p.tax
            else:
                pass
            followers[hahmo].happiness = followers[hahmo].happiness - self.tax * 1
        return self.taxincome
resources = {"food" : 10, "shelter" : 10, "brick" : 10}
followers = {}
score = 0
professions = [Farmari, Builder, Merchant, Soldier, Scout]
beginwith = 40
p = Pelaaja(resources, followers, professions)
for resurssi in resources:
    resources[resurssi] = beginwith
p.enemies = []
for i in range(10):
    p.enemies.append(i)
class CmdShell(cmd.Cmd):
    intro = "Type 'tutorial' or 'help' to get started"
    prompt = ">"
    file = None
    war = False
    firstrun = True
    training_percent = {}
    tutorial_index = 0
    tutorial = False
    tutorial_list = [None, None, "First let's hit <tab> key twice. This will bring out the list of available commands. Then, type 'pr' and hit <tab> to autocomplete 'pray'.", "Using the autocomplete method punch in a sentence 'train farmer 25' and hit <enter> -this will set the amount of farmers to be trained to 25%.", "As you can see, the game automatically compensates the training rate for rest of the professions. Good, now the training is set. Let's change the tax rate by typing 'tax'.", "Type 'help' for in-game help or 'help <command> to view help for a certain command (don't forget the tab-autocomplete!). Now type 'pass' to finish the turn"]
    last_action = ""
    informations_index = 0
    color_reset='\033[0m'
    color_red=red='\033[31m'
    color_green='\033[32m'
    color_yellow='\033[93m'
    color_cyan='\033[36m'
    color_bold='\033[01m'

    for profession in p.professions:
        training_percent[profession.name] = 20
    def preloop(self):
        clearScreen()
        self.do_stats("foo")
    def emptyline(self):
        self.do_pass("foo")
    def resources(self):
        s = ""
        for resource in p.resources:
            s += resource + ": "
            if p.resources[resource] < 30:
                s += self.color_red + str(p.resources[resource]) + self.color_reset + " "
            if p.resources[resource] > 75:
                s += self.color_green + str(p.resources[resource]) + self.color_reset + " "
            else:
                s += self.color_yellow + str(p.resources[resource]) + self.color_reset + " "
        return s
    def postcmd(self, stop, line):
        if self.tutorial == True:
            self.tutorial_index += 1
        if p.informations_index > self.informations_index:
            last_action = "Scouts have provided new information. Type 'scout' to view information."
        for profession in professions:
            for i in range(int(self.training_percent[profession.name] / 100 * p.birthrate)):
                p.followers[len(p.followers) + 1] = profession(resources, followers)
                p.birthrate -= 1
        if line[0:4] != "help" and line[0:5] != "story":
            clearScreen()
            self.do_stats("foo")
            print(self.last_action)
            if self.tutorial_index != 0:
                print(self.color_cyan, "Tutorial:", self.tutorial_list[self.tutorial_index], self.color_reset)
            if self.tutorial_index >= len(self.tutorial_list) -1:
                self.tutorial_index = 0
                self.tutorial = False
        if stop == True:
            return True
    def laske_sanakirja(self, sanakirja):
        s = 0
        for item in sanakirja:
            s += sanakirja[item]
        return s
    def do_train(self, s):
        print(self.training_percent)
        s = s.split(" ")
        for profession in p.profession_names:
            try:
                if s[1].isdigit() == True and s[0] == profession:
                    if int(s[1]) > 100:
                        self.last_action = "Error: use values 0-100%"
                    else:
                        self.training_percent[profession] = int(s[1])
                        while sum(self.training_percent.values()) > 100:
                            for item in self.training_percent:
                                if item != s[0] and self.training_percent[item] >= 1:
                                    self.training_percent[item] -= 1

                if s[0] == profession and len(s) == 1:
                    self.training_percent[profession] = int(input("Give percentage: "))
            except IndexError:
                self.last_action = "Needs more parameters eg. 'train builder 25'"
            if s[0] == "equal":
                for profession in p.profession_names:
                    self.training_percent[profession] = 20
        if self.firstrun == True:
            print("Type 'help' to see the commands or 'story' to print the story so far.")
            self.firstrun = False
        
    def complete_train(self, text, line, begidx, endidx):
        #print(p.profession_names)
        if not text:
            c = p.profession_names
        else:
            c = [i for i in p.profession_names if i.startswith(text)]
        return c
    def help_train(self):
        print("Choose the percentage of new followers trainded to a profession. You can type 'train <profession> [number]' to choose the percent to train chosen professionals.")
        print("If you set total training percent higher than 100%, the game will automatically compensate.")
        print("The farmer produces food, the builder builds shelters from bricks, the merchant trades food for brick, the soldier defends and attacks when on war and the scout provides you information. Everybody needs food and shelter.")
    def do_entertain(self, s):
        if p.taxincome >= 2:
            self.last_action = ["Travelling circus arrives to your kindom", "You arrange festival", "You arrange tournament", "You declare a bank holiday", "You arrange royal wedding"][random.randint(0, 4)]
            for follower in p.followers:
                p.followers[follower].happiness += 1
            p.taxincome -= 2
        else:
            self.last_action = "You don't have money to do that!"
    def help_entertain(self):
        print("Arrange fun activities for followers. Increases happines and wellbeing. Costs 2 money units.")
    def do_story(self, s):
        for line in p.story:
            print(line)
    def help_story(self):
        print("Print out the story so far. You can also start the game by typing 'python3 7_mountains.py skip' to omit the intro")
    def do_tax(self, l):
        print("Current tax is", p.tax)
        j = input("Give new tax rate (0.01-0.99 ")
        if j == "":
            pass
        else:
            p.tax = float(j)
        self.last_action = "You set the tax rate"
    def help_tax(self):
        print("change taxation")
    def do_scout(self, s):
        if self.informations_index <= p.informations_index:
            self.last_action = p.informations[self.informations_index]
            self.informations_index += 1
        if self.informations_index == 0:
            self.last_action = "Scouts have not yet provided any information."
    def help_scout(self):
        print("Show information provided by the scouts.")
    def do_punish(self, s):
        s = s.split(" ")
        try:
            if s[0] == "":
                self.last_action = "Try 'punish [punishment]'."
                print("nope")
                time.sleep(1)
            else:
                for crime in p.crimes:
                    p.crimes[crime] = 0
                self.last_action = s[0] + "ed the criminals"
                for follower in p.followers:
                    followers[follower].happiness += 1
                print(s[0] + "ing!")
                time.sleep(1)
                if s[0] == "pardon":
                    p.karma += 1
                if s[0] == "jail":
                    pass
                else:
                    p.karma -= 1
        except IndexError:
            self.last_action = "Try 'punish [punishment]'."
    def complete_punish(self, text, line, begidx, endidx):
        if not text:
            c = p.punishments
        else:
            c = [i for i in p.punishments if i.startswith(text)]
        return c
    def do_pray(self, s):
        if p.karma > 1:
            for follower in followers:
                followers[follower].happiness += p.karma / 10
        else:
            self.last_action = "Your god(s) seem unhappy to your actions."
    def help_pray(self):
        print("Pray your god(s) for help.")
    def do_stats(self, l):
        print("A young kingdom of", p.citadel)
        print(self.resources(), p.taxincome, "tax income")
        # print(self.training_percent)
        happiness = 0
        crimes = {}
        for profession in professions:
            a = 0
            for hahmo in followers:
                if profession.name == followers[hahmo].name:
                    a += 1
            print(self.color_bold, a, self.color_reset, profession.name, "\t" + str(self.training_percent[profession.name]) + "%")
        for hahmo in followers:
            happiness += followers[hahmo].happiness
        try:
            print("Happiness level: ", happiness / len(p.followers))
        except ZeroDivisionError:
            pass
        if sum(p.crimes.values()) != 0:
            for item in p.crimes:
                if p.crimes[item] != 0:
                    print("There were", p.crimes[item], item+ "s")
            print("Type punish to punish the perps.")
    def help_stats(self):
        print("Print out the statistics.")
    def do_war(self, l):
        if self.war == False:
            if input("You are about to declare a war, continue? (y/n)") == "y":
                print("War is not fully implemented yet. Type 'help' or hit tab twice to see war-related commands.")
                self.war = True
                nested=NestedShell()
                nested.cmdloop()
            else:
                self.last_action = "When the power of love overcomes the love of power the world will know peace. - Jimi Hendrix"
        else:
            nested=NestedShell()
            nested.cmdloop()
    def help_war(self):
        print("Declare a war or continue ongoing battle, a subshell will be opened for commanding the troops")
    def do_tutorial(self, s):
        self.tutorial = True
        if self.tutorial_index == 0:
            self.tutorial_index = 1
        else:
            self.tutorial_index = 0
    def help_tutorial(self):
        print("Start in-game tutorial how to play the game.")
    def do_pass(self, l):
        time.sleep(1)
        clearScreen()
        p.taxincome = p.collect_tax()
        p.bornAndDie()
        print(len(followers), "followers", resources, "tax income", p.taxincome)
        print(p.birthrate, "new followers were born.")
        for profession in professions:
            a = 0
            for hahmo in followers:
                if profession.name == followers[hahmo].name:
                    a += 1
            print(profession.name, a)
#        self.last_action = "Passed."
        if len(followers) < 1 and self.firstrun == False:
            self.last_action = "All the followers died. Game over!"

    def help_pass(self):
        print("Finish the turn. You can also press <enter> to pass.")
    def do_exit(self, s):
        return True
class NestedShell(cmd.Cmd):
    prompt = "war>"
    intro = "Type 'exit' to return to the main game."
    enemies = {"wildlings" : 10, "Another kingdom" : 100}
    def do_exit(self, s):
        return True
    def help_exit(self):
        print("Return back to main view")
    def do_stats(self, s):
        n = 0
        for Follower in p.followers:
            if p.followers[Follower].name == "soldier":
                n += 1
        print("You have", n, "soldiers")
        print("There's", len(p.enemies), "enemies")
    def do_attack(self, s):
        for Follower in p.followers:
            if followers[Follower].name == "soldier":
                followers[Follower].sodi()
        p.bornAndDie()
    def help_attack(self, s):
        print("Attack to the enemy")
    def do_retreat(self, s):
        pass
    def help_retreat(self, s):
        print("Retreat from the battle")
    def do_fortify(self, s):
        pass
    def help_fortify(self, s):
        print("Fortify to defence position")

p.story = ["At the beginning You and your twin brother were born to the King of Seven Mountains.", "Then came the war that tore the kindom to the dust.", "Your twin brother chose his evil wife over you and your family. Both of you chose different paths with few loyal followers.", "You travelled to the East and found a good place to start a residence."]
try:
    if sys.argv[1] == "skip":
        clearScreen()
except IndexError:
    clearScreen()
    for line in p.story:
        clearScreen()
        print(line)
        time.sleep(8)

p.citadel = input("Give name to this newborn town: ")
# print("Farmer produces food, builder builds shelter, merchant trades food to bricks that builder uses. Everybody needs food and shelter. Start by training followers to profession")
p.bornAndDie()
for Follower in followers:
    followers[Follower].age = 10

if __name__=='__main__':
    CmdShell().cmdloop()

print("Score:", score / beginwith)
