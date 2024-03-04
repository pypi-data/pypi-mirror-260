import sys

from pyrot13 import rot13


def main() -> None:
	x = sys.stdin.read()
	y = rot13(x)
	sys.stdout.write(y)


if __name__ == "__main__":
	main()
