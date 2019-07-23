# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
import json
from collections import namedtuple
import unicodedata
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import time
import re

import psycopg2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3831.602 Safari/537.36',
    'Cookie': 'datr=HpntWUrc0QawJrdvP6Ynw7kN; sb=W5ntWROUmZlYjysKseKep_91; pl=n; dpr=1.5; c_user=100009855792024; xs=35%3AUXgh6AceOVeGvw%3A2%3A1508743515%3A20772%3A8699; fr=09kK2tX9Vuz0OSrn7.AWUcfLFMyKAy2sEScE_co9LLnUk.BZ7Zke.Q_.FpM.0.0.BaU5YP.AWUFt5Ae; wd=1280x561; act=1515430580572%2F1; presence=EDvF3EtimeF1515430601EuserFA21B09855792024A2EstateFDutF1515430601519CEchFDp_5f1B09855792024F15CC'
}


def index(request):
    # res = apiCall(request)
    setupDB()
    return HttpResponse('complete')


def setupDB(db, mode):
    conn = None
    if mode == 1:
        inSQL = "INSERT INTO Location (locationID,address,longitude,latitude)VALUES('" + db.locationID + "','" + db.address + "','" + db.long + "','" + db.lat + "');"
    elif mode == 2:
        inSQL = "INSERT INTO Cuisine (cuisineType,restaurantID)VALUES('" + db.cuisineType + "','" + db.restaurantID + "');"
    elif mode == 3:
        inSQL = "INSERT INTO Photo (pictureURL,restaurantID)VALUES('" + db.pictureURL + "','" + db.restaurantID + "');"
    elif mode == 4:
        inSQL = "INSERT INTO Restaurant (restaurantID,priceRange,website,phoneNumber,locationID)VALUES('" + db.restaurantID + "','" + db.priceRange + "','" + db.website + "','" + db.phoneNumber + "','" + db.locationID + "');"
    elif mode == 5:
        inSQL = "INSERT INTO RestaurantFeature (featureName,restaurantID,description)VALUES('" + db.featureName + "','" + db.restaurantID + "','" + db.description + "');"
    elif mode == 6:
        inSQL = "INSERT INTO RestaurantRating (scale,restaurantID,overallRating,source)VALUES('" + db.scale + "','" + db.restaurantID + "','" + db.overallRating + "','" + db.source + "');"
    elif mode == 7:
        inSQL = "INSERT INTO UserReview (comment,restaurantID,reviewRating,reviewDate)VALUES('" + db.comment + "','" + db.restaurantID + "','" + db.reviewRating + "','" + db.reviewDate + "');"
    # createSql = "CREATE TABLE Restaurant ( ResID int, Address varchar(255), Coordinate varchar(255), Price varchar(255), City varchar(255) );"
    # insertSql = "INSERT INTO Location (address,longitude,latitude)VALUES('test','10.2','10.1');"
    selectSql = "select * from Location"
    try:
        # inSQL = "INSERT INTO Location (locationID,address,longitude,latitude)VALUES('test','test','10.2','10.1');"
        conn = psycopg2.connect("dbname='aim1' user='admin' host='localhost' password='1234'")
        print('PostgreSQL database version:')
        cur = conn.cursor()
        #  cur.execute(sql)
        cur.execute(inSQL)
        conn.commit()
        '''
        cur.execute(selectSql)
        print(cur.rowcount)
        row = cur.fetchone()
        while row is not None:
         print(row)
         row = cur.fetchone()
        '''
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    #   time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    website = soup.select('span.biz-website.js-add-url-tagging > a')[0].get_text()
    phone = soup.select('span.biz-phone')[0].get_text().strip()
    feature = 0
    feature_a = soup.select('div.short-def-list')[0].get_text()
    # print(feature_a)
    import re
    feature = re.sub(r"\s{2,}", " ", feature_a)
    # print(feature)
    featureName = soup.select('div.short-def-list > dl > dt')
    featureDescription = soup.select('div.short-def-list > dl > dd')
    feature = []
    for featureName, featureDescription in zip(featureName, featureDescription):
        # info = {
        #     'featureName'    :featureName.get_text(),
        #     'featureDescription'   :featureDescription.get_text()
        #     }
        feature.append(re.sub(r"\s{2,}", " ", featureName.get_text()).strip() + ':' + re.sub(r"\s{2,}", " ",
                                                                                             featureDescription.get_text()).strip())
    print("Website restuarant : " + website)
    print("Retuarant phonenumber : " + phone)
    print("All feature of restuarant : ".join(feature))


def apiCall(request):
    checkerYelp = True
    checkerGoo = True
    offset = 0
    responseData = []
    while (checkerYelp):
        ### call yelp api
        resp = requests.get(
            'https://api.yelp.com/v3/businesses/search?term=restaurant&location=berlin&limit=2&offset=' + str(offset),
            headers={
                'Authorization': 'Bearer sfNwLics9lPqpWB7916BaiwHJTYVw7a2jlWbcxbwJuvdmvCB4flz1Hv0tPL3tZQpgl88DoGytEUEJCRrtChhSAU7rZ5KBOlidyyVY24TzREO_yc0IiX3iLWpnAw5WnYx'}, )
        offset = offset + 1
        if (offset == 1):
            checkerYelp = False
        if resp.status_code != 200:
            checkerYelp = False
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        data = resp.text
        x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        ### get review for each place
        for i in xrange(1, len(x.businesses)):
            locationId = x.businesses[i].id
            yelpUrl = x.businesses[i].url
            print("Price : " + x.businesses[i].price)
            print("Location : ")
            print(x.businesses[i].location)
            get_info(yelpUrl)
            db = {}
            db["restaurantID"] = x.businesses[0].id
            db["priceRange"] = x.businesses[0].price
            db["website"]
            # print(locationId)
            '''
            respR = requests.get('https://api.yelp.com/v3/businesses/' + locationId + '/reviews',
                                 headers={
                                     'Authorization': 'Bearer sfNwLics9lPqpWB7916BaiwHJTYVw7a2jlWbcxbwJuvdmvCB4flz1Hv0tPL3tZQpgl88DoGytEUEJCRrtChhSAU7rZ5KBOlidyyVY24TzREO_yc0IiX3iLWpnAw5WnYx'}, )
            if respR.status_code != 200:
                raise ApiError('GET /tasks/ {}'.format(respR.status_code))
            dataR = respR.text
            r = json.loads(dataR, object_hook=lambda d: namedtuple('R', d.keys())(*d.values()))
            # print(r)
            for p in xrange(1, len(r.reviews)):
                print("Review from yelp : " + r.reviews[p].text)
                print("Author (yelp) : " + r.reviews[p].user.name)
            lat = x.businesses[i].coordinates.latitude
            # print(lat)
            long = x.businesses[i].coordinates.longitude
            # print(long)
            ### check that place exist in google map or not by given lat long
            respG = requests.get(
                'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(lat) + ',' + str(
                    long) + '&radius=5&type=restaurant&key=AIzaSyB_pmY_DHLOEzAeyq6YeVNk1XEugx-5ZfM', )
            if respG.status_code != 200:
                raise ApiError('GET /tasks/ {}'.format(respG.status_code))
            data2 = respG.text
            y = json.loads(data2, object_hook=lambda d: namedtuple('Y', d.keys())(*d.values()))
            #### Get google review
            if len(y.results) > 0:
                placeId = y.results[0].place_id
                # print(placeId)
                respGDetail = requests.get(
                    'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + placeId + '&key=AIzaSyB_pmY_DHLOEzAeyq6YeVNk1XEugx-5ZfM', )
                if respGDetail.status_code != 200:
                    raise ApiError('GET /tasks/ {}'.format(respGDetail.status_code))
                data3 = respGDetail.text
                z = json.loads(data3, object_hook=lambda d: namedtuple('Z', d.keys())(*d.values()))
                # print(z.result.reviews)
                for k in xrange(1, len(z.result.reviews)):
                    print(" ")
                    print("Review from Google : " + z.result.reviews[k].text)
                    print("Author (Google) : " + z.result.reviews[k].author_name)
          '''
    return HttpResponse('complete')



