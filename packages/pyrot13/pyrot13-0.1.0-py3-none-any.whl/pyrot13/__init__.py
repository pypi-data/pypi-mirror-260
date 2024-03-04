""" rot13 rotate letters by 13 place. """


def rot13(s: str) -> str:
	""" rot13 returns a copy of s but each letter is rotated by 13 places. """
	out = []
	for c in s:
		if ord("a") <= ord(c) <= ord("z"):
			x = ord(c) - ord("a") + 13
			y = ord("a") + x%26
			out.append(chr(y))
		elif ord("A") <= ord(c) <= ord("Z"):
			x = ord(c) - ord("A") + 13
			y = ord("A") + x%26
			out.append(chr(y))
		else:
			out.append(c)
	return "".join(out)
