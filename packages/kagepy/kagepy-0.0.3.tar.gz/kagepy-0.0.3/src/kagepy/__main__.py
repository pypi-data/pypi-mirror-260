import math
import random

from kagepy.data import get_cake, get_cake_amount


def main():
    cake_amount = get_cake_amount()
    cake_index = math.floor(random.Random().random() * cake_amount)
    cake = get_cake(cake_index)
    print(cake)


if __name__ == '__main__':
    main()
