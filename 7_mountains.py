#!/usr/bin/env python3
# -*- coding: UTF-8 -*-  
# 7 mountains text game 
import random
import time
import cmd
import os
import sys
class Kansalainen():
    def __init__(self, resurssit, kansalaiset):
        self.metodit = [self.syo, self.etsisheltera, self.seksi_ja_kuolema, self.rotostele]
        self.resurssit = resurssit
        self.kansalaiset = kansalaiset
        self.elossa = True
        self.ika = 0
        self.varallisuus = 0
        self.onnellisuus = 7
        self.nimi = ""
        if self.resurssit["shelter"] < 1:
            self.elossa = False
        else:
            self.resurssit["shelter"] -= 1
    def syo(self):
        if self.resurssit["food"] > 1:
            self.resurssit["food"] -= 1
        else:
            self.elossa = False
    def etsisheltera(self):
        if self.resurssit["shelter"] > 1:
            pass
        else:
            self.elossa = False
    def seksi_ja_kuolema(self):
        self.ika += 1
        if self.ika > 40 or self.elossa == False:
            return "kuollut"
        if self.ika > 2 and self.ika < 35:
            return "penska"
    def rotostele(self):
        for rotos in p.rikokset:
            if random.randint(0, int(self.onnellisuus)) >= int(self.onnellisuus):
                p.rikokset[rotos] += 1
            
class Farmari(Kansalainen):
    # tuottaa fooda
    nimi = "farmer"
    def __init__(self, resurssit, kansalaiset):
        Kansalainen.__init__(self, resurssit, kansalaiset)
        self.metodit.append(self.viljele)
    def viljele(self):
        self.resurssit["food"] += 8
        self.varallisuus += 1
class Rakentaja(Kansalainen):
    # tuottaa sheltera resursseista
    nimi = "builder"
    def __init__(self, resurssit, kansalaiset):
        Kansalainen.__init__(self, resurssit, kansalaiset)
        self.metodit.append(self.rakenna)
    def rakenna(self):
        if self.resurssit["brick"] > 0:
            self.resurssit["shelter"] += 4
            self.resurssit["brick"] -= 2
            self.varallisuus += 2

class Sotilas(Kansalainen):
    # puolustaa ja sotii
    nimi = "soldier"
    def __init__(self, resurssit, kansalaiset):
        Kansalainen.__init__(self, resurssit, kansalaiset)
        self.nimi = "soldier"
    def sodi(self):
        killed = 0
        died = 0
        for sotilas in p.kansalaiset:
            if kansalaiset[sotilas].nimi == "soldier":
                r = random.randint(1, 2)
                if r == 1:
                    killed += 1
                    foo = p.enemies.pop()
                else:
                    self.elossa = False
                    died += 1
        print(killed, "enemies killed")
        print(died, "soldiers died")
class Kauppias(Kansalainen):
    # vaihtaa fooda resursseihin
    nimi = "merchant"
    def __init__(self, resurssit, kansalaiset):
        Kansalainen.__init__(self, resurssit, kansalaiset)
        self.metodit.append(self.kay_kauppaa)
    def kay_kauppaa(self):
        self.resurssit["food"] -= 2
        self.resurssit["brick"] += 4
        self.varallisuus += 3
class Tiedustelija(Kansalainen):
    nimi = "scout"
    def __init__(self, resurssit, kansalaiset):
        Kansalainen.__init__(self, resurssit, kansalaiset)
        self.metodit.append(self.tiedustele)
    def tiedustele(self):
        # tiedustelijat kuolevat helposti
        if random.randint(1, 2) == 2:
            self.elossa = False
        if random.randint(1, 6) == 6:
            if p.tiedot_index <= len(p.tiedot):
                p.tiedot_index += 1
class Pelaaja:
    def __init__(self, resurssit, kansalaiset, ammatit):
        self.resurssit = resurssit
        self.kansalaiset = kansalaiset
        self.syntyma = 10
        self.ammatit = ammatit
        self.ammattinimet = []
        for ammatti in self.ammatit:
            self.ammattinimet.append(ammatti.nimi)
        self.vero = 0.02
        self.verotulo = 0
        self.rikokset = {"theft" : 0, "arsony" : 0, "rape" : 0, "murder" : 0, "con" : 0}
        self.tiedot_index = 0
        self.tiedot = ["No information. Try training some scouts or pass few turns", "Scouts report: There are angry wildlings in nearby woods. You can start war against them by typing 'war'.", "Scouts report: There is an abandoned mine nearby. You can raid it by typing 'raid' (feature not available yet)"]

    def synnyJaKuole(self):
        kuolema = []
        for tyyppi in self.kansalaiset:
            for metodi in self.kansalaiset[tyyppi].metodit:
                a = metodi()
                if a == "penska":
                    self.syntyma += 1
                if a == "kuollut":
                    kuolema.append(tyyppi)
        for vainaa in kuolema:
            del self.kansalaiset[vainaa]
    def keraaVerot(self):
        self.verotulo = 0
        for hahmo in self.kansalaiset:
            if self.kansalaiset[hahmo].varallisuus - p.vero > 0:
                self.kansalaiset[hahmo].varallisuus -= p.vero
                self.verotulo += p.vero
            else:
                pass
            kansalaiset[hahmo].onnellisuus = kansalaiset[hahmo].onnellisuus - self.vero * 1
        return self.verotulo
resurssit = {"food" : 10, "shelter" : 10, "brick" : 10}
kansalaiset = {}
pisteet = 0
ammatit = [Farmari, Rakentaja, Kauppias, Sotilas, Tiedustelija]
aloitus = 40
p = Pelaaja(resurssit, kansalaiset, ammatit)
for resurssi in resurssit:
    resurssit[resurssi] = aloitus
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
    tutorial_list = [None, "First let's train some farmers by typing 'train farmer 25' -this will set the amount of farmers to be trained to 25%. Type 'tutorial' again to stop tutorial", "Next, let's set the training for the rest of the followers. Repeat the previous step but this time by typing 'train builder 25'.", "Next 'train merchant 25'. Once you're set, the values will remain the same until you change them -you don't have to do this every turn.", "And 'train soldier 25'.", "Good, now the training is set. Let's change the tax rate by typing 'tax'.", "The last thing we'll do in this tutorial is to hit tab-key twice. This will show all the commands we'll have. You can autocomplete sentences with tab by typing first few letters of a sentence and then hit tab. For example pa<tab> to autocomplete 'pass'", "Type 'help' for in-game help or 'help <command> to view help for a certain command (don't forget the tab-autocomplete!). TIP: train some scouts."]
    last_action = ""
    tiedot_index = 0

    for ammatti in p.ammatit:
        training_percent[ammatti.nimi] = 0
    def preloop(self):
        os.system("clear")
        self.do_stats("foo")
    def emptyline(self):
        self.do_pass("foo")
    def postcmd(self, stop, line):
        if p.tiedot_index > self.tiedot_index:
            last_action = "Scouts have provided new information. Type 'scout' to view information."
        for ammatti in ammatit:
            for i in range(int(self.training_percent[ammatti.nimi] / 100 * p.syntyma)):
                p.kansalaiset[len(p.kansalaiset) + 1] = ammatti(resurssit, kansalaiset)
                p.syntyma -= 1
        if line[0:4] != "help" and line[0:5] != "story":
            os.system("clear")
            self.do_stats("foo")
            print(self.last_action)
            if self.tutorial_index != 0:
                print(self.tutorial_list[self.tutorial_index])
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
        for ammatti in p.ammattinimet:
            try:
                if s[1].isdigit() == True and s[0] == ammatti:
                    if int(s[1]) > 100:
                        self.last_action = "Error: use values 0-100%"
                    else:
                        self.training_percent[ammatti] = int(s[1])
                        while sum(self.training_percent.values()) > 100:
                            for item in self.training_percent:
                                if item != s[0] and self.training_percent[item] >= 1:
                                    self.training_percent[item] -= 1

                if s[0] == ammatti and len(s) == 1:
                    self.training_percent[ammatti] = int(input("Give percentage: "))
            except IndexError:
                last_action = "Needs more parameters eg. 'train builder 25'"
            if s[0] == "equal":
                for ammatti in p.ammattinimet:
                    self.training_percent[ammatti] = 20
        if self.firstrun == True:
            print("Type 'help' to see the commands or 'story' to print the story so far.")
            self.firstrun = False
        if self.tutorial == True:
            self.tutorial_index += 1
        
    def complete_train(self, text, line, begidx, endidx):
        #print(p.ammattinimet)
        if not text:
            c = p.ammattinimet
        else:
            c = [i for i in p.ammattinimet if i.startswith(text)]
        return c
    def help_train(self):
        print("Choose the percentage of new followers trainded to a profession. You can type 'train <profession> [number]' to choose the percent to train chosen professionals.")
        print("If you set total training percent higher than 100%, the game will automatically compensate.")
        print("The farmer produces food, the builder builds shelters from bricks, the merchant trades food for brick, the soldier defends and attacks when on war and the scout provides you information. Everybody needs food and shelter.")
    def do_entertain(self, s):
        if p.verotulo >= 2:
            self.last_action = ["Travelling circus arrives to your kindom", "You arrange festival", "You arrange tournament", "You declare a bank holiday", "You arrange royal wedding"][random.randint(0, 4)]
            for follower in p.kansalaiset:
                p.kansalaiset[follower].onnellisuus += 1
            p.verotulo -= 2
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
        print("Current tax is", p.vero)
        j = input("Give new tax rate (0.01-0.99 ")
        if j == "":
            pass
        else:
            p.vero = float(j)
        self.last_action = "You set the tax rate"
        if self.tutorial == True:
            self.tutorial_index += 1
    def help_tax(self):
        print("change taxation")
    def do_scout(self, s):
        if self.tiedot_index <= p.tiedot_index:
            self.last_action = p.tiedot[self.tiedot_index]
            self.tiedot_index += 1
        if self.tiedot_index == 0:
            self.last_action = "Scouts have not yet provided any information."
#        s = s.split(" ")
#        if s[1].isdigit() == True:
#            try:
#                if int(s[1]) <= p.tiedot_index:
#                    self.last_action = p.tiedot[int(s[1])]
#            except IndexError or ValueError:
#                self.last_action = "Type 'scout [number]'. Available numbers 0..." + str(p.tiedot_index)
#        try:
#            if int(s[1]) > p.tiedot_index:
#                self.last_action = "Use number in range 0-" + str(p.tiedot_index)
#        except ValueError:
#            self.last_action = "Use number in range 0-" + str(p.tiedot_index)
#        else:
#            self.last_action = "Type 'scout [number]'. Available numbers 0-" + str(p.tiedot_index)
    def help_scout(self):
        print("Show information provided by the scouts.")
    def do_justice(self, s):
        i = input("What do we do with these criminals? (jail/hang/scald) ")
        for crime in p.rikokset:
            p.rikokset[crime] = 0
        last_action = i + "ed the criminals"
    def do_stats(self, l):
        print("A young kingdom of", p.citadel)
        print(resurssit, p.verotulo, "tax income")
        # print(self.training_percent)
        happiness = 0
        crimes = {}
        for ammatti in ammatit:
            a = 0
            for hahmo in kansalaiset:
                if ammatti.nimi == kansalaiset[hahmo].nimi:
                    a += 1
            print(a, ammatti.nimi, "\t" + str(self.training_percent[ammatti.nimi]) + "%")
        for hahmo in kansalaiset:
            happiness += kansalaiset[hahmo].onnellisuus
        try:
            print("Happiness level: ", happiness / len(p.kansalaiset))
        except ZeroDivisionError:
            pass
        if sum(p.rikokset.values()) != 0:
            for item in p.rikokset:
                if p.rikokset[item] != 0:
                    print("There were", p.rikokset[item], item+ "s")
            print("Type justice to punish the perps.")
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
                last_action = "When the power of love overcomes the love of power the world will know peace. - Jimi Hendrix"
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
        os.system("clear")
        p.verotulo = p.keraaVerot()
        p.synnyJaKuole()
        print(len(kansalaiset), "followers", resurssit, "tax income", p.verotulo)
        print(p.syntyma, "new followers were born.")
        for ammatti in ammatit:
            a = 0
            for hahmo in kansalaiset:
                if ammatti.nimi == kansalaiset[hahmo].nimi:
                    a += 1
            print(ammatti.nimi, a)
#        self.last_action = "Passed."
        if self.tutorial == True:
            self.tutorial_index += 1
        if len(kansalaiset) < 1 and self.firstrun == False:
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
        for kansalainen in p.kansalaiset:
            if p.kansalaiset[kansalainen].nimi == "soldier":
                n += 1
        print("You have", n, "soldiers")
        print("There's", len(p.enemies), "enemies")
    def do_attack(self, s):
        for kansalainen in p.kansalaiset:
            if kansalaiset[kansalainen].nimi == "soldier":
                kansalaiset[kansalainen].sodi()
        p.synnyJaKuole()
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
        os.system("clear")
except IndexError:
    os.system("clear")
    for line in p.story:
        os.system("clear")
        print(line)
        time.sleep(8)

p.citadel = input("Give name to this newborn town: ")
# print("Farmer produces food, builder builds shelter, merchant trades food to bricks that builder uses. Everybody needs food and shelter. Start by training followers to profession")
p.synnyJaKuole()
for kansalainen in kansalaiset:
    kansalaiset[kansalainen].ika = 10

if __name__=='__main__':
    CmdShell().cmdloop()

print("Score:", pisteet / aloitus)
