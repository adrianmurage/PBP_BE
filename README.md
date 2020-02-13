[![time tracker](https://wakatime.com/badge/github/MainaMurage/PBP_BE.svg)](https://wakatime.com/badge/github/MainaMurage/PBP_BE)
## PBP BE(Backend)
RESTful API for the [PBP webapp](https://github.com/MainaMurage/PBP-FE). 

Built using [Flask](https://flask.palletsprojects.com/en/1.1.x/)

### API Resources
> all end points for the api start with **/api**

Implements JSON Web Tokens(JWT) for authentication.

The JWTs expire after 15 minutes and can be refreshed via:

| Resource        | method | endpoint  |
| --------------- | ------ | --------- |
| JWT refresh     | POST   | /token/refresh |
###### resource tables key:
ru
 : regular user
 
ve
: vendor

#### [User Resources](#user-resources)
The app has two types of users:
- Regular users
- Vendors

| JWT protected | Resource        | method | endpoint  | end goal |
| ------------- | --------------- | ------ | --------- | -------- |
| No            | ru registration | POST   | /register | create a ru |
| No            | ru login        | POST   | /login    | login a ru, generate & return access token and refresh token |
| Yes           | ru profile      | GET    | /user/profile | cr ru profile information |
| No            | ve registration | POST   | /vendor/register | create a ve |
| No            | ve login        | POST   | /vendor/login | login a ve |
| Yes           | ve shop         | POST   | /vendor/shop | create a vendor's shop |

#### Marketplace Resources
These comprise of everything that doesn't fall under [User Resources](#user-resources)

ie.
- items
- orders
- order map

| JWT protected | Resource        | method | endpoint  | end goal |
| ------------- | --------------- | ------ | --------- | -------- |
| No            | item            | GET    | /item     | get all items |
| Yes           | item            | POST   | /item     | ve create a new item |
| Yes           | orders          | GET    | /order    | return all orders made by a re |
| Yes           | orders          | POST   | /order    | ru create a new order or add item to an existing order |
| Yes           | order map       | GET    | /order/map | return coordinates(lat, lng) for all ve a ru has ordered from |
