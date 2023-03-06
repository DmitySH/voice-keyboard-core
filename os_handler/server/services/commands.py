from pb import commands_pb2_grpc, commands_pb2


class CommandsService(commands_pb2_grpc.CommandsServicer):
    def AddCommand(self, request, context):
        print(request)
        resp = commands_pb2.AddCommandResponse(status=200, error='watafak')

        return resp
