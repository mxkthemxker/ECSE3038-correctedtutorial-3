
from fastapi import FastAPI, HTTPException

app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall", "temp": 27.4, "online": True},
    {"name": "hall-lamp", "room": "hall", "temp": 26.1, "online": True},
    {"name": "attic", "room": "attic", "temp": 31.9, "online": True},
    {"name": "fridge", "room": "kitchen", "temp": 4.2, "online": False},
    {"name": "patio", "room": "outside", "temp": 29.8, "online": True},
]


def list_devices(devices):
    for device in devices:
        print(f"Device: {device['name']}, Temperature: {device['temp']},")

list_devices(readings)

def average_temp(devices):
    total_temp = 0

    for device in devices:
        total_temp = total_temp + device["temp"]
    return total_temp / len(devices)
print(f"Average temperature: {average_temp(readings)}")

def hottest_device(devices):
    hottest = devices[0]

    for device in devices:
        if device["temp"] > hottest["temp"]:
            hottest = device

    return hottest
print(f"Hottest device: {hottest_device(readings)}")


@app.get("/devices")
def get_devices():
    return readings


@app.get("/devices/hottest")
def get_hottest():
    return hottest_device(readings)


@app.get("/devices/online")
def get_online_devices():
    online_devices = []

    for device in readings:
        if device["online"] == True:
            online_devices.append(device)

    return online_devices


@app.get("/devices/{name}")
def get_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device

    raise HTTPException(
        status_code=404,
        detail="No device called " + name
    )


@app.get("/stats")
def get_stats():
    return {
        "average_temperature": round(average_temp(readings), 2)
    }

