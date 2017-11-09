"""This module implements basic gaming operations.  These
functions should be used to create higher level operations.
In particular, they should NOT be directly used by players."""


import os, pickle, random


# === game management functions ===
def reset_game():
    """Remove all characters and creatures + reset counters (money + defeated)."""
    
    if os.path.exists('game.db'):
        os.remove('game.db')


# === database management (do not use outside of API) ===
def _load_game_db():
    """Loads the game database.
    
    Returns
    -------
    game_db: contains all game information (dict)
    
    Notes
    -----
    If no database exists, an empty one is automatically created.
    
    """
    
    try:
        fd = open('game.db', 'rb')
        game_db = pickle.load(fd)
        fd.close()
    except:
        game_db = {'creatures': {},
                   'characters': {},
                   'team_money': 0,
                   'nb_defeated': 0}

    return game_db


def _dump_game_db(game_db):
    """Dumps the game database.
    
    Parameters
    -------
    game_db: contains all game information (dict)
    
    """
    
    fd = open('game.db', 'wb')
    pickle.dump(game_db, fd)
    fd.close()


# === team management functions ===
def set_team_money(money):
    """Sets the amount of money of the team.
        
    Parameters
    ----------
    money: amount of money (int)
    
    Raises
    ------
    ValueError: if money is strictly negative
    
    """
    
    game_db = _load_game_db()
    
    if money < 0:
        raise ValueError('money cannot be negative (money = %d)' % money)
    
    game_db['team_money'] = money
    
    _dump_game_db(game_db)


def get_team_money():
    """Returns the amount of money of the team.
    
    Returns
    -------
    money: amount of money (int)
   
    """
    
    game_db = _load_game_db()
    
    return game_db['team_money']


def set_nb_defeated(nb_defeated):
    """Sets the number of creatures defeated by the team.
        
    Parameters
    ----------
    nb_defeated: number of creatures defeated (int)
    
    Raises
    ------
    ValueError: if nb_defeated is strictly negative
    
    """
    
    game_db = _load_game_db()
    
    if nb_defeated < 0:
        raise ValueError('cannot be negative (nb_defeated = %d)' % nb_defeated)
    
    game_db['nb_defeated'] = nb_defeated
    
    _dump_game_db(game_db)


def get_nb_defeated():
    """Returns the number of creatures defeated by the team.
    
    Returns
    -------
    nb_defeated: number of creatures defeated (int)
   
    """
    
    game_db = _load_game_db()
    
    return game_db['nb_defeated']


# === character management functions ===
def character_exists(character):
    """Tells whether a character already exists or not.
    
    Parameters
    ----------
    character: character name (str)
    
    Returns
    -------
    result: True if character already exists, False otherwise (bool)
    
    """
    
    game_db = _load_game_db()
    
    return character in game_db['characters']
    
    
def add_new_character(character, variety, reach, strength, life):
    """Adds a new character to the game.
        
    Parameters
    ----------
    character: character name (str)
    variety: character variety (str)
    reach: character reach (str)
    strength: character strength (int)
    life: character life (int)
    
    Raises
    ------
    ValueError: if there already is a character with the same name
    ValueError: if variety is neither 'dwarf', 'elf', 'healer', 'wizard' nor 'necromancer'
    ValueError: if reach is neither 'short' nor 'long'
    ValueError: if strength is strictly negative
    ValueError: if life is strictly negative
    
    Notes
    -----
    This function does not give +50 gold to the team.
    
    """
    
    game_db = _load_game_db()
    
    if character_exists(character):
        raise ValueError('character %s already exists' % character)
    if variety not in ('dwarf', 'elf', 'healer', 'wizard', 'necromancer'):
        raise ValueError('variety %s is not valid' % variety)
    if reach != 'short' and reach != 'long':
        raise ValueError('reach %s is not valid' % reach)
    if strength < 0:
        raise ValueError('strength cannot be negative (strength = %d)' % strength)
    if life < 0:
        raise ValueError('life cannot be negative (life = %d)' % life)

    game_db['characters'][character] = {'variety': variety, 'reach': reach, 'strength': strength, 'life': life}
    
    _dump_game_db(game_db)


def get_character_variety(character):
    """Returns the variety of a character.
        
    Parameters
    ----------
    character: character name (str)
    
    Returns
    -------
    variety: character variety (str)
    
    Raises
    ------
    ValueError: if the character does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    
    return game_db['characters'][character]['variety'] 


def get_character_reach(character):
    """Returns the reach of a character.
        
    Parameters
    ----------
    character: character name (str)
    
    Returns
    -------
    reach: character reach (str)
    
    Raises
    ------
    ValueError: if the character does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    
    return game_db['characters'][character]['reach'] 


def set_character_strength(character, strength):
    """Modifies the strength of a character.
        
    Parameters
    ----------
    character: character name (str)
    strength: character strength (int)
    
    Raises
    ------
    ValueError: if the character does not exist
    ValueError: if strength is strictly negative
     
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    if strength < 0:
        raise ValueError('strength cannot be negative (strength = %d)' % strength)
    
    game_db['characters'][character]['strength'] = strength
    
    _dump_game_db(game_db)


def get_character_strength(character):
    """Returns the strength of a character.
        
    Parameters
    ----------
    character: character name (str)
    
    Returns
    -------
    strength: character strength (int)
    
    Raises
    ------
    ValueError: if the character does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    
    return game_db['characters'][character]['strength'] 
    
    
def set_character_life(character, life):
    """Modifies the life of a character.
        
    Parameters
    ----------
    character: character name (str)
    life: character life (int)
        
    Raises
    ------
    ValueError: if the character does not exist
    ValueError: if life is strictly negative
     
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    if life < 0:
        raise ValueError('life cannot be negative (life = %d)' % life)
    
    game_db['characters'][character]['life'] = life
    
    _dump_game_db(game_db)

        
def get_character_life(character):
    """Returns the life of a character.
        
    Parameters
    ----------
    character: character name (str)
    
    Returns
    -------
    life: character life (int)
    
    Raises
    ------
    ValueError: if the character does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not character_exists(character):
        raise ValueError('character %s does not exist' % character)
    
    return game_db['characters'][character]['life'] 


# === creature management functions ===
def creature_exists(creature):
    """Tells whether a creature already exists or not.
    
    Parameters
    ----------
    creature: creature name (str)
    
    Returns
    -------
    result: True if creature already exists, False otherwise (bool)
    
    """
    
    game_db = _load_game_db()
    
    return creature in game_db['creatures']


def add_creature(creature, reach, strength, life):
    """Adds a creature in the game.
    
    Parameters
    -------
    creature: creature name (str)
    reach: creature reach (str)
    strength: creature strength (int)
    life: creature life (int)
    
    Raises
    ------
    ValueError: if the creature already exist
    ValueError: if reach is neither 'short' nor 'long'
    ValueError: if strength is strictly negative
    ValueError: if life is strictly negative

    """
    
    game_db = _load_game_db()
    
    if creature_exists(creature):
        raise ValueError('creature %s already exists' % creature)
    if reach != 'short' and reach != 'long':
        raise ValueError('reach %s is not valid' % reach)
    if strength < 0:
        raise ValueError('strength cannot be negative (strength = %d)' % strength)
    if life < 0:
        raise ValueError('life cannot be negative (life = %d)' % life)
    
    game_db['creatures'][creature] = {'reach': reach, 'strength': strength, 'life': life}
    
    _dump_game_db(game_db)


def remove_creature(creature):
    """Removes a creature from the game.
    
    Parameters
    -------
    creature: creature name (str)
    
    Raises
    ------
    ValueError: if the creature does not exist
    
    Notes
    -----
    After its removal, the creature cannot be used anymore and is "lost".

    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exists' % creature)
    
    del game_db['creatures'][creature]
    
    _dump_game_db(game_db)


def get_random_creature_name():
    """Returns a new, random, unique creature name.
    
    Returns
    -------
    creature: random, unique creature name (str)
    
    """

    game_db = _load_game_db()
    
    if get_nb_defeated() == 0 or random.randint(0, 2) == 0:
        prefix = 'Python'
    else:
        prefix = ('Lieju', 'Raiden', 'Rinnees')[random.randint(0, 2)]

    suffix = str(random.randint(100, 999))
    
    return prefix + '#' + suffix


def get_creature_reach(creature):
    """Returns the reach of a creature.
        
    Parameters
    ----------
    creature: creature name (str)
    
    Returns
    -------
    reach: creature reach (str)
    
    Raises
    ------
    ValueError: if the creature does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exist' % creature)
    
    return game_db['creatures'][creature]['reach'] 


def set_creature_strength(creature, strength):
    """Modifies the strength of a creature.
        
    Parameters
    ----------
    creature: creature name (str)
    strength: creature strength (int)
    
    Raises
    ------
    ValueError: if the creature does not exist
    ValueError: if strength is strictly negative
     
    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exist' % creature)
    if strength < 0:
        raise ValueError('strength cannot be negative (strength = %d)' % strength)
    
    game_db['creatures'][creature]['strength']  = strength
    
    _dump_game_db(game_db)
    
    
def get_creature_strength(creature):
    """Returns the strength of a creature.
        
    Parameters
    ----------
    creature: creature name (str)
    
    Returns
    -------
    strength: creature strength (int)
    
    Raises
    ------
    ValueError: if the creature does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exist' % creature)
    
    return game_db['creatures'][creature]['strength'] 
    
    
def set_creature_life(creature, life):
    """Modifies the life of a creature.
        
    Parameters
    ----------
    creature: creature name (str)
    life: creature life (int)
        
    Raises
    ------
    ValueError: if the creature does not exist
    ValueError: if life is strictly negative
     
    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exist' % creature)
    if life < 0:
        raise ValueError('life cannot be negative (life = %d)' % life)
    
    game_db['creatures'][creature]['life']  = life
    
    _dump_game_db(game_db)

        
def get_creature_life(creature):
    """Returns the life of a creature.
        
    Parameters
    ----------
    creature: creature name (str)
    
    Returns
    -------
    life: creature life (int)
    
    Raises
    ------
    ValueError: if the creature does not exist
    
    """
    
    game_db = _load_game_db()
    
    if not creature_exists(creature):
        raise ValueError('creature %s does not exist' % creature)
    
    return game_db['creatures'][creature]['life'] 
