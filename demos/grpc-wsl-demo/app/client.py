import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import test_pb2
import test_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        resp = stub.SayHello(helloworld_pb2.HelloRequest(name="Maxwell",age=10,flag=True))
        print("Greeter client received:", resp.message)
        stub2 = test_pb2_grpc.GreeterStub(channel)
        resp2 = stub2.SayTest(test_pb2.TestRequest(name="MaxwellTest"))
        print("Greeter client received:", resp2.message,resp2.errorCode)

if __name__ == "__main__":
    run()
