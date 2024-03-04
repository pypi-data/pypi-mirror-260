# Copyright 2023-2024 Amir Ali Malekani Nezhad.
#
# Licensed under the GPL Ver 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/ACE07-Sev/QRandom/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Quantum Random Number Generator.'
LONG_DESCRIPTION = '`qoin` is the analogue of `random` package implemented through gate-based quantum computing.'

# Setting up
setup(
    name="qoin",
    version=VERSION,
    author="Amir Ali Malekani Nezhad",
    author_email="<amiralimlk07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'qiskit', 'qiskit_aer'],
    keywords=['quantum computing', 'quantum random number generator', 'random', 'qrandom', 'qoin'],
    classifiers=[
        "Development Status :: DONE",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)