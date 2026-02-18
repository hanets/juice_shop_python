def transform_base_10_to_2(number: int) -> int:
    res = ""
    while number > 0:
        res += "1" if (number & 1) == 1 else "0"
        number >>= 1
    res = res[::-1]
    return int(res)


def transform_base_2_to_10(number: int) -> int:
    res = 0
    pow = 0
    while number > 0:
        res += number % 10 * 2**pow
        pow += 1
        number //= 10
    return res


def test_transform():
    input = 42
    res = ~input
    base2 = transform_base_10_to_2(input)
    print(base2)
    base10 = transform_base_2_to_10(base2)
    print(base10)
    assert base10 == input