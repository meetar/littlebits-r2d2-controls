import asyncio
from bleak import BleakScanner

# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

#To discover BLE devices nearby 
async def scan():
    dev = await discover()
    for i in range(0,len(dev)):
        #Print the devices discovered
        print("[" + str(i) + "]" + dev[i].address,dev[i].name,dev[i].metadata["uuids"])
        #Put devices information into list
        devices_dict[dev[i].address] = []
        devices_dict[dev[i].address].append(dev[i].name)
        devices_dict[dev[i].address].append(dev[i].metadata["uuids"])
        devices_list.append(dev[i].address)


from bleak import BleakClient

# address = "24:71:89:cc:09:05"
address = "3C:15:C2:E5:A9:11"
MODEL_NBR_UUID = "44D5602F-186F-4228-B934-D91B61574A78"

async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))