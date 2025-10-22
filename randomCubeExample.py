from cube_solver import Cube, Maneuver, Kociemba, Thistlethwaite

scramble = Maneuver.random()
print(f"Scramble: {scramble}")

#cube = Cube(scramble)
#cube = Cube(None,"WGGRWRWWYOWOWOBYGRGOGYGYWRGOBRGRRRYYWOBGBBROOBYYWYOBBB")
cube = Cube(None, "WGROWGYRY"+"GYGGOYOWB"+"OYRBGOYWG"+"GOBWRWWOB"+"WRORBYOBW"+"RGRBYBBRY")
print(cube)
print(f"Cube: {repr(cube)}")

solver = Kociemba()
#solver = Thistlethwaite()
solution = solver.solve(cube)
# assert solution is not None
# assert solution == scramble.inverse
print(f"Solution: {solution} ({len(solution)})")