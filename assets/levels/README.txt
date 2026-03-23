PROPERTY-DRIVEN LEVELS AND TEACHING TILESET
===========================================

This folder now includes a pre-configured external Tiled tileset file:

    teaching_tileset.tsx

It points at:

    ../images/tileset.png

and already contains a small set of useful gameplay properties for teaching.

WHAT IS PRE-CONFIGURED
----------------------

The teaching tileset already marks some common tiles as gameplay tiles:

* solid ground/platform tiles
* ladder tiles
* one hazard tile with damage

This means students can start painting levels straight away without first
having to remember to add tile properties by hand.

CURRENT PRE-CONFIGURED PROPERTIES
---------------------------------

SOLID TILES:
    tile ids 74, 83, 88, 89, 98
    property: solid = true

LADDER TILES:
    tile ids 41, 56, 71
    property: ladder = true

HAZARD TILE:
    tile id 122
    properties:
        hazard = true
        damage = 50

USING IT IN TILED
-----------------

When creating a new map, use:

    teaching_tileset.tsx

or open:

    level_template.tmj

which is already set up to use it.

REQUIRED MAP LAYERS
-------------------

Tile layer:
    ground

Object layer:
    objects

OBJECT NAMES
------------

Use point objects in the "objects" layer named exactly:

    player
    enemy_runner
    enemy_shooter
    boss
    health
    ammo
    shield
    exit

BACKGROUND FILES
----------------

Backgrounds are still separate images, for example:

    level1bg1.png
    level1bg2.png
    level1bg3.png

COMMON TEACHING WORKFLOW
------------------------

1. Open level_template.tmj
2. Paint terrain on the ground layer
3. Use the pre-configured solid tiles for floors and walls
4. Use the pre-configured ladder tiles for climbable areas
5. Use the pre-configured hazard tile for spikes/traps
6. Add player/enemy/pickup/exit objects on the objects layer
7. Save the map as a new .tmj file

NOTES
-----

* Students can still add or change properties in Tiled later
* Different levels can still use different tilesets
* This teaching tileset is mainly a safe starter setup
* The game ignores Tiled tile rotation/flip visuals
