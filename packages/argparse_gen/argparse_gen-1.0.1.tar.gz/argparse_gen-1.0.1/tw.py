import textwrap


print(repr("".join(str(x % 10) for x in range(17))))
print(
    "\n".join(
        (
            repr(line)
            for line in textwrap.wrap(
                "  ".join(
                    "".join(str(x) for x in range(n + 1))
                    for n in range(10)
                ),
                17,
            )
        ),
    ),
)
