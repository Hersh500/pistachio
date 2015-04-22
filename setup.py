import re 
from setuptools import setup

version = re.search(
	'^__version__\s*=\s*"(.*)"',
	open('pistachio/pistachio.py').read(),
	re.M
	).group(1)

with open("README.md", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name = "pistachio-mail", 
	packages = ["pistachio"],
	entry_points = {
		"console_scripts": ['pistachio = pistachio.pistachio:main']
		},
	version = version, 
	description = "A simple command line tool to quickly view messages in your email.",
	long_description = long_descr,
	author = "Hersh Sanghvi", 
	author_email = "hersh500@gmail.com", 
	url = "https://github.com/Hersh500/pistachio",
	)
 
