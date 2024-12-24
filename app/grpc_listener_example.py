from concurrent import futures

import grpc

from proto import message_pb2 as message_proto_buffer
from proto import message_pb2_grpc as message_proto_buffer_grpc


class MessageService(message_proto_buffer_grpc.MessageServiceServicer):
    def SendMessage(self, request, context):
        try:
            print(f"수신된 메시지: {request.message}")
            return message_proto_buffer.MessageResponse(
                status=message_proto_buffer.MessageResponse.Status.SUCCESS
            )
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return message_proto_buffer.MessageResponse(
                status=message_proto_buffer.MessageResponse.Status.FAILURE
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_proto_buffer_grpc.add_MessageServiceServicer_to_server(
        MessageService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("서버 실행 중...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
