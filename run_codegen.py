from grpc_tools import protoc

protoc.main(
    (
	'',
	'-I./protos',
	'--python_out=./protos',
	'--grpc_python_out=./protos',
	'./protos/*.proto',
    )
)