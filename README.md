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

### Perquisites:
- python3
- python-pip
- virtualenv
- flask

### Local Setup
1. Clone the repository
```
https://github.com/MainaMurage/PBP_BE.git
```
2. Using virtualenv set up a virtual environment
```
virtualenv <environment name>
```
3. Activate the virtual environment
```
source <path to env name>/bin/activate (in bash)
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the dev server
```
python3 app.py 
```

### Contribution

 If you want to contribute to this project:
- Fork it!
- Create your feature branch: git checkout -b my-new-feature
- Commit your changes: git commit -am 'Add some feature'
- Push to the branch: git push origin my-new-feature
- Submit a pull request
