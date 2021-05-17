
run-client:
	python client.py

run-server:
	python server.py

format-client:
	python -m isort client
	python -m yapf --recursive --in-place --parallel client

format-server:
	python -m isort server
	python -m yapf --recursive --in-place --parallel server

format-all:
	python -m isort .
	python -m yapf --recursive --in-place --parallel */*.py

run-tests:
	python -m unittest discover -v -s "./test" -p "test_*.py"
