# Checkers engine

The game itself is mostly copied from [this solution](https://github.com/techwithtim/Python-Checkers),
but with rules changed to be the same as the [ones provided by 
Polish Checkers Union](https://www.kurnik.pl/warcaby/zasady.phtml) (similar to giveaway checkers).

There is 2 heuristics to valuate the position, both static (for now). You can look into values in 
`checkers/constans.py` file.

There is 3 way to play, player vs player, AI vs AI and player vs AI (for now only as white).

The `min-max` algorithm is implemented. `alfa-beta` is yet to be implemented.