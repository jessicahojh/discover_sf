# Discover San Francisco

Discover San Francisco is a full stack web application that allows users to learn more about the city. Users can learn about the various neighborhoods and discover “things to do.” The Yelp API is used to display the top 5 most popular restaurants in each neighborhood and the Google Maps API is used to mark the location of each tourist attraction. Users can even contribute their thoughts by creating an account to comment and rate. 

## Table of Contents
* [Overview](#overview)<br/>
* [Tech Stack](#techstack)<br/>
* [Setup/Installation](#installation)<br/>
* [Demo](#demo)<br/>
* [Future Features](#features)

<a name="overview"/></a>
## Overview

Once a user lands on the homepage, he or she can click the "Let's Explore" button to view the list of neighborhoods in San Francisco. The neighborhoods and their data is stored in a PostgreSQL database. A map image marking the specific location of a popular tourist attraction is shown when the user lands on the "specific place" page. The map with the marker is populated using the Google Maps API. This API is called with an AJAX request inserting the location's latitude and longitude. Users can also view the top 5 most popular restaurants for each neighborhood. This list is populated when a request is made to the Yelp API to get a JSON response with the specific parameters. Logged in users can contribute their thoughts by leaving a comment. Their comments are stored in a PostgreSQL database and displayed on the webpage when the user clicks "submit." The submit button has an event listener so that an AJAX request can be made to get the JSONIFY-ed data.

<a name="techstack"/></a>
## Tech Stack
**Frontend:** Javascript, AJAX, JSON, jQuery, Jinja, HTML, CSS, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>
**APIs:** Google, Yelp<br/>

<a name="installation"/></a>
## Setup/Installation
Get Client ID and Key from [Yelp](https://www.yelp.com/fusion) and save them to a file `secrets.sh`:
```
export yelp_client_id="YOUR_CLIENT_ID"
export yelp_api_key="YOUR_KEY"
```
Get Key from [Google Maps](https://cloud.google.com/maps-platform/?apis=maps) and save them to the same file `secrets.sh`:
```
export google_api_key="YOUR_KEY"
```
On local machine, go to directory where you want to work and clone Discover San Francisco repository:
```
$ git clone https://github.com/jessicahojh/San_Francisco_Webpage_Project.git
```
Create a virtual environment in the directory:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database:
```
$ createdb sanfrancisco
```
Seed data into the database tables:
```
$ python3 seed.py
```
Create .gitignore file:
```
$ touch .gitignore
```
Access .gitignore file in terminal to ignore secrets.sh file:
```
$ nano .gitignore
```
Store secrets.sh file in .gitignore file:
```
secrets.sh
```
Activate secrets.sh:
```
$ source secrets.sh
```
Run the app:
```
$ python3 server.py
```
Open localhost:5000 on browser.

<a name="demo"/></a>
## Demo
**Homepage:**
<br/><br/>
![Homepage](/static/README/homepage.png)
<br/>

**List of Neighborhoods:**
<br/><br/>
![Neighborhoods](/static/README/neighborhoods.gif)
<br/>

**View a specific neighborhood:**
<br/><br/>
![View specific neighborhood](/static/README/specific_neighborhood.png)
<br/>

**View a specific neighborhood's list of "things-to-do/see":**
<br/><br/>
![View list of "things-to-do/see"](/static/README/list_places.gif)
<br/>

**Specific place ("things-to-see") in a specific neighborhood:**
<br/><br/>
![View a specific place in a neighborhood](/static/README/specific_place.gif)
<br/>


**Top 5 Most Popular Restaurants for a specific neighborhood:**
<br/><br/>
![Top 5 Restaurants](/static/README/restaurants.gif)
<br/> 

<a name="features"/></a>
## Future Features
* Using various APIs such as Zillow, weather, and Eventbright to provide housing, weather, and event info 
* Marketplace for users to buy/sell or exchange services
* Page for residents of specific neighborhoods to communicate with each other
