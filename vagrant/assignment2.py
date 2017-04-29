import httplib2
import json
import sys
import codecs

def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    google_api_key = "AIzaSyAox4Mjj81wNdY-RQuYB496vJ8j0ilu80o"
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)



sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "A5SLLJZFCW5YJH1OFDSJ2ANDKBGFQIJZGENOEZTMITSY5LJS"
foursquare_client_secret = "AAT153KQCIEG3CHYX5JLVMCZ5UBQH4FCVA0LXSVKAYJFBNFI"


def findARestaurant(mealType,location):
	latitude, longitude = getGeocodeLocation(location)

	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v20130815&ll=%s,%s&query=%s,browse'% (foursquare_client_id, foursquare_client_secret,  latitude,longitude,mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id']
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['fomattedAddress']
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % (venue_id,foursquare_client_id,foursquare_client_secret))
		result = json.loads(h.request(url,'GET')[1])
		if result['response']['photos']['items']:
			first_pic = result['response']['photos']['items'][0];
			prefix = first_pic['prefix']
			suffix = first_pic['suffix']
			image_url = prefix+"300x300"+suffix

		else:
			image_url = 'http://www.koekjeswereld.nl/wp-content/uploads/2015/04/OTooles-burger-300x300.jpg'

		info = {'name':restaurant_name, 'address':restaurant_address, 'image':image_url} 

		print "Name %s" %info['name']
		print "Adress %s" %info['address']
		print "url for image %s" %info['image']

		return info
	else:
		return "mo results found"
		






	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

	#3. Grab the first restaurant
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url	
if __name__ == '__main__':
	# findARestaurant("Pizza", "Tokyo Japan")
	# findARestaurant("Tacos", "Jakarta, Indonesia")
	# findARestaurant("Tapas", "Maputo, Mozambique")
	# findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	# findARestaurant("Cappuccino", "Geneva, Switzerland")
	# findARestaurant("Sushi", "Los Angeles, California")
	# findARestaurant("Steak", "La Paz, Bolivia")
	# findARestaurant("Gyros", "Sydney Australia")
