# Beerbolaget
Beerbolaget is a component which shows the latest beer available at Systembolaget in Sweden, also known as "Små partier".

## What can beerbolaget do?
* Show the latest batch of beer available (or which will become available current week).
* Supply image information for available beer.
* Show availability of those beers at choosen local store.

## Upcoming features
* Display the beers rating using data from [ratebeer](https://www.ratebeer.com/)
* Display the beers rating using data from [untappd](http://untappd.com/)
* Show availability of those beers at the webstore.

## Setup
To add this component to your home assistant configuration, download the folder (beerbolaget) and place it under <config_dir>/custom_components, or install it through [HACS](https://github.com/custom-components/hacs).

Then type the following in your configuration.yaml

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
