# Systembolaget
Custom home assistant component for systembolaget.

## Setup
To add this component to your home assistant configuration, just type the following in your configuration.yaml

`systembolaget:`

### Options

|Name            |Default       |Supported options                                 |Description                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`       |`null`        |String                                            |API key to access the api owned by Systembolaget. (https://api-portal.systembolaget.se/)
|`show_beer`     |`False`       |`True`\|`False`                                   |Show all new beers available in next release.
|`show_wine`     |`False`       |`True`\|`False`                                   |Show all new wine available in next release.
|`show_whisky`   |`False`       |`True`\|`False`                                   |Show all new whisky available in next release.

#### Example
  ```yaml
  systembolaget:
    api_key: !secret systembolaget
    show_beer: True
    show_wine: False
    show_whisky: True
  ```
