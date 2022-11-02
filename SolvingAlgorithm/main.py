import json
import os.path

from cube import RubiksCube
from solve import IDA_star, build_heuristic_db

"""
	heuristic variables
	
	max_num_moves - max amount of moves when building heuristics map
	new_heuristics - control for overwritting heuristics
	heuristic_file - file that the heuristic hash tables are saved in or need to be saved in
"""
max_num_moves = 6
new_heuristics = False
heuristic_file = 'heuristics.json'

test_cube = RubiksCube("")
test_cube.reset()
test_cube.CW_Up()
test_cube.CW_Right()
test_cube.CCW_Up()
test_cube.CCW_Right()
test_cube.CCW_Back()
test_cube.CW_Down()
test_cube.CW_Left()
test_cube.CW_Right()
test_cube.CCW_Up()
test_cube.CW_Left()


cube = RubiksCube("")
print(cube.CurrentArray)
print(cube.stringify())

"""
	Reading existing heuristics and creating ne ones if heuristics.json is empty
"""
if os.path.exists(heuristic_file):
	with open(heuristic_file) as f:
		h_db = json.load(f)
else:
	h_db = None

if h_db is None or new_heuristics is True:
	actions = ["F", "B", "R", "L", "U", "D", "FP", "Bp", "Rp", "Lp", "Up", "Dp"]
	h_db = build_heuristic_db(
		cube.stringify(),
		actions,
		max_moves = max_num_moves,
		heuristic = h_db
	)	
    
	with open(heuristic_file, 'w', encoding='utf-8') as f:
		json.dump(
			h_db,
			f,
			ensure_ascii=False,
			indent=4
		)
	
print("Cube to solve: ")
print(test_cube.CurrentArray)
print(test_cube.stringify())
solver = IDA_star(h_db)
moves = solver.run(test_cube.stringify())
print(moves)

print(moveSequence(moves))

def moveSequence(moves):
	state = ""
	for i in range(len(moves)):
		state.join(moves[i])
	return state
		
print("Finished")


