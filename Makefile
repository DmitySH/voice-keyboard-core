.PHONY: run
run:
	python main.py -p windows -c C:\Users\dm1tr\Desktop\voice-keyboard-core\commands\commands.json

.PHONY: proto-python
proto-python:
	python -m grpc_tools.protoc -I./pb --python_out=./pb --pyi_out=./pb --grpc_python_out=./pb ./pb/commands/commands.proto
	python -m grpc_tools.protoc -I./pb --python_out=./pb --pyi_out=./pb --grpc_python_out=./pb ./pb/app_control/app_control.proto

.PHONY: proto-swift
proto-swift:
	protoc --swift_out=. --grpc-swift_out=. ./pb/commands/commands.proto
	protoc --swift_out=. --grpc-swift_out=. ./pb/app_control/app_control.proto
