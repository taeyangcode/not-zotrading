default:
	python3 source/server.py | python3 main.py
lint:
	mypy source
