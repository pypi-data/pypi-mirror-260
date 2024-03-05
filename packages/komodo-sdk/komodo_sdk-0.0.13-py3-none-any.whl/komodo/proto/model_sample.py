from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse as JsonToMessage

from komodo.proto.model_pb2 import User, Appliance

user = User(guid="123456", email="john.doe@acme.com", name="John Doe")
print(user)

## Test Json conversion
user_json = MessageToJson(user, indent=0).replace("\n", "")
print(user_json)
message = JsonToMessage(user_json, User())
print(message)
assert message == user  # True

## Test Serialization
ser = user.SerializeToString()
print(ser)
deser = User.FromString(ser)
print(deser)

appliance = Appliance(guid="123456", name="ACME 123", purpose="Building Automation")
print(appliance)
