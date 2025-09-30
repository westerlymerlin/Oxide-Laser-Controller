# None

<a id="analogue_class"></a>

# analogue\_class

Initializes and manages analogue-to-digital converter functionality.

This module provides functions to initialize and configure the analogue-to-digital
converter (ADC) interface, fetch individual or collective input channel values, and
validate analogue channel keys. The module ensures compatibility with ADC devices
by dynamically checking their presence and functionality at runtime.

<a id="analogue_class.settings"></a>

## settings

<a id="analogue_class.logger"></a>

## logger

<a id="analogue_class.analogue_channels"></a>

#### analogue\_channels

<a id="analogue_class.ADC_DEVICE"></a>

#### ADC\_DEVICE

<a id="analogue_class.init_analogue"></a>

#### init\_analogue

```python
def init_analogue()
```

Initializes the analogue interface by setting up the I2C connection and
checking for the presence of the analogue to digital converter (ADC).

This function determines if the analogue interface is installed and operational.
It scans for connected I2C devices and logs whether the analogue to digital
converter (ADC) is successfully connected at the specified address.
If the ADC is not found, the 'analogue_installed' setting is updated to False,
and a warning is logged.

<a id="analogue_class.check_analogue_key"></a>

#### check\_analogue\_key

```python
def check_analogue_key(item)
```

Check if the given item matches a digital key based on a predefined prefix.

This function iterates through a range of identifiers and checks if the
provided item matches a specific format comprising a digital prefix and an
identifier value. If a match is found, it returns True. Otherwise, it
returns False.

<a id="analogue_class.analogue_single_channel"></a>

#### analogue\_single\_channel

```python
def analogue_single_channel(item, command)
```

Executes a single analogue channel operation by evaluating the provided channel and command. This function
validates if the analogue-to-digital converter is installed and performs the necessary operation to fetch
the voltage value from the specified channel.

Warns if the analogue-to-digital converter is not installed, or if the specified channel is not enabled.
Returns the operation status with voltage information where applicable.

<a id="analogue_class.analogue_all_values"></a>

#### analogue\_all\_values

```python
def analogue_all_values(item, command, log_error=True)
```

Retrieve current analogue input values for all configured channels.

This function checks if the analogue-to-digital converter (ADC) is installed,
and if it is, gathers the voltage readings from enabled analogue channels.
If a channel is disabled, its status will be set to -1. If the ADC is not installed,
the function logs a warning and returns a status indicating its unavailability.

