# HustleFiti

<p align="center">
  <img src="./images/hustler.png" alt="Size Limit CLI" width="738">
</p>

An open API for an Online Marketplace for contract service providers HustleFiti is a visionary platform aimed at transforming the Local(Kenyan) GigEconomy for good. By building a user-friendly online marketplace connects skilled professionals offering services such as plumbing, electrical repair, photography, lawn mowing, hair styling and much more with discerning clients in search of reliable solutions. Through this platform, artisans can showcase their expertise, enabling clients to effortlessly browse, hire, and purchase services and products, all in one place. Clients can schedule appointments, make secure online payments, and have services delivered directly to their doorstep with just a few clicks.

## Vuejs Frontend Demo 
[HustleFiti_Vue(http://35.154.52.204/)]

## Live API Documentation
[HustleFiti_API(http://13.234.17.232/redoc)

## Test API with Swagger UI
[HustleFiti_API(http://13.234.17.232/docs)

## Read MORE on this Project
[HustleFiti Project Pitch(https://winter-mint-a1c.notion.site/HustleFiti-Portfolio-Project-eb5f491359cf4a35a5059129ab6d947e)]

## Installation Ubuntu 20 - 22
Clone this repository

### in the projects root directoy run this to setup Mariadb
```./setup/setup_mariadb.sh```

### or for mysql consider changing usernames ans passwords in setup as they are required as environment variables in running flask
```./setup/setup_mysql.sh```

### set up python and all python requirements 
```./setup/setup_python.sh```

### Open a brevo account to get brevo api key and initiate environmet variables as:
```export ENV_HUSTLE_API="*********************************************"  ENV_MYSQL_USER="*******" ENV_MYSQL_PWD="********" ENV_MYSQL_HOST="localhost" ENV_MYSQL_DB="hustle_db"

### to run fastapi  as localhost in developer mode use
```uvicorn main:app --reload```
