import asyncio
from bleak import BleakScanner

async def scan_ble_devices():
    # return_adv=True मुळे BLEDevice आणि AdvertisementData दोन्ही मिळतात
    devices_dict = await BleakScanner.discover(timeout=5.0, return_adv=True)
    device_list = []
    
    for device, adv_data in devices_dict.values():
        name = device.name if device.name else "Unknown / Nearby Device"
        address = device.address
        rssi = adv_data.rssi  # RSSI इथे असतो
        
        device_list.append({
            "name": name,
            "address": address,
            "rssi": rssi,
            "is_connected": False
        })
        
    return device_list