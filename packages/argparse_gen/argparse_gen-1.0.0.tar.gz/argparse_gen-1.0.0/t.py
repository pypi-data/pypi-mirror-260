import enum
import sys

from argparse_gen import ArgparseGen


class Foo(enum.Enum):
    a = enum.auto()
    b = enum.auto()


def f(
    x: int | str,
    c: int | str = "17",
    /,
    y: int = 1,
    xxx: float = 17,
    b: bool = True,
    something: int | str | None = None,
    foo: Foo = Foo.a,
):
    """
    dkfjgbn

    skdfj jshkdbf jh.

    :param x: Some number
        that we like and want to use. Why, you may ask? I guess it's hard
        to explain. So we won't even try. At all. Not one bit. Nada!
    :param y: Some number that we also like.
    :param xxx: Hmpf...
    """


if __name__ == "__main__":
    print(ArgparseGen(sys.modules[__name__], "f").as_code())
