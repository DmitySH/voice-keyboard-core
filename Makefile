.PHONY: run-windows
run-windows:
	python main.py -p windows

.PHONY: run-macos
run-macos:
	python main.py -p macos
.PHONY: proto-python
proto-python:
	python -m grpc_tools.protoc -I./pb --python_out=./pb --pyi_out=./pb --grpc_python_out=./pb ./pb/commands/commands.proto
	python -m grpc_tools.protoc -I./pb --python_out=./pb --pyi_out=./pb --grpc_python_out=./pb ./pb/app_control/app_control.proto

.PHONY: proto-swift
proto-swift:
	protoc --swift_out=. --grpc-swift_out=. ./pb/commands/commands.proto
	protoc --swift_out=. --grpc-swift_out=. ./pb/app_control/app_control.proto
