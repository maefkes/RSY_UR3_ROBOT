from cube_solver import Kociemba, Thistlethwaite, Cube

# scramble = Maneuver.random()
# print(f"Scramble: {scramble}")

#cube = Cube(scramble)
#cube = Cube(None,"WGGRWRWWYOWOWOBYGRGOGYGYWRGOBRGRRRYYWOBGBBROOBYYWYOBBB")
# cube = Cube(None, "WGROWGYRY"+"GYGGOYOWB"+"OYRBGOYWG"+"GOBWRWWOB"+"WRORBYOBW"+"RGRBYBBRY")
# print(cube)
# print(f"Cube: {repr(cube)}")

def get_Cube_Solution(cube:str)->str:
    cube = Cube(None, cube.upper())
    solver = Kociemba()
    #solver = Thistlethwaite()
    solution = solver.solve(cube)
    # assert solution is not None
    # assert solution == scramble.inverse
    return solution