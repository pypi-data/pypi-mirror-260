import unittest

from pyrot13 import rot13


class TestRot13(unittest.TestCase):
	test_cases = [
		("", ""),
		("a", "n"),
		("abc", "nop"),
		("xyzabc", "klmnop"),
		("A", "N"),
		("ABC", "NOP"),
		("XYZABC", "KLMNOP"),
		("Hello, World!", "Uryyb, Jbeyq!"),
		("!@#$%^&*()_+-=", "!@#$%^&*()_+-="),
	]

	def test_rot13(self) -> None:
		for inp,out in self.test_cases:
			self.assertEqual(rot13(inp), out, f"{inp=}")


if __name__ == "__main__":
	unittest.main()
