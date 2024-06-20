import doctest
import os
import unittest
import sys

paths = ['./docs', './ciw']

def load_tests(loader, tests, ignorex):
	for path in paths:
		for root, dirs, files in os.walk(path):
			for f in files:
				if f.endswith(".rst"):
					tests.addTests(
						doctest.DocFileSuite(
							os.path.join(root, f), optionflags=doctest.ELLIPSIS
						)
					)

		return tests


if __name__ == "__main__":
    if sys.version_info >= (3, 6):
        unittest.main()
