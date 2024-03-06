from setuptools import setup
import os

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
readme_loc = os.path.join(location, 'README.md')

long_description = open(readme_loc).read()
setup(name="keylock",
version="1.0.0",
description="Encryptor For Python and Bash and Decryptor for Python",
long_description=long_description,
long_description_content_type='text/markdown',
author="CodingSangh",
py_modules=['setup'],
url="https://github.com/CodingSangh/keylock",
scripts=["keylock"],
install_requires= ['requests', 'colourfulprint==1.5'],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
