def mod_pow(base, exponent, modulus):
    result = 1
    base %= modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2

    return result


def read_input():
    a, p = map(int, input().split())
    return a, p


def main():
    a, p = read_input()
    print(mod_pow(a, p - 2, p))


if __name__ == "__main__":
    main()
