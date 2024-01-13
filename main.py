from lib.mqtt_as import MQTTClient, config
import uasyncio as asyncio
import json
import time
import machine
from machine import Timer, Pin
from threadsafe import Message
import _thread


from pms7003 import PassivePms7003, UartError
from math_f import iqr_filter, median

from aqi import AQI

from constants import (
    MQTT_CLIENT,
    SELECTED_SENSORS,
    MQTT_PREFIX,
    CONFIG_SETTINGS,
    CFG_DEV,
    DEV,
    UNIQE_ID_PRE,
    ID,
    BASE_CFG,
    AV_TPC,
    AV_MSG,
    PMS_PERIOD,
    PMS_WARM_PER,
    PMS_RD_DEL,
    PMS_RD_CNT,
    LED_ENABLE,
    LED_PIN,
    PMS_SET_PIN,
    PMS_RST_PIN,
    ST_TPC,
)

from secrets import WIFI_AP, WIFI_PWD, MQTT_HOST, DEVICE_LOCATION



# Local configuration
config["ssid"] = WIFI_AP
config["wifi_pw"] = WIFI_PWD
config["server"] = MQTT_HOST

aqi_read_buffer = []
try:
    time.sleep(1)
    pms = PassivePms7003(uart=1)
except UartError:
    print("failed to reach pms")
    machine.reset()
except TypeError:
    print("pms typeerror")
    machine.reset()


pms_sleep = Pin(PMS_SET_PIN, Pin.OUT, Pin.PULL_DOWN)
pms_enable = Pin(PMS_RST_PIN, Pin.OUT, Pin.PULL_DOWN)
led = Pin(LED_PIN, Pin.OUT)


async def unblock(func, *args, **kwargs):
    def wrap(func, message, args, kwargs):
        message.set(func(*args, **kwargs))  # Run the blocking function.
    msg = Message()
    _thread.start_new_thread(wrap, (func, msg, args, kwargs))
    return await msg

async def read_value(wait_time):
    global aqi_read_buffer
    global pms

    await asyncio.sleep_ms(wait_time)
    print("Wake")
    pms.wakeup()
    await asyncio.sleep(
        3
    )  # Need a better option, this was the lowest value that didn't cause a crash

    print("Read")
    pms_data = await unblock(pms.read)
    aqi_class = AQI()
    pms_data["AQI"] = aqi_class.aqi(pms_data["PM2_5_ATM"], pms_data["PM10_0_ATM"])
    #pms_data["AQI"] = await unblock(aqi_class.aqi, (aqi_class, pms_data["PM2_5_ATM"], pms_data["PM10_0_ATM"]))
    #pms_data["AQI"] = await aqi.aqi(pms_data["PM2_5_ATM"], pms_data["PM10_0_ATM"])
    aqi_read_buffer.append(pms_data)

async def send_sensor_data(client, data, topic):
    await client.publish(
         topic, json.dumps(data).encode("utf_8"), qos=1, retain=False
    )
   

async def read_aqi_sensor(client):
    led.on()
    pms_enable.on()
    pms_sleep.on()

    global aqi_read_buffer
    aqi_read_buffer = []
    
    print("waiting on warm up")
    await asyncio.sleep_ms(PMS_WARM_PER) # Let sensor warm up
    print("warm up complete")

    tasks = []
    for i in range(PMS_RD_CNT):
        print("Scheduling read task %s" % i)
        tasks.append(asyncio.create_task(read_value(PMS_RD_DEL * i)))
        

    await asyncio.gather(*tasks)

    print("All tasks complete")

    result = {}
    for key in SELECTED_SENSORS:
        value_list = []
        for value in aqi_read_buffer:
            value_list.append(value.get(key))
        iqr_res = iqr_filter(value_list)
        result[key] = median(iqr_res)

    print("iqr result")
    print(result)
    print("Sleep")
    try:
        pms.sleep()
    except UartError:
        print("Bad Sleep Rsp")
        pass
    pms_sleep.off()  # Sleep
    pms_enable.off()  # Disable

    asyncio.create_task(send_sensor_data(client, result, ST_TPC))



async def send_config(client):  # Send Config Message
    for sensor_id in SELECTED_SENSORS:
        config_topic = f"{MQTT_PREFIX}/sensor/{ID}/{sensor_id}/config"
        asyncio.create_task(send_sensor_config(client, sensor_id, config_topic))

async def send_sensor_config(client, sensor_id, config_topic):
    cfg_msg = CONFIG_SETTINGS.get(sensor_id)
    cfg_msg.update(BASE_CFG)
    await client.publish(
         config_topic, json.dumps(cfg_msg).encode("utf_8"), qos=1, retain=True
    )


async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await send_config(client)


async def main(client):
    await client.connect()
    for coroutine in (
        up,
    ):
        asyncio.create_task(coroutine(client))
    
    last_read = time.ticks_ms() - PMS_PERIOD

    while True:
        await asyncio.sleep(5)
        # If WiFi is down the following will pause for the duration.
        await client.publish(AV_TPC, AV_MSG.encode("utf_8"), qos=1)

        print((time.ticks_ms() - last_read))
        if (time.ticks_ms() - last_read) > PMS_PERIOD:
            print("schedule reads")
            asyncio.create_task(read_aqi_sensor(client))
            last_read = time.ticks_ms()



config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages

try: 
    client = MQTTClient(config)
except OSError:
    machine.reset()
try:
    asyncio.run(main(client))
except OSError:
    machine.reset()
finally:
    client.close()  # Prevent LmacRxBlk:1 errors   