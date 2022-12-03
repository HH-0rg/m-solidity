from globals import storage

def main():
    y = storage[0]
    x = y * 5
    storage[0] = x + 1

main()

from globals import dump_code
dump_code()