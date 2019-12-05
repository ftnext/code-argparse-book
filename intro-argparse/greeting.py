import sys


def hi(name):
    print("Hi " + name + "!")


if __name__ == "__main__":
    name = sys.argv[1]
    hi(name)
