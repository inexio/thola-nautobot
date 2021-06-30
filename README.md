# Thola Nautobot
The Integration of [Thola](https://github.com/inexio/thola) into [Nautobot](https://github.com/nautobot/nautobot)

Thola is a unified interface for communication with network devices. You can use it to retrieve live information of your network devices, independent of their vendor, type or model.

## Installation

The first thing you need is a running Thola API. Checkout Thola's [main repository](https://github.com/inexio/thola) to get information on how to install and start a Thola API.

Once this is done, we can install the Nautobot plugin for Thola.
You need to install thola-nautobot in the same python environment as your running nautobot instance.

Download and install the plugin using:

```
$ pip3 install thola-nautobot
```

Add thola-nautobot to your local requirements in the `NAUTOBOT_ROOT` directory.

```
$ echo thola-nautobot >> $NAUTOBOT_ROOT/local_requirements.txt
```

In your `nautobot_config.py`, add thola-nautobot to the `PLUGINS` list. Here you can also define special configuration parameters.

```python
PLUGINS = ["thola_nautobot"]

PLUGINS_CONFIG = {
  "thola_nautobot": {
    # ADD YOUR PARAMETERS HERE
  }
}
```

Next, run the database migrations.

```
$ nautobot-server migrate
```

Finally, restart the WSGI service to load the new plugin.

```
$ sudo systemctl restart nautobot nautobot-worker
```

That's it! Now you are ready to use Thola 🎉

## Usage

We now want to monitor our first device with Thola. To get started, we create a Thola configuration on that device. Open the device's detail view and search for the Thola panel. Click on `Enable`.

<img src="docs/img/enable_thola.png" alt="">

Thola mainly uses SNMP for communication. Therefore, you need to enter the SNMP credentials for your device. In case you rely on the default credentials, just leave these fields empty.

Once you click on `Create`, the Thola API you started before will connect to your device. So make sure to have the API running now.

If successful, you find an overview over all components that you can monitor on the given device. This depends on the type of device.

<img src="docs/img/components.png" alt="">

Now you can inspect the live status of your device by clicking on the `Live Status` tab. This shows the status of all available components for your device.

## Plugin Config

As stated before nautobot has a config file, where plugin parameters can be set:

```python
PLUGINS_CONFIG = {
  "thola_nautobot": {
    # ADD YOUR PARAMETERS HERE
  }
}
```

For thola_nautbot all parameters are optional. If a parameter is not set, the plugin will just use the default values.

| Parameter | Description | Type | Default value
|---|---|---|---|
| `thola_api` | Default Address and port of a running thola API | String | `"http://localhost:8237"` |
| `snmp_community` | Default SNMP community for a device | String | `"public"` |
| `snmp_version` | Default SNMP version for a device| String | `"2c"` |
| `snmp_port` | Default SNMP port for a device | Integer | `161` |
| `snmp_discover_par_requests` | Default amount of parallel connection requests used while trying to get a valid SNMP connection | Integer | `5` |
| `snmp_discover_timeout` | Default timeout in seconds used while trying to get a valid SNMP connection | Integer | `2` |
| `snmp_discover_retries` | Default number of retries used while trying to get a valid SNMP connection | Integer | `0` |

## API

The plugin comes with 6 API endpoints.

| Method | Route | Description |
|---|---|---|
| `GET` | `/plugins/thola_nautobot/tholadevice` | Returns list of all Thola configurations |
| `POST` | `/plugins/thola_nautobot/tholadevice` | Creates a new Thola configuration |
| `GET` | `/plugins/thola_nautobot/tholadevice/{id}` | Returns details of a given configuration |
| `PUT` | `/plugins/thola_nautobot/tholadevice/{id}` | Updates a given Thola configuration |
| `DELETE` | `/plugins/thola_nautobot/tholadevice/{id}` | Deletes a given Thola configuration |
| `GET` | `/plugins/thola_nautobot/tholadevice/{id}/livedata` | Returns available live data for a given Thola device |

## Any questions?

Feel free to look at the [main repository](https://github.com/inexio/thola) of Thola. Also, checkout our [website](https://thola.io).

### Missing a device?

If you run a device that Thola doesn't support yet, check out our [documentation](https://docs.thola.io/adding-device/writing-device-classes/). There you find a full explanation on how to add a new device type into Thola. We are happy to see your pull requests!