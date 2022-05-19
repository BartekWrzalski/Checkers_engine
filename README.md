# Checkers engine

The game itself is mostly copied from [this solution](https://github.com/techwithtim/Python-Checkers),
but with rules changed to be the same as the [ones provided by 
Polish Checkers Union](https://www.kurnik.pl/warcaby/zasady.phtml) (similar to giveaway checkers).

There is 2 heuristics to valuate the position, both static (for now). You can look into values in 
`checkers/constans.py` file.

There is 3 way to play, player vs player, AI vs AI and player vs AI.

When starting game you can provide 
`depth` (default `3`), `algorithm` (default `'alpha-beta'`), `heuristic` (way of evaluation; default `1`) and 
player `color` (if playing against AI; default `WHITE`)