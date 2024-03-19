import os
import platform
from grpc_tools import protoc


if __name__ == "__main__":
	target_dir = "./protos"
	destination_dir = "pypb2"
	clients_dir = "clients"
	print("Start Compile Protobufs")
	print(f"Compile Targets From {target_dir}")
	print(f"Compile Destination To ./{destination_dir} & ./{destination_dir}/{clients_dir}")
	if platform.system() == "Windows":
		protoc.main(
			(
			'',
			'-Ipypb2=./protos',
			'--python_out=.',
			'--grpc_python_out=.',
			'--python_out=./clients',
			'--grpc_python_out=./clients',
			f'{target_dir}/*.proto',
			)
		)
		print("Compile Protobufs Success")
	elif platform.system() == "Linux":
		proto_files = []
		for file_inner in os.listdir(target_dir):
			if not file_inner.endswith(".proto"):
				continue
			proto_files.append(os.path.join(target_dir, file_inner))
		protoc.main(
			(
			'',
			'-Ipypb2=./protos',
			'--python_out=.',
			'--grpc_python_out=.',
			'--python_out=./clients',
			'--grpc_python_out=./clients',
			" ".join(proto_files),
			)
		)
		print("Compile Protobufs Success")
	else:
		print("Unsupport Platform")

