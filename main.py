import network
import micropython
import time
import json
from machine import Timer, Pin
from umqtt.simple import MQTTClient


from pms7003 import PassivePms7003, UartError

from aqi import AQI

from constants import (
    MQTT_CLIENT,
    SELECTED_SENSORS,
    MQTT_PREFIX,
    CONFIG_SETTINGS,
    CONFIG_DEVICE,
    DEVICE,
    UNIQE_ID_PRE,
    PMS_PERIOD,
    PMS_WARM_PER,
    PMS_RD_DEL,
    PMS_RD_CNT,
    LED_ENABLE,
    LED_PIN,
    PMS_SET_PIN,
    PMS_RST_PIN,
)

from secrets import WIFI_AP, WIFI_PWD, MQTT_HOST, DEVICE_LOCATION

from math_f import iqr_filter, median

aqi_read_buffer = []
time.sleep(1)  # Won't start without a delay
pms = PassivePms7003(uart=1)
if LED_ENABLE:
    led = Pin(LED_PIN, Pin.OUT)
pms_sleep = Pin(PMS_SET_PIN, Pin.OUT, Pin.PULL_DOWN)
pms_enable = Pin(PMS_RST_PIN, Pin.OUT, Pin.PULL_DOWN)


def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_AP, WIFI_PWD)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)
    print(wlan.ifconfig())


def led_off():
    if LED_ENABLE:
        led.off()


def led_on():
    if LED_ENABLE:
        led.on()


def publish_json_value(server="localhost", topic="", value=""):
    led_off()
    c = MQTTClient(
        MQTT_CLIENT,
        server,
        keepalive=30,
    )
    c.connect()
    c.publish(topic.encode("utf_8"), json.dumps(value).encode("utf_8"))
    c.disconnect()
    led_on()


def mqtt_config():
    try:
        for sensor_type in SELECTED_SENSORS:
            sensor_id = f"sensor{DEVICE_LOCATION}{sensor_type}"
            sensor_prefix = f"{MQTT_PREFIX}/sensor"
            config_topic = f"{sensor_prefix}/{sensor_id}/config"
            config_payload = CONFIG_SETTINGS.get(sensor_type)
            config_payload.update(
                {
                    "name": sensor_type,
                    "state_topic": f"{sensor_prefix}/{DEVICE}_{UNIQE_ID_PRE}/state",
                    "device": CONFIG_DEVICE,
                }
            )
            publish_json_value(
                server=MQTT_HOST, topic=config_topic, value=config_payload
            )
        print("MQTT Config Complete")
        return True
    except Exception as e:
        print("MQTT Config Failed %s" % e)
        return False


def read_aqi_sensor(t_obj: Timer):
    pms_enable.on()
    pms_sleep.on()
    start_sensor_warmup()


def start_sensor_warmup():
    print("Clear buffer")

    global aqi_read_buffer
    aqi_read_buffer = []

    aqi_warm_tim = Timer()
    aqi_warm_tim.init(
        mode=Timer.ONE_SHOT, period=PMS_WARM_PER, callback=read_aqi_values
    )


def read_aqi_values(t: Timer):
    # Read values after warmup
    print("Schedule Reads")
    # schedule reads
    timers = []
    for i in range(PMS_RD_CNT):
        timers.append(Timer())
        timers[-1].init(
            mode=Timer.ONE_SHOT, period=PMS_RD_DEL * i, callback=schedule_read
        )


def schedule_read(t: Timer):
    micropython.schedule(read_value, 0)


def read_value(rd_ct: int):
    global aqi_read_buffer
    global pms

    print("Wake")
    pms.wakeup()
    time.sleep(
        3
    )  # Need a better option, this was the lowest value that didn't cause a crash

    print("Read")
    pms_data = pms.read()

    pms_data["AQI"] = AQI.aqi(pms_data["PM2_5_ATM"], pms_data["PM10_0_ATM"])
    aqi_read_buffer.append(pms_data)

    if len(aqi_read_buffer) == PMS_RD_CNT:
        print("read complete")
        filter_read_data(aqi_read_buffer)
        print("Sleep")
        try:
            pms.sleep()
        except UartError:
            print("Bad Sleep Rsp")
            pass
        pms_sleep.off()  # Sleep
        pms_enable.off()  # Disable


def filter_read_data(values: list):
    result = {}
    for key in SELECTED_SENSORS:
        value_list = []
        for value in values:
            value_list.append(value.get(key))
        iqr_res = iqr_filter(value_list)
        result[key] = median(iqr_res)

    print("iqr result")
    print(result)
    sensor_prefix = f"{MQTT_PREFIX}/sensor"
    state_topic = f"{sensor_prefix}/{DEVICE}_{UNIQE_ID_PRE}/state"
    publish_json_value(server=MQTT_HOST, topic=state_topic, value=result)


# Need to warm sensor up, discarding data
# Take readings
# Put sensor in standby

if __name__ == "__main__":
    print("### Start ###")
    pms_sleep.off()  # Sleep
    pms_enable.off()  # Disable
    led_off()
    connect_wlan()
    mqtt_connected = False
    while not mqtt_connected:
        mqtt_connected = mqtt_config()
        if not mqtt_connected:
            time.sleep(1)
    aqi_timer = Timer()
    aqi_timer.init(period=PMS_PERIOD, callback=read_aqi_sensor)
    read_aqi_sensor(aqi_timer) # Schedule Immediate Read
    led_on()
