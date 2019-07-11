## What can beerbolaget do?
* Tell you if there is a new release of beer coming this week.
* Show the latest batch of beer available (or which will become available current week).
* Supply image information for available beer.
* Show availability of those beers at choosen local store.
* Display the beers rating using data from [untappd](http://untappd.com/)

## Upcoming features
* Display the beers rating using data from [ratebeer](https://www.ratebeer.com/)
* Show availability of those beers at the webstore.

## Setup
Type the following in your configuration.yaml

`beerbolaget:`

### Required/Options
`api_key` is required to use this component.

|Name            |Default       |Supported options                                 |Description                                                                                                                                                                                                                                                                                                                                    |
| --------------     | ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`           |`None`        |`String`                                          |API key to access the api owned by systembolaget.se (https://api-portal.systembolaget.se/)
|`image_url`         |`None`        |`String`                                          |Source to use when collecting image data for available beer. (https://www.systembolaget.se/api/productsearch/search/sok-dryck)
|`store`             |`None`        |`String`                                          |Local store to use when checking availability of beers. (https://www.systembolaget.se/butiker-ombud/)
|`ratebeer`          |`None`        |`String`                                          |API key to access the api owned by ratebeer.com
|`untappd_client_id` |`None`        |`String`                                          |API client id to access the api owned by untappd.com
|`untappd_secret`    |`None`        |`String`                                          |API client secret to access the api owned by untappd.com
#### Example
  ```yaml
  beerbolaget:
    api_key: !secret systembolaget
    image_url: "https://example.com/api"
    store: "Avenyn"
    untappd_client_id: !secret untappd_client
    untappd_secret: !secret untappd_secret
  ```
