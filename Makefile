default:
	flask --app main run
lint:
	mypy source
