import argparse


def calculate_total_price(price, rate):
    included_tax_rate = 1 + rate / 100
    total = int(price * included_tax_rate)
    print(f"税込金額は{total}円です")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("price", type=int)
    args = parser.parse_args()

    price = args.price
    calculate_total_price(price, 8)
