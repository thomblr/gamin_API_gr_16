from gaming_tools import *
from random import randint


def kill_creature(killer, creature):
    """
    'killer' kill the creature 'creature'

    Parameters
    ----------
    killer : Name of the killer (str)
    creature : Name of the killed creature (str)

    """
    set_nb_defeated(get_nb_defeated() + 1)
    set_team_money(get_team_money() + (40 + 10 * get_nb_defeated()))
    print("%s(%s) killed the creature %s" % (killer, get_character_variety(killer), creature))
    remove_creature(creature)


def is_lucky(chance):
    """
    Check if yes or no you are lucky with a percentage of 'chance'

    Parameters
    ----------
    chance : the percentage of chance to succeed (int)

    Return
    ------
    lucky : if you are lucky or not (bool)
    """
    return randint(0, 100) <= chance


def can_attack(attacker_name, target_name):
    """
    Check if attacker can attack target, based on their reach
    :param attacker_name: the name of the attacker (str)
    :param target_name: the name of the target (str)
    :return: if attacker can attack target (bool)
    """

    if character_exists(attacker_name) and creature_exists(target_name):
        return get_character_reach(attacker_name) == 'long' \
               or get_character_reach(attacker_name) == 'short' and get_creature_reach(target_name) == 'short'
    elif creature_exists(attacker_name) and character_exists(target_name):
        return get_creature_reach(attacker_name) == 'long' \
               or get_creature_reach(attacker_name) == 'short' and get_character_reach(target_name) == 'short'
    else:
        return False


def create_character(name, variety):
    """
    Create a new character with a unique name and a variety

    Parameters
    ----------
    name : Name of the character (str)
    variety : Variety of the character (str)

    """
    if not character_exists(name):
        if variety == 'dwarf' or variety == 'elf' or variety == 'healer' \
                or variety == 'necromancer' or variety == 'wizard':
            if variety == 'dwarf':
                life = randint(10, 50)
                strength = randint(10, 50)
            elif variety == 'elf':
                life = randint(15, 25)
                strength = randint(15, 25)
            else:
                life = randint(5, 15)
                strength = randint(5, 15)

            # Check if variety is elf or wizard -> long reach
            if variety == 'elf' or variety == 'wizard':
                reach = 'long'
            # If not wizard and not elf -> can only be short reach
            else:
                reach = 'short'

            # Add the new character to the db
            add_new_character(name, variety, reach, strength, life)
            # Add 50 money on each character creation
            set_team_money(get_team_money() + 50)
            print("New %s created named %s with %d life and %d strength" % (variety, name, life, strength))
        else:
            print('This variety does not exists')
    else:
        print("A character with that name already exists")


def create_creature():
    """
    Create a new creature with random name, reach, strength and life

    Returns
    -------
    creature : the creature name (str)
    """
    name = get_random_creature_name()
    random_reach = randint(0, 1)
    strength = randint(1, 10) * (1 + get_nb_defeated())
    life = randint(1, 10) * (1 + get_nb_defeated())

    if random_reach == 0:
        reach = 'short'
    else:
        reach = 'long'

    print("Added creature %s with %s reach, %d strength and %d life" % (name, reach, strength, life))
    add_creature(name, reach, strength, life)
    return name


def attack(attacker_name, creature_name):
    """
    Attack the current creature whose name is creature_name

    Parameters
    ----------
    attacker_name : Name of the attacker (str)
    creature_name : Name of the creature to attack (str)

    """
    # Player does not exists
    if not character_exists(attacker_name):
        print('This attacker does not exists')
    # Creature does not exists
    elif not creature_exists(creature_name):
        print('This creature does not exist')
    # Player is dead
    elif get_character_life(attacker_name) <= 0:
        print('You can not attack because you are dead')
    # Creature is already dead
    elif get_creature_life(creature_name) <= 0:
        print('You can not attack this creature because she is dead')
    # Player does not have enough range
    elif not can_attack(attacker_name, creature_name):
        print('You do not have enough reach to attack this creature')
    # All conditions are true
    else:
        character_life = get_character_life(attacker_name)
        character_strength = get_character_strength(attacker_name)
        character_variety = get_character_variety(attacker_name)

        creature_life = get_creature_life(creature_name)
        creature_strength = get_creature_strength(creature_name)

        # Player kills creature
        if creature_life - character_strength <= 0:
            kill_creature(attacker_name, creature_name)
        else:
            '''
                Creature still alive
                Reduce creature life by attacker strength
            '''
            print("%s(%s) dealt %d damages to the creature and it has %d points of life left" %
                  (attacker_name, character_variety, character_strength,
                   (creature_life - character_strength)))
            set_creature_life(creature_name, (creature_life - character_strength))
            if character_life - creature_strength <= 0:
                '''
                    Attacker killed
                    Set attacker life to 0 (can not attack anymore)
                '''
                set_character_life(attacker_name, 0)
                print("%s(%s) has been killed by creature %s" %
                      (attacker_name, character_variety, creature_name))
            else:
                '''
                    Attacker still alive
                    Reduce attacker life by creature strength
                '''
                if can_attack(creature_name, attacker_name):
                    print("%s(%s) lost %d points of life, he still has %d point of life" %
                          (attacker_name, character_variety, creature_strength,
                           (character_life - creature_strength)))
                    set_character_life(attacker_name, (character_life - creature_strength))


def launch_spell(launcher_name, target_name):
    """
    Character 'launcher_name' launch a spell on the creature/player 'target_name'

    Parameters
    ----------
    launcher_name : Name of the character who launch the spell (str)
    target_name : Name of the creature/player who receives the spell (str)

    """
    if not character_exists(launcher_name):
        print('This character does not exists')
    elif get_character_life(launcher_name) <= 0:
        print('This character is dead and can not launch a spell')
    elif get_character_variety(launcher_name) == 'healer':
        if get_team_money() < 5:
            print('Your team does not have enough money')
        elif not character_exists(target_name):
            print('This character does not exists')
        elif get_character_life(target_name) <= 0:
            print('You can not heal a dead character')
        else:
            """
                Character still alive
                Add 10 points of life to the target
                Remove 5 money from team
            """
            set_character_life(target_name, get_character_life(target_name) + 10)
            set_team_money(get_team_money() - 5)
            print("%s(healer) has added 10 points of life to %s(%s)" %
                  (launcher_name, target_name, get_character_variety(target_name)))
    elif get_character_variety(launcher_name) == ' wizard':
        if get_team_money() < 20:
            print('Your team does not have enough money')
        elif not creature_exists(target_name):
            print('This creature does not exists')
        elif get_creature_life(target_name) <= 0:
            print('That creature is not alive')
        else:
            """
                Creature still alive
                Reduce by 2 creature's life
                Remove 20 money from team
            """
            set_creature_life(target_name, get_creature_life(target_name) // 2)
            set_team_money(get_team_money() - 20)
            # Check if the spell kills the target creature
            if get_creature_life(target_name) // 2 == 0:  # 1 // 2 == 0
                kill_creature(launcher_name, target_name)
            # The spell does not kill the target creature
            else:
                print("%s creature still has %d points of life" %
                      (target_name, get_creature_life(target_name)))
    elif get_character_variety(launcher_name) == 'necromancer':
        if get_team_money() < 75:
            print('Your team does not have enough money')
        elif not character_exists(target_name):
            print('This character does not exists')
        elif get_character_life(target_name) > 0:
            print('%s(%s) is still alive' % (target_name, get_character_variety(target_name)))
        else:
            """
                Character dead
                Set target life to 10
                Remove 75 money from team
            """
            set_character_life(target_name, 10)
            set_team_money(get_team_money() - 75)
            print("%s(necromancer) has resurrected the character %s(%s)" %
                  (launcher_name, target_name, get_character_variety(target_name)))
    # Variety =/= from healer, wizard & necromancer
    else:
        print("Your variety does not have any spell")


def evolute(name):
    """
    Player 'name' evolute if the team has enough money

    Parameters
    ----------
    name : Name of the player who wants to evolute (str)

    """
    # Check if the character exists
    if character_exists(name):
        # Check if the character is still alive
        if get_character_life(name) > 0:
            # Check if the team has enough money
            if get_team_money() >= 4:
                print("Evolution of %s" % name)
                set_team_money(get_team_money() - 4)

                if is_lucky(25):
                    new_character_strength = get_character_strength(name) + 4
                    print("%s character has now %d points of strength" % (name, new_character_strength))
                    set_character_strength(name, new_character_strength)
                else:
                    print('Your strength has not evolved')

                if is_lucky(50):
                    new_character_life = get_character_life(name) + 2
                    print("%s character has now %d points of life" % (name, new_character_life))
                    set_character_life(name, new_character_life)
                else:
                    print('Your life has not evolved')
            # The team has not enough money
            else:
                print("Your team does not have enough money for evolution")
        # Character not alive
        else:
            print("You can not evolute if you are dead")
    # Character does not exists
    else:
        print("This character does not exists")


def character_info(character_name):
    """
    Show the information of the character 'character_name'

    Parameters
    ----------
    character_name : Name of the character (str)

    """
    if character_exists(character_name):
        print(character_name)
        print('\tVariety : %s' % get_character_variety(character_name))
        print('\tLife : %d' % get_character_life(character_name))
        print('\tStrength : %d' % get_character_strength(character_name))
    else:
        print('This character does not exists')


def money():
    """Show the money of the team"""
    print('Money of the team : %d' % get_team_money())
