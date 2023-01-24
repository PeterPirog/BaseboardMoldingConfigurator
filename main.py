# https://www.optaplanner.org/blog/2016/10/26/DomainModelingGuide.html
# https://docs.optaplanner.org/7.11.0.Final/optaplanner-docs/html_single/index.html#designPatterns
# https://yed-uml.readthedocs.io/en/latest/class-diagram.html


from collections import OrderedDict
from math import ceil

if __name__ == "__main__":
    wall_len = OrderedDict()
    wall_len['a'] = 150.0
    wall_len['b'] = 100.0
    wall_len['c'] = 30.0
    wall_len['d'] = 40.0
    wall_len['e'] = 120.0
    wall_len['f'] = 60.0

    min_len=20.0
    board_len=140.0

    # wylicz maksynalną bazową liczbę listew
    N=ceil((sum(wall_len.values())+len(wall_len)*min_len)/board_len)
    print(N)
