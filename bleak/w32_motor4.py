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

        addresses=  [
            "140202897BCC",
"140202FF659D",
"140202FA3538",
"140202F6F4B4",
"140202F2B430",
"140202ED57EE",
"140202EA2709",
"140202E6E685",
"140202E3B620",
"140202DF41FF",
"140202DA115A",
"140202D6D0D6",
"140202D29052",
"140202CE43EF",
"140202CA036B",
"140202C5F284",
"140202C28263",
"140202BE3D78",
"140202BA7DFC",
"140202B6BC70",
"140202B2FCF4",
"140202AB7FEC",
"140202AA6FCD",
"140202A6AE41",
"140202A2EEC5",
"140202A1DEA6",
"1402029E191A",
"1402029969FD",
"140202969812",
"14020292D896",
"1402028D3B48",
"1402028A4BAF",
"140202897BCC",
"1402027DD457",
"1402027994D3",
"14020276653C",
"1402027225B8",
"1402026EF605",
"1402026DC666",
"1402026896C3",
"1402026327A8",
"1402026107EA",
"1402025CE014",
"14020259B0B1",
"14020255713D",
"140202502198",
"1402024B82C2",
"14020249A280",
"14020245630C",
"140202412388",
"1402023BFC55",
"14020239DC17",
"140202337D5D",
"140202304D3E",
"1402022BEE64",
"14020229CE26",
"140202214F2E",
"140202205F0F",
"1402021BD837",
"14020218E854",
"1402021429D8",
"1402020F8A82",
"1402020CBAE1",
"140202070B8A"]

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
