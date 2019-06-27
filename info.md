# Beerbolaget
Beerbolaget is a component for fetching information about the latest available beer at the swedish Systembolaget,
also known as "Små partier".

## Setup
Type the following in your configuration.yaml

`beerbolaget:`

### Required/Options
`api_key` is required to use this component.

|Name            |Default       |Supported options                                 |Description                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`       |`None`        |`String`                                          |API key to access the api owned by systembolaget.se (https://api-portal.systembolaget.se/)
|`image_url`     |`None`        |`String`                                          |Source to use when collecting image data for available beer.
|`store`         |`None`        |`String`                                          |Local store to use when checking availability of beers. (https://www.systembolaget.se/butiker-ombud/)
|`ratebeer`      |`None`        |`String`                                          |API key to access the api owned by ratebeer.com
|`untappd`       |`None`        |`String`                                          |API key to access the api owned by untappd.com
#### Example
  ```yaml
  beerbolaget:
    api_key: !secret systembolaget
    image_url: https://example.com/api
    store: Avenyn
    ratebeer: !secret ratebeer
    untappd: !secret untappd
  ```
