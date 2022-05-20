# Checkers engine

The game itself is mostly copied from [this solution](https://github.com/techwithtim/Python-Checkers),
but with rules changed to be the same as the [ones provided by 
Polish Checkers Union](https://www.kurnik.pl/warcaby/zasady.phtml) (similar to giveaway checkers).

There are three ways to play, player vs. player, AI vs. AI and player vs. AI.

There is two heuristics to evaluate the position, both static:
- Edge function - the more valuable squares are in the center of the board, so the game goes to the center
- 3 stages function - the game is divided into 3 phases, opening, mid-game and endgame. The function is the same as in the edge function in the opening. In the middle game, the most profitable moves are those 
which move pawns in the back rows, so they stay close to each other. In the endgame, the most beneficial moves are those which advance pawns further to promote them as quickly as possible.

You can look into exact values in `checkers/constans.py` file.

When starting game you can provide:
- `depth` - any integer; default `3`
- `algorithm` - `'min-max'` or `'alpha-beta'`; default `'alpha-beta'`
- `heuristic` - way of evaluation, `1` or `2`; default `1`
- `color` - if playing against AI, `WHITE` or `RED`; default `WHITE`