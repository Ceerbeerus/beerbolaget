# Beerbolaget
Custom home assistant component for systembolaget.

## Setup
To add this component to your home assistant configuration download the files and place it under <config_dir>/custom_components. Then type the following in your configuration.yaml

`beerbolaget:`

### Required/Options
`api_key` is required to use this component.

|Name            |Default       |Supported options                                 |Description                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`       |`None`        |`String`                                          |API key to access the api owned by systembolaget.se (https://api-portal.systembolaget.se/)
|`store`         |`None`        |`String`                                          |Local store to use when checking availability of beers. (https://www.systembolaget.se/butiker-ombud/)
|`ratebeer`      |`None`        |`String`                                          |API key to access the api owned by ratebeer.com
|`untappd`       |`None`        |`String`                                          |API key to access the api owned by untappd.com
#### Example
  ```yaml
  beerbolaget:
    api_key: !secret systembolaget
    store: Avenyn
    ratebeer: !secret ratebeer
    untappd: !secret untappd
  ```
