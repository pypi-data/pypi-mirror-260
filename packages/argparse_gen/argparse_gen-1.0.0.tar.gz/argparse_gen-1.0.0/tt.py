#!/usr/bin/pyuthon3

import argparse
import sys

from t import Foo, f


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='',
        description=sys.modules[__name__].__doc__,
    )
    parser.add_argument(
        'x',
        help='Some number that we like.',
    )
    parser.add_argument(
        'c',
        nargs='?',
        default='17',
    )
    parser.add_argument(
        '-y',
        default=1,
        type=int,
        help='Some number that we also like.',
    )
    parser.add_argument(
        '-x',
        '--xxx',
        default=17,
        type=float,
        help='Hmpf...',
    )
    parser.add_argument(
        '-b',
        default=True,
        action='store_false',
    )
    parser.add_argument(
        '-s',
        '--something',
        default=None,
    )
    parser.add_argument(
        '-f',
        '--foo',
        default=Foo.a,
        type=lambda value: getattr(Foo, value),
        choices=[Foo.a, Foo.b],
    )

    args = parser.parse_args()

    f(
        args.x,
        args.c,
        y=args.y,
        xxx=args.xxx,
        b=args.b,
        something=args.something,
        foo=args.foo,
    )
