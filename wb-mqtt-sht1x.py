#!/usr/bin/python
import sys
import json

import mosquitto

import sht1x


def main():
    if len(sys.argv) < 2:
        raise RuntimeError('USAGE: ./wb-mqtt-sht1x.py <config file>')

    config_fname = sys.argv[1]
    config = json.load(open(config_fname))


    for param in ('data_gpio', 'sck_gpio'):
        if param not in config:
            raise RuntimeError('mandatory option %s is missing in config file' % param)
        if not isinstance(config.get(param), int):
            raise RuntimeError('invalid %s option: integer is required' % param)


    update_interval = config.get('update_interval', 5)

    mqtt_device_id = config.get('device_id', 'sht1x').encode('utf8')
    device_name = config.get('device_name', "SHT1x Sensor").encode('utf8')

    sensor = sht1x.WaitingSht1x(config['data_gpio'], config['sck_gpio'])

    client = mosquitto.Mosquitto()
    client.connect("127.0.0.1")

    client.publish("/devices/%s/meta/name" % mqtt_device_id, device_name, 0, True)

    client.publish("/devices/%s/controls/temperature/meta/type" % mqtt_device_id, "temperature", 0, True)
    client.publish("/devices/%s/controls/humidity/meta/type" % mqtt_device_id, "rel_humidity", 0, True)



    while client.loop(update_interval) == 0:
        temp, hum = sensor.read_temperature_and_Humidity()

        client.publish("/devices/%s/controls/temperature" % mqtt_device_id, str(temp), 0, True)
        client.publish("/devices/%s/controls/humidity" % mqtt_device_id, str(hum), 0, True)

if __name__ == '__main__':
    main()

