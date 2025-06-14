# Contents for: app_control

* [app\_control](#app_control)
  * [random](#app_control.random)
  * [json](#app_control.json)
  * [datetime](#app_control.datetime)
  * [VERSION](#app_control.VERSION)
  * [initialise](#app_control.initialise)
  * [generate\_api\_key](#app_control.generate_api_key)
  * [writesettings](#app_control.writesettings)
  * [readsettings](#app_control.readsettings)
  * [loadsettings](#app_control.loadsettings)
  * [settings](#app_control.settings)

<a id="app_control"></a>

# app\_control

Application Settings Management

This module handles the application's configuration settings, providing functionality
to read, write, and manage persistent application settings. It maintains centralized
control over configuration parameters used across the application.

Exports:
    settings: Dictionary containing application configuration parameters
    writesettings(): Function to persist settings changes to storage

Usage:
    from app_control import settings, writesettings

    # Read settings
    current_power = settings['power']

    # Modify and persist settings
    settings['power'] = new_value
    writesettings()

<a id="app_control.random"></a>

## random

<a id="app_control.json"></a>

## json

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Initializes and returns the default application settings.

This function creates and returns a dictionary that contains
the initial configuration for the Oxide Line Laser Controller.
The configurations include details related to logs, laser device
settings, and camera settings.

:return: A dictionary containing the application’s default settings.
:rtype: dict

<a id="app_control.generate_api_key"></a>

#### generate\_api\_key

```python
def generate_api_key(key_len)
```

generate a new api key of key_len characters

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Write settings to the json file

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Read the json file

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Replace the default values in the settings dict object with thsoe from the json files.
If the api-key is the default value then generate a new 128 character one.

<a id="app_control.settings"></a>

#### settings

