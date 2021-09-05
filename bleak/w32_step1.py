import asyncio
import logging
import uuid

from bleak import discover, BleakClient, BleakScanner, BleakError

from binascii import hexlify

devices_dict = {}
devices_list = []
receive_data = []

device = None

#To discover BLE devices nearby 
async def scan():
    dev = await discover()
    for i in range(0,len(dev)):
        #Print the devices discovered
        print("[" + str(i) + "]",'',dev[i].address,'',dev[i].name,'',dev[i].metadata["uuids"])
        #Put devices information into list
        devices_dict[dev[i].address] = []
        devices_dict[dev[i].address].append(dev[i].name)
        devices_dict[dev[i].address].append(dev[i].metadata["uuids"])
        devices_list.append(dev[i].address)
        if dev[i].name == "w32 ControlHub":
            print("found hub:", dev[i])
            global device
            print("setting device to", dev[i].address)
            device = dev[i].address
    print('device:', device)
    if device == None:
        print('device not found')

#An easy notify function, just print the recieve data
def notification_handler(sender, data):
    print(', '.join('{:02x}'.format(x) for x in data))

def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

async def run(address, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)
    
    # address = "44D5602F-186F-4228-B934-D91B61574A78"
    global device
    device = await BleakScanner.find_device_by_address(address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {address} could not be found.")

    async with BleakClient(address, disconnected_callback=handle_disconnect) as client:
    # async with device as client:
        x = client.is_connected
        log.info("Connected: {0}".format(x))


        #Characteristic uuid
        rw_charac = "d9d9e9e1-aa4e-4797-8151-cb41cedaf2ad" # w32
        # rw_charac = "f8e49401-16f2-457e-8426-0fbce4eac6dc" # w33

        await client.start_notify(rw_charac, notification_handler)
        loop = asyncio.get_event_loop()

        addresses=  ["140202897BCC",
"140201FC00AD", # right
"140201EA725A",
"140201E49394",
"140201DF14AC",
"140201D9746A",
"140201D1F562",
"140201CC36FE",
"140201C697B4",
"140201C0F772",
"140201B918CC",
"140201B4C961",
"140201AE7A1A",
"140201A7EB33",
"140201A2BB96",
"1402019C6C0B", #
"14020196CD41", #
"14020190AD87",
"1402018A1EFC",
"14020184FF32",
"1402017EB167", # middle!
"14020178D1A1",
"1402017270EB",
"1402016C8314",
"14020166225E",
"140201604298",
"1402015AD581",
"14020154344F",
"1402014F9715",
"14020149F7D3",
"1402014246B8",
"1402013CD9E1",
"1402013548C8",
"140201002E3E", # left
        ]

        # for y in range(3):
        for x in addresses:
            print(x)
            data = bytearray.fromhex(bytes(x, 'utf-8').decode('utf-8'))
            # print(data)
            await client.write_gatt_char(rw_charac, data, response=True)
            await asyncio.sleep(1)


        await client.stop_notify(rw_charac)



if __name__ == "__main__":
    # print("Scanning for peripherals...")
    # # Build an event loop
    # loop = asyncio.get_event_loop()
    # # Run the discover event
    # loop.run_until_complete(scan())

    # global device
    address = "44D5602F-186F-4228-B934-D91B61574A78" # W32
    # address = "6D46D478-28F6-4877-A7F7-B8BB008E89E2" # W33

    # global device
    # device = await BleakScanner.find_device_by_address(address, timeout=20.0)

    #Run notify event
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address, True))
    # asyncio.run(show_disconnect_handling())
    exit()
