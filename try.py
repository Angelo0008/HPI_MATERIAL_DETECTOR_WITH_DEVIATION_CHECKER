#%%
# pip install pycomm3
from pycomm3 import CIPDriver

PLC_IP = "192.168.35.150"

with CIPDriver(PLC_IP) as plc:   # defaults to port 44818
    print("Connected?", plc.connected)

    # read a tag by name
    # result = plc.read('Tag_1')   # replace MyTag with your tag
    # if result:
    #     print('Value:', result.value)
    # else:
    #     print('Read failed or tag not found')


# %%
from cpppo.server.enip import client

PLC_IP = "192.168.35.150"

with client.connector(host=PLC_IP) as conn:
     

#%%