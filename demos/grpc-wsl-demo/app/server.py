from concurrent import futures
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import test_pb2
import test_pb2_grpc

import time
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        age=request.age
        title=""
        if age>20 :
            title="Mr."
        else :
            title="Miss."   
        #time.sleep(5)        
        return helloworld_pb2.HelloReply(message=f"Message from server:Hello, {title} {request.name,request.flag}!", ) 

class Greeter2(test_pb2_grpc.GreeterServicer):
    def SayTest(self, request, context):       
        return test_pb2.TestReply(message=f"Message from server:Hello,{request.name}!", errorCode="0") 
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    test_pb2_grpc.add_GreeterServicer_to_server(Greeter2(), server)
    server.add_insecure_port("[::]:50051")  # 監聽 50051
    server.start()
    print("gRPC server listening on 0.0.0.0:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
