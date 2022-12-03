from globals import storage

def main():
    y = storage[0]
    # y = 0
    # memory[y] = storage[0]
    x = y * 5
    # x = 1
    # memory[x] = memory[y] * 5
    storage[0] = x + 1
    # z = 2
    # memory[z] = memory[x] + 1
    # storage[0] = memory[z]

main()

from globals import dump_code
dump_code()