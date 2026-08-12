# The grcp tools generate:
#  This will generate pandas_pb2.py and pandas_pb2_grpc.py. Then in server.py:

import grpc
from concurrent import futures
import pandas_pb2_grpc
import pandas_pb2

class PandasService(pandas_pb2_grpc.PandasServiceServicer):
    def GetData(self, request, context):
        # Imagine you return serialized JSON here
        return pandas_pb2.DataFrameResponse(json_rows=["{\"a\":1}"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pandas_pb2_grpc.add_PandasServiceServicer_to_server(PandasService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()