from T_Done import solve_cube
from T_Cube2 import solve_CFOP

def main():
	state = 'UUDUUUDDUFFFRRLBFBFBLFFFFRRUUDDDDDDULLRRLLLLRLBBBBBRRB'
	seq = solve_CFOP(state)
	print(seq)


if __name__ == '__main__':
	main()
