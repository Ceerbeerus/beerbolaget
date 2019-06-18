# Beerbolaget
Custom home assistant component for systembolaget.

## Setup
To add this component to your home assistant configuration, just type the following in your configuration.yaml

`beerbolaget:`

### Options

|Name            |Default       |Supported options                                 |Description                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`       |`None`        |`String`                                          |API key to access the api owned by systembolaget.se (https://api-portal.systembolaget.se/)
|`ratebeer`      |`None`        |`String`                                          |API key to access the api owned by ratebeer.com
|`untappd`       |`None`        |`String`                                          |API key to access the api owned by untappd.com
#### Example
  ```yaml
  systembolaget:
    api_key: !secret systembolaget
    ratebeer: !secret ratebeer
    untappd: !secret untappd
  ```
