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

        # quit()

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

        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)
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
            rw_charac = "d9d9e9e1-aa4e-4797-8151-cb41cedaf2ad" # w32
            # rw_charac = "f8e49401-16f2-457e-8426-0fbce4eac6dc" # w33
            await client.start_notify(rw_charac, notification_handler)

            # await asyncio.sleep(2.0)  # Sleeping just to make sure the response is not missed...
            value = await client.read_gatt_descriptor(13)
            print('initial value 13:', hexlify(value))
            # value = await client.read_gatt_descriptor(11)
            # print('initial value 11:', hexlify(value))


            print("Connected, start typing and press ENTER...")

            loop = asyncio.get_event_loop()

            # for x in range(21998857063042, 21998872720828, 1):
            for x in range(21998857063042, 21998872720828, 256):
                hx = hex(x)[2:]
                print(x, hx)
                data = bytearray.fromhex(hx)
                await client.write_gatt_char(rw_charac, data, response=True)            
                await asyncio.sleep(0.05)

            print("FINISHED")
            await client.stop_notify(rw_charac)

if __name__ == "__main__":
    print("Scanning for peripherals...")
    # Build an event loop
    loop = asyncio.get_event_loop()
    # Run the discover event
    loop.run_until_complete(scan())

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
