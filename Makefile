
client:
	python client.py

server:
	python server.py

tests:
	python -m unittest discover -v -s "./test" -p "test_*.py"
