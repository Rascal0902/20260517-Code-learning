def find_inverse_bruteforce(a, p):
    for candidate in range(1, p):
        if (a * candidate) % p == 1:
            return candidate
    return -1


def read_input():
    a, p = map(int, input().split())
    return a, p


def main():
    a, p = read_input()
    print(find_inverse_bruteforce(a, p))


if __name__ == "__main__":
    main()
