# HoPRe: Homophone-based Pun Recognition
HoPRe is a pun-recognition software based on first-order logic and lambda calculus.

## Installation
All instructions below have only been tested with Ubuntu 20.04.6 LTS, specifically using WSL2 on Windows 10.
Please adapt and improvise along the way.
1. Clone this repository.
	```bash
	git clone https://github.com/pingpingy1/HoPRe.git
	cd HoPRe
	```
2. Download SWI-Prolog. ([Help](https://www.swi-prolog.org/build/PPA.html))
	```bash
	sudo apt-add-repository ppa:swi-prolog/stable
	sudo apt update
	sudo apt install swi-prolog
	swipl --version
	```
2. Create and activate a Python virtual environment.
	```bash
	pyenv virtualenv 3.10.7 hopre3107
	pyenv local hopre3107
	```
3. Install required packages.
	```bash
	python setup.py
	```
4. Run HoPRe.
	```bash
	python -m hopre.core
	```
