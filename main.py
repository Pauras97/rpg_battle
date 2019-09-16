from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#Create Black Magic
fire = Spell("Fire",25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 15, 130, "black")

#Create White Magic
cure = Spell("Cure", 25, 600, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-potion", "potion", "Heals 300 HP", 1000)
elixr = Item("Elixr", "elixr", "Fully restores HP/MP of 1 member", 9999)
hielixr = Item("Mega-Elixr", "elixr", "Fully restores HP/MP of all members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixr, "quantity": 5},
                {"item": hielixr, "quantity": 2}, {"item": grenade, "quantity": 5}]
#Instantiate people
player1 = Person("Pauras :", 4000, 150, 300, 40, player_spells, player_items)
player2 = Person("Rohit  :", 3000, 100, 250, 40, player_spells, player_items)
player3 = Person("Anushka:", 3500, 200, 280, 40, player_spells, player_items)

enemy1 = Person("  Imp", 1300, 130, 550, 300, enemy_spells, [])
enemy2 = Person("Bhatt", 13000, 100, 500, 30, enemy_spells, [])
enemy3 = Person("  Imp", 1300, 130, 550, 300, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "An enemy attacks!" + bcolors.ENDC)

while running:
    print("=======================")

    print("\n\n")
    print("NAME                             HP                                    MP")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose an action : ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage. ")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic : ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()


            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don\'t have enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal_hp(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg), "HP." + bcolors.ENDC)
                print(bcolors.OKGREEN + "Current HP : " + str(player.get_hp()) + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals ", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose item : ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\nNone Left\n" + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1
            print(bcolors.OKBLUE + item.name + " left : " + str(player.items[item_choice]["quantity"]))


            if item.type == "potion":
                player.heal_hp(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixr":
                if item.name == "Mega-Elixr":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)
                print(bcolors.FAIL + "\n" + "You attacked " + enemies[enemy].name.replace(" ", "") + " for " + str(item.prop) + " points" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    #Check is battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    #Check if players won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + bcolors.BOLD + "You Win" + bcolors.ENDC)
        running = False

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #Check if enemies won
    if defeated_players == 2:
        print(bcolors.FAIL + bcolors.BOLD + "Your enemy has defeated you" + bcolors.ENDC)
        running = False

    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            #Enemy chose attack
            target = random.randrange(0, 3)

            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)

            print(bcolors.FAIL + bcolors.BOLD + enemy.name.replace(" ", "") + " attacks " + players[target].name + " for", enemy_dmg, "points of damage." + bcolors.ENDC)

        elif enemy_choice == 1:

            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal_hp(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for " + str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + spell.name + " deals ", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print([players][target].name + " has died.")
                    del players[target]

            #print("Enemy chose", spell.name, "with damage", magic_dmg)


