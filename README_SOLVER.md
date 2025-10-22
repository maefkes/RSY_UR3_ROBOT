# Rubiks-Cube Solver

Solver source: https://github.com/itsdaveba/cube-solver/blob/main/README.rst

## Install: 
``` bash
pip install cube-solver
```

## Notation
Color Strings:
- 'W' -> White
- 'G' -> Green
- 'R' -> Red
- 'Y' -> Yellow
- 'B' -> Blue
- 'O' -> Orange

Cube Face Colloring
``` 
        ---------
        | W W W |
        | W W W |
        | W W W |
---------------------------------
| O O O | G G G | R R R | B B B |
| O O O | G G G | R R R | B B B |
| O O O | G G G | R R R | B B B |
---------------------------------
        | Y Y Y |
        | Y Y Y |
        | Y Y Y |
        ---------
```

Cube Face Numbering
``` 
           ------------
           | 01 02 03 |
           | 04 05 06 |
           | 07 08 09 |
---------------------------------------------
| 10 11 12 | 19 20 21 | 28 29 30 | 37 38 39 |
| 13 14 15 | 22 23 24 | 31 32 33 | 40 41 42 |
| 16 17 18 | 25 26 27 | 34 35 36 | 43 44 45 |
---------------------------------------------
           | 46 47 48 |
           | 49 50 51 |
           | 52 53 54 |
           ------------
```