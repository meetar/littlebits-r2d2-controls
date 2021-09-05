import asyncio
import logging
import uuid

from bleak import discover
from bleak import BleakClient

devices_dict = {}
devices_list = []
receive_data = []

# device = None

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
        # if dev[i].name == "w32 ControlHub":
        #     print("found hub:", dev[i])
        #     print("setting device to", dev[i].address)
        #     global device
        #     device = dev[i].address

#An easy notify function, just print the recieve data
def notification_handler(sender, data):
    print(', '.join('{:02x}'.format(x) for x in data))

async def run(address, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address) as client:
        x = client.is_connected
        log.info("Connected: {0}".format(x))

        svcs = await client.get_services()
        # print("Services:")
        # for service in svcs:
        #     print(service)
        value = await client.read_gatt_descriptor(13)
        print('value:', value)

        for service in client.services:
            log.info("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                log.info(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    log.info(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )

        #Characteristic uuid
        rw_charac = "d9d9e9e1-aa4e-4797-8151-cb41cedaf2ad"
        await client.start_notify(rw_charac, notification_handler)

        await asyncio.sleep(2.0)  # Sleeping just to make sure the response is not missed...

        await client.stop_notify(rw_charac)

if __name__ == "__main__":
    print("Scanning for devices...")
    # Build an event loop
    loop = asyncio.get_event_loop()
    # Run the discover event
    loop.run_until_complete(scan())

    # global device
    address = "44D5602F-186F-4228-B934-D91B61574A78"

    #let user chose the device
    index = input('please select device from 0 to ' + str(len(devices_list)) + ":")
    index = int(index)
    address = devices_list[index]
    # global device
    # print('checking', device)
    # address = device
    # address = device
    uuid = devices_dict[address][1][0]
    print("Address is", address)
    print("uuid is", uuid)
    print("dict? ", devices_dict[address])
    print("dict: ")
    for x in devices_dict:
        print (x)

    #Run notify event
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address, True))