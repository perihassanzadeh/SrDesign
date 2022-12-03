from T_Done import solve_cube

def main():
	state = 'UUDUUUDDUFFFRRLBFBFBLFFFFRRUUDDDDDDULLRRLLLLRLBBBBBRRB'
	seq = solve_cube(state)
	print(seq)


if __name__ == '__main__':
	main()
