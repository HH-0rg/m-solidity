from globals import storage

def main():
    y = storage[0]
    x = y * 5
    storage[0] = x + 1

main()

from globals import dump_code, to_uint256
deployedcode = dump_code()
l = len(deployedcode)//2
print("7F" + to_uint256(l).hex() + "8060283D393DF3" + deployedcode)
