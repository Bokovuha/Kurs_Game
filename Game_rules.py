import init

damage = 25
aster_count = 8
aster_min_speed = 2
aster_max_speed = 6
ammo_chance = 500
heal_chance = 1000
item_speed = 1

if init.score >= 5000:
    damage = 34
    aster_count = 10
    aster_min_speed = 4
    aster_max_speed = 8
    ammo_chance = 1000
    heal_chance = 1500
    item_speed = 2

if init.score >= 10000:
    damage = 50
    aster_count = 12
    aster_min_speed = 6
    aster_max_speed = 12
    ammo_chance = 1500
    heal_chance = 2500
    item_speed = 3

if init.score >= 15000:
    damage = 100
    aster_count = 14
    aster_min_speed = 8
    aster_max_speed = 14
    ammo_chance = 1234
    heal_chance = 1234
    item_speed = 4
