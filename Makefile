help:
	@echo make install
	@echo make install-mac
	@echo make install-ubuntu
	@echo make run

install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

install-mac:
	brew install python-tk

install-ubuntu:
	sudo apt-get install python3-tk

run:
	python3 main.py
