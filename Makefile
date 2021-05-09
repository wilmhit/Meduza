
run-client:
	python client.py

run-server:
	python server.py

run-tests:
	python -m unittest discover -v -s "./test" -p "test_*.py"
