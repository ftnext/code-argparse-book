import argparse


def hi(name):
    print("Hi " + name + "!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    name = args.name
    hi(name)
