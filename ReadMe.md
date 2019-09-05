rdfind.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
=========
![GitLab Build Status](https://gitlab.com/KOLANICH/rdfind.py/badges/master/pipeline.svg)
![GitLab Coverage](https://gitlab.com/KOLANICH/rdfind.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/rdfind.py.svg)](https://coveralls.io/r/KOLANICH/rdfind.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/rdfind.py.svg)](https://libraries.io/github/KOLANICH/rdfind.py)
[![Gitter.im](https://badges.gitter.im/rdfind.py/Lobby.svg)](https://gitter.im/rdfind.py/Lobby)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://github.com/KOLANICH-tools/antiflash.py)

This is just a parser of [`rdfind`](https://github.com/pauldreik/rdfind) ![Licence](https://img.shields.io/github/license/pauldreik/rdfind.svg)
[![TravisCI Build Status](https://travis-ci.org/pauldreik/rdfind.svg?branch=master)](https://travis-ci.org/pauldreik/rdfind)
[![Coveralls Coverage](https://img.shields.io/coveralls/pauldreik/rdfind.svg)](https://coveralls.io/r/pauldreik/rdfind)
[![Libraries.io Status](https://img.shields.io/librariesio/github/pauldreik/rdfind.svg)](https://libraries.io/github/pauldreik/rdfind), output. It allows you to customize deduplication process a bit. `rdfind` finds dupes and you decide what to do with them.

Requirements
------------
* [`Python >=3.4`](https://www.python.org/downloads/). [`Python 2` is dead, stop raping its corpse.](https://python3statement.org/) Use `2to3` with manual postprocessing to migrate incompatible code to `3`. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their `dict` is ordered and deterministic. Python 3 is also semi-dead, 3.7 is the last minor release in 3.
* [`rdfind`](https://github.com/pauldreik/rdfind) ![Licence](https://img.shields.io/github/license/pauldreik/rdfind.svg) [![TravisCI Build Status](https://travis-ci.org/pauldreik/rdfind.svg?branch=master)](https://travis-ci.org/pauldreik/rdfind) [![Libraries.io Status](https://img.shields.io/librariesio/github/pauldreik/rdfind.svg)](https://libraries.io/github/pauldreik/rdfind)
* [`sh`](https://github.com/amoffat/sh) ![Licence](https://img.shields.io/github/license/amoffat/sh.svg) [![PyPi Status](https://img.shields.io/pypi/v/sh.svg)](https://pypi.python.org/pypi/sh) [![TravisCI Build Status](https://travis-ci.org/amoffat/sh.svg?branch=master)](https://travis-ci.org/amoffat/sh) [![CodeCov Coverage](https://codecov.io/github/amoffat/sh/coverage.svg?branch=master)](https://codecov.io/github/amoffat/sh/) [![Libraries.io Status](https://img.shields.io/librariesio/github/amoffat/sh.svg)](https://libraries.io/github/amoffat/sh)
