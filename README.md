# Beerbolaget
Beerbolaget is a component which shows the latest beer available at Systembolaget in Sweden, also known as "Tillfälligt sortiment".
This component is a great match with the custom card for Home Assistant, [Beerbolaget-Card](https://github.com/Ceerbeerus/beerbolaget-card).

## What can beerbolaget do?
* Tell you if there is a new release of beer coming this week.
* Show the latest batch of beer available (or which will become available current week).
* Supply image information for available beer.
* Show availability of those beers at choosen local store.
* Display the beers rating using data from [untappd](http://untappd.com/)
* Display which beers you have previously checked in using [untappd](http://untappd.com/), and the rating you gave.

## Upcoming features
* Display the beers rating using data from [ratebeer](https://www.ratebeer.com/)
* Show availability of those beers at the webstore.

## Releases
### 0.4.0
* Untappd auth-flow integrated to get api token.
#### Breaking changes
* untappd_token option is now replaced with untappd_callback
  (This is the callback specified in the api key request to untappd. Required format [YOUR HA URL]/api/untappd)

## Setup
To add this component to your home assistant configuration, download the folder (beerbolaget) and place it under <config_dir>/custom_components, or install it through [HACS](https://github.com/custom-components/hacs).

Then type the following in your configuration.yaml

`beerbolaget:`

### Required/Options
`api_key` is required to use this component.

|Name            |Required/Option      |Default       |Supported options                                 |Description  |
| -------------- |---------------------| ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`api_key`           |`Required`       |`None`        |`String`                                          |API key to access the api owned by [systembolaget.se](https://api-portal.systembolaget.se/)
|`image_url`         |`Option`         |`None`        |`String`                                          |Source to use when collecting image data for available beer. (https://www.systembolaget.se/api/productsearch/search/sok-dryck)
|`store`             |`Option`         |`None`        |`String`                                          |[Local store](https://www.systembolaget.se/butiker-ombud/) to use when checking availability of beers.
|`untappd_client_id` |`Option`         |`None`        |`String`                                          |API client id to access the api owned by [untappd](http://untappd.com/)
|`untappd_secret`    |`Option`         |`None`        |`String`                                          |API client secret to access the api owned by [untappd](http://untappd.com/)
|`untappd_callback`  |`Option`         |`None`        |`String`                                          |The callback url submited to untappd requesting the api key. (Required format: [YOUR HA URL]/api/untappd)
|`cache_path`        |`Option`         |`None`        |`String`                                          |File to use for caching the Untappd token
#### Example
  ```yaml
  beerbolaget:
    api_key: !secret systembolaget
    image_url: "https://example.com/api"
    store: "Avenyn"
    untappd_client_id: !secret untappd_client
    untappd_secret: !secret untappd_secret
    untappd_callback: http://my_ha_url.com:8123/api/untappd
  ```
### Automation example
  ```yaml
  # Beerbolaget release notification
  - alias: Beerbolaget Release
    initial_state: on
    trigger:
      platform: state
      entity_id: sensor.beerbolaget
      from: 'False'
      to: 'True'
    action:
      service: notify.mobile_app_xxx_iphone
      data:
        title: "Beerbolaget"
        message: "Nya Små partier: {{ states.sensor.beerbolaget.attributes.release_date }}"
        data:
          push:
            badge: 0
  ```
