from secrets import UNIQE_ID_PRE

LED_ENABLE = True
LED_PIN = "LED"
PMS_SET_PIN = 3  # Sleep
PMS_RST_PIN = 4

PMS_PERIOD = 300000  # (5 Min)
PMS_WARM_PER = 10000  # ms (10 Seconds)
PMS_RD_DEL = 5000  # ms
PMS_RD_CNT = 10

MQTT_PREFIX = "isilentllc"
MQTT_STATUS = "isilentllc/status"
MQTT_CLIENT = "isilentllc_aqi"

SELECTED_SENSORS = [
    "PM1_0",
    "PM2_5",
    "PM10_0",
    "PM1_0_ATM",
    "PM2_5_ATM",
    "PM10_0_ATM",
    "PCNT_0_3",
    "PCNT_0_5",
    "PCNT_1_0",
    "PCNT_2_5",
    "PCNT_5_0",
    "PCNT_10_0",
    "AQI",
]

VERSION = 1
MODEL = "Air Quality 7003"
MANUFACTURER = "iSilent LLC"
AREA = "Living Room"
DEVICE = "iSilentLLC_AQI"
NAME = f"{MANUFACTURER} {MODEL}"


CONFIG_DEVICE = {
    "sw": VERSION,
    "mdl": MODEL,
    "mf": MANUFACTURER,
    "sa": AREA,
    "name": NAME,
    "ids": [f"{DEVICE}_{UNIQE_ID_PRE}"],
}


CONFIG_SETTINGS = {
    "PM1_0": {
        "dev_cla": "pm1",
        "uniq_id": UNIQE_ID_PRE + "-pm1",
        "val_tpl": "{{ value_json.PM1_0 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM2_5": {
        "dev_cla": "pm25",
        "uniq_id": UNIQE_ID_PRE + "-pm25",
        "val_tpl": "{{ value_json.PM2_5 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM10_0": {
        "dev_cla": "pm10",
        "uniq_id": UNIQE_ID_PRE + "-pm10",
        "val_tpl": "{{ value_json.PM10_0 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM1_0_ATM": {
        "dev_cla": "pm1",
        "uniq_id": UNIQE_ID_PRE + "-pm1a",
        "val_tpl": "{{ value_json.PM1_0_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PM2_5_ATM": {
        "dev_cla": "pm25",
        "uniq_id": UNIQE_ID_PRE + "-pm25a",
        "val_tpl": "{{ value_json.PM2_5_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PM10_0_ATM": {
        "dev_cla": "pm10",
        "uniq_id": UNIQE_ID_PRE + "-pm10a",
        "val_tpl": "{{ value_json.PM10_0_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PCNT_0_3": {
        "uniq_id": UNIQE_ID_PRE + "-prt0_3",
        "val_tpl": "{{ value_json.PCNT_0_3 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_0_5": {
        "uniq_id": UNIQE_ID_PRE + "-prt0_5",
        "val_tpl": "{{ value_json.PCNT_0_5 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_1_0": {
        "uniq_id": UNIQE_ID_PRE + "-prt1_0",
        "val_tpl": "{{ value_json.PCNT_1_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_2_5": {
        "uniq_id": UNIQE_ID_PRE + "-prt2_5",
        "val_tpl": "{{ value_json.PCNT_2_5 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_5_0": {
        "uniq_id": UNIQE_ID_PRE + "-prt5_0",
        "val_tpl": "{{ value_json.PCNT_5_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_10_0": {
        "uniq_id": UNIQE_ID_PRE + "-prt10_0",
        "val_tpl": "{{ value_json.PCNT_10_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "AQI": {
        "dev_cla": "aqi",
        "uniq_id": UNIQE_ID_PRE + "-aqi",
        "val_tpl": "{{ value_json.AQI }}",
        "unit_of_meas": "",
    },
}
