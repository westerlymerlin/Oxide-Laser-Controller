# None

<a id="config_class"></a>

# config\_class

Application Configuration

This module provides utilities for managing system configuration, network settings, and application naming.
It serves as the core configuration interface for the Raspberry Pi control application, handling both
network interfaces and application identity management.

Key Features:
    - Network configuration: Get and set network interface settings (DHCP/static)
    - IP address validation: Verify IP addresses and network class formats
    - Application naming: Manage application names with automatic sanitization
    - System hostname: Update system hostname based on application name

Functions:
    friendlydirname(sourcename): Sanitizes strings by removing invalid characters
    get_netifo(): Retrieves network configuration information
    validate_ipaddress(ip_str): Validates IPv4 address format
    validate_class(class_str): Validates network class (1-32)
    set_netinfo(mode, ip_addr, nwclass, df_gw, dns_server): Configures network interface
    set_appname(name): Updates application name in settings and system hostname

Dependencies:
    subprocess: For executing system commands
    re: For regex pattern matching
    app_control: For settings management
    logmanager: For logging configuration changes

<a id="config_class.subprocess"></a>

## subprocess

<a id="config_class.re"></a>

## re

<a id="config_class.settings"></a>

## settings

<a id="config_class.writesettings"></a>

## writesettings

<a id="config_class.friendlyname"></a>

## friendlyname

<a id="config_class.logger"></a>

## logger

<a id="config_class.updatesetting"></a>

#### updatesetting

```python
def updatesetting(newsetting)
```

Updates the global settings with the provided dictionary object.

This function takes a dictionary containing key-value pairs and updates the global `settings` object
with the provided data. Each key from the input dictionary will replace or create a corresponding
key in the global `settings`. After updating, the function calls `writesettings()` to persist the changes.

:param newsetting: A dictionary object containing key-value pairs to update the global settings.
:type newsetting: dict

<a id="config_class.get_netifo"></a>

#### get\_netifo

```python
def get_netifo()
```

Retrieve network configuration information for "Wired connection 1".

This function uses the `nmcli` command-line tool to fetch detailed network
configuration information. The configuration details are returned in the form
of a dictionary where keys correspond to the configuration parameter names,
and values to their respective settings.

:raises subprocess.SubprocessError: If the subprocess to execute `nmcli` fails.

:return: A dictionary containing network configuration information for
    "Wired connection 1". Keys are parameter names, and values are their
    associated configuration settings. The dictionary always contains
    at least the key `'ipv4.method'`, which defaults to `'unknown'` if
    not provided in the output of `nmcli`.
:rtype: dict

<a id="config_class.validate_ipaddress"></a>

#### validate\_ipaddress

```python
def validate_ipaddress(ip_str)
```

Validates whether the provided string is a valid IPv4 address.

This function checks if the input string matches the standard format of
an IPv4 address. IPv4 addresses are composed of four octets, separated
by periods, with each octet containing a numeric value between 0 and 255.
If the input string complies with the format, it is returned unchanged;
otherwise, the function returns False.

:param ip_str: The string to be tested for validity as an IPv4 address.
:type ip_str: str
:return: The original input string if it is a valid IPv4 address,
         otherwise returns False.
:rtype: Union[str, bool]

<a id="config_class.validate_class"></a>

#### validate\_class

```python
def validate_class(class_str)
```

Validates if the provided string is a class number between 1 and 32.

This function checks whether the input string matches the format for a valid
class number. A valid class number is represented as a string containing an
integer ranging from 1 to 32, inclusive. If the string satisfies the format,
it is returned; otherwise, the function returns False.

:param class_str: The string representing the class number to validate.
:type class_str: str
:return: The input string if it matches a valid class number format, or
    False if it does not.
:rtype: str or bool

<a id="config_class.set_netinfo"></a>

#### set\_netinfo

```python
def set_netinfo(mode, ip_addr, nwclass, df_gw, dns_server)
```

Sets network configuration either to DHCP (automatic) or static by specifying IP address, network class,
default gateway, and DNS server. Validates given parameters for correctness before applying the network settings.
If mode is 'auto', the system will use DHCP. For static configuration, the provided IP address, network class,
default gateway, and DNS server are validated and applied.

:param mode: The mode for network configuration ('auto' for DHCP or 'static').
:type mode: str
:param ip_addr: IP address to be set for static network configuration. Required if mode is 'static'.
:type ip_addr: str
:param nwclass: Network class to which the IP address belongs. Required if mode is 'static'.
:type nwclass: str
:param df_gw: Default gateway address for static network configuration. Required if mode is 'static'.
:type df_gw: str
:param dns_server: DNS server address for static network configuration. Required if mode is 'static'.
:type dns_server: str
:return: A dictionary indicating the mode of network configuration. Possible keys are 'mode' with values
    'DHCP', 'static', 'invalid ip', 'invalid class', 'invalid df_gw', or 'invalid dns_server'.
:rtype: dict

<a id="config_class.set_appname"></a>

#### set\_appname

```python
def set_appname(name)
```

Sets the application name by modifying the settings dictionary. The function updates the
application name in the settings and then writes the updated settings to persistent storage.
It also logs the action performed.

:param name: The desired name to set as the application name.
:return: A dictionary containing the updated application name.

<a id="config_class.restart_services"></a>

#### restart\_services

```python
def restart_services()
```

Restart system services using the systemctl command.

This function logs the action of restarting services, executes the system command to
restart the `gunicorn` service, and logs the completion of the operation.

<a id="config_class.set_analogue_settings"></a>

#### set\_analogue\_settings

```python
def set_analogue_settings(newsettings)
```

Updates the analogue settings by modifying specific configuration parameters. The function
ensures that the analogue prefix is distinct from the digital prefix, updates channel names,
enable/disable states based on the provided input, writes the changes to persistent storage,
logs the update information, and restarts relevant services to apply changes.

:param newsettings: A dictionary containing the new settings for the analogue configuration.
    It should include keys for channel names (e.g., 'ch1-name', 'ch2-name', etc.) and their
    enabled states (e.g., 'ch1-enabled', 'ch2-enabled', etc.), as well as an 'analogue_prefix'
    key for the new analogue prefix.
:type newsettings: dict
:return: None

<a id="config_class.set_digital_settings"></a>

#### set\_digital\_settings

```python
def set_digital_settings(newsettings)
```

Updates the digital settings configuration, including prefix, value, and command settings, as well as
individual channel configurations such as name, direction, exclusion, and enablement. After applying
the new settings, related services are restarted, and an informational log entry is created.

:param newsettings: A dictionary containing the updated digital settings and individual channel
    configurations. Expected keys are:
    - 'digital_prefix': New prefix for digital settings, compared against the analogue prefix.
    - 'digital_on_value': Value to be assigned when the digital channel is turned on.
    - 'digital_off_value': Value to be assigned when the digital channel is turned off.
    - 'digital_on_command': Command to execute when the digital channel is turned on.
    - 'digital_off_command': Command to execute when the digital channel is turned off.
    - 'chXX-name': Name of the digital channel (XX is the channel number, e.g., 'ch1-name').
    - 'chXX-direction': Direction of the digital channel (XX is the channel number).
    - 'chXX-excluded': Boolean indication of whether the channel is excluded (XX is the channel number).
    - 'chXX-enabled' (optional): If present, the channel is marked as enabled (XX is the channel number).

:return: None

