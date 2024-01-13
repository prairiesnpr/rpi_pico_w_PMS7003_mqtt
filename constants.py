from secrets import UNIQE_ID_PRE

LED_ENABLE = True
LED_PIN = "LED"
PMS_SET_PIN = 3  # Sleep
PMS_RST_PIN = 4

PMS_PERIOD = 300000  # (5 Min) in ms
PMS_WARM_PER = 30000  # ms (30 Seconds) in ms
PMS_RD_DEL = 5000  # ms
PMS_RD_CNT = 10

MQTT_PREFIX = "isilentllc"
MQTT_STATUS = "status"
MQTT_CLIENT = "aqi"

AV_MSG = "online"


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

VER = 1
MDL = "Air Quality 7003"
MNF = "iSilent LLC"
AREA = "Living Room"
DEV = "iSilentLLC_AQI"
NAME = f"{MNF} {MDL}"

ID = f"{DEV}_{UNIQE_ID_PRE}"

ST_BASE = f"{ID}/status"
CMD_TPC = f"{ID}/command"
AV_TPC = ST_BASE + "/availability"
ST_TPC = ST_BASE + "/readings"

CFG_DEV = {
    "sw": VER,
    "mdl": MDL,
    "mf": MNF,
    "sa": AREA,
    "name": NAME,
    "ids": [ID],
}


BASE_CFG = {
    "~": ID,
    "state_topic": "~/status/readings",
    "avty_t": "~/status/availability",
    "device": CFG_DEV,
}

CONFIG_SETTINGS = {
    "PM1_0": {
        "name": "PM\u2081",
        "dev_cla": "pm1",
        "uniq_id": UNIQE_ID_PRE + "-pm1",
        "val_tpl": "{{ value_json.PM1_0 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM2_5": {
        "name": "PM\u2082\u2085",
        "dev_cla": "pm25",
        "uniq_id": UNIQE_ID_PRE + "-pm25",
        "val_tpl": "{{ value_json.PM2_5 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM10_0": {
        "name": "PM\u2081\u2080",
        "dev_cla": "pm10",
        "uniq_id": UNIQE_ID_PRE + "-pm10",
        "val_tpl": "{{ value_json.PM10_0 }}",
        "unit_of_meas": "µg/m³",
    },
    "PM1_0_ATM": {
        "name": "PM\u2081 ATM",
        "dev_cla": "pm1",
        "uniq_id": UNIQE_ID_PRE + "-pm1a",
        "val_tpl": "{{ value_json.PM1_0_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PM2_5_ATM": {
        "name": "PM\u2082\u2085 ATM",
        "dev_cla": "pm25",
        "uniq_id": UNIQE_ID_PRE + "-pm25a",
        "val_tpl": "{{ value_json.PM2_5_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PM10_0_ATM": {
        "name": "PM\u2081\u2080 ATM",
        "dev_cla": "pm10",
        "uniq_id": UNIQE_ID_PRE + "-pm10a",
        "val_tpl": "{{ value_json.PM10_0_ATM }}",
        "unit_of_meas": "µg/m³",
    },
    "PCNT_0_3": {
        "name": "0.3\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt0_3",
        "val_tpl": "{{ value_json.PCNT_0_3 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_0_5": {
        "name": "0.5\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt0_5",
        "val_tpl": "{{ value_json.PCNT_0_5 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_1_0": {
        "name": "1.0\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt1_0",
        "val_tpl": "{{ value_json.PCNT_1_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_2_5": {
        "name": "2.5\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt2_5",
        "val_tpl": "{{ value_json.PCNT_2_5 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_5_0": {
        "name": "5.0\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt5_0",
        "val_tpl": "{{ value_json.PCNT_5_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "PCNT_10_0": {
        "name": "10.0\u00B5\u006d Particle Count",
        "uniq_id": UNIQE_ID_PRE + "-prt10_0",
        "val_tpl": "{{ value_json.PCNT_10_0 }}",
        "unit_of_meas": "particles/0.1 liter",
    },
    "AQI": {
        "name": "Air Quality Index",
        "dev_cla": "aqi",
        "uniq_id": UNIQE_ID_PRE + "-aqi",
        "val_tpl": "{{ value_json.AQI }}",
        "unit_of_meas": "",
    },
}


