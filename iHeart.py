import asyncio
from socketserver import DatagramRequestHandler
from turtle import pu
from bleak import BleakScanner, BleakClient

class OximeterData:
    pulse = 0
    spo2 = 0
    ir1 = 0
    ir1Index = 0
    ir2 = 0
    ir2Index = 0

    def __init__(self, data: bytearray):
        self.pulse = data[2]
        self.spo2 = data[3]
        self.ir1 = int.from_bytes(data[4:7], byteorder='little')
        self.ir1Index = data[8]
        self.ir2 = int.from_bytes(data[9:12], byteorder='little')
        self.ir2Index = data[13]

    def __str__(self):
        return f"Pulse: {self.pulse}, SpO2: {self.spo2}, IR1: {self.ir1}, IR1 Index: {self.ir1Index}, IR2: {self.ir2}, IR2 Index: {self.ir2Index}"

async def main():
    devices = await BleakScanner.discover()
    oximeterDevice = None
    for d in devices:
        if d.name == "iHeart":
            print(f"Oximeter found: {d.address}")
            oximeterDevice = d
            break

    if oximeterDevice == None:
        print("Oximeter not found")
    else:
        client = BleakClient(oximeterDevice.address)
        try:
            await client.connect()
            print("Connected")
            await client.start_notify(13, callback)
            print("Subscribed")
            await asyncio.sleep(3.0) 
        except Exception as e:
            print(e)
        finally:
            await client.disconnect()
            print("Disconnected")
            pass

def callback(sender: int, data: bytearray):
    od = OximeterData(data)
    print(f"RX: {od}")


asyncio.run(main())

