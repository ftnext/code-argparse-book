import argparse


def hi(name):
    print("Hi " + name + "!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
