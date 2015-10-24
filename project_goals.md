# Chess

## Primary Goal:

implement star trek chess, create an api that uses the library and implements the interface for playing a game and then create a web front-end, possibly followed by a mobile front end.

## Decisions:

1. Start by implementing regular chess in an extensible way
2. after regular chess is up and running, modify for star trek chess

## Design

The json object `chess_game.json` describes the rules behind chess. the main goal of putting all the rules in a json data object is to allow the flexibility to later implement Star Trek chess with minimal rework.
