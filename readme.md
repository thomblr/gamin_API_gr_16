# Mini Projet 1

Mini projet n°1 du cours de programmation
Bloc 1

## How to use it

Different classes :
* dwarf
    * Health : 10 - 50
    * Strength : 10 - 50
    * Range : Short
* elf
    * Health : 15 - 25
    * Strength : 15 - 25
    * Range : Long
* healer
    * Health : 5 - 15
    * Strength : 5 - 15
    * Range : Short
* wizard
    * Health : 5 - 15
    * Strength : 5 - 15
    * Range : Long
* necromancer
    * Health : 5 - 15
    * Strength : 5 - 15
    * Range : Short

To create a character use `create_character(name, variety)`

To create a creature use `creature_name = create_creature()`

> Note: Team receives 50 money when creating a character

### Attack
***

To attack a creature use `attack(player_name, creature)`

**Short** range players can not attack **long** range creatures.

You deal as much damage as you have strength.

The creature deals you back as much damage as it has.

If the attacker is **long** range and the creature is **short** range,
the creature does not attack back.

When a creature is killed, the team earns `40 + 10 * nb_creature_killed` money.

### Special abilities
***

To use special abilities of players use `launch_spell(launcher_name, target_name)`

TODO

### Evolution
***

To use the evolution on a player use `evolute(player_name)`

TODO