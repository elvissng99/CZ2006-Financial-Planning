import requests #pip install requests
import smtplib
from .models import *

# API key
api_key = "AIzaSyBQAyuGhTFC-cfUcJxTyNaNPZLHI_3l8wI"

class TripMgr:
    def __init__(self):
        self.trips = []
        self.tripObj = []

    @staticmethod
    def calcDistance(source, destination):
        source += " Singapore"
        destination += " Singapore"

        #Base url
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

        #get response
        r = requests.get(url + "origins=" + source + "&destinations=" + destination + "&key=" + api_key)
        distance = r.json()['rows'][0]['elements'][0]['distance']['value']
        return distance

    def addTrip(self, source, destination, frequency):      #Append trip into array
        newTrip = {"source": source, "destination": destination, "frequency": frequency}
        distance = self.calcDistance(source, destination)
        newTrip["distance"] = distance
        self.trips.append(newTrip)
        return distance

    def deleteTrip(self, index):        #Delete trip from array
        try:
            del self.trips[index]
            del self.tripObj[index]
        except IndexError:
            print("Index out of bounds")

    def addTripDB(self):        #Add individual trip to the database
        for trip in self.trips:
            newTrip = Trip.objects.get_or_create(source=trip["source"], destination=trip["destination"],
                                                frequency=int(trip["frequency"]), distance=float(trip["distance"]))
            self.tripObj.append(newTrip[0])

    def addUserTripDB(self, user):      #Use this to save/update user's trips to database
        if Trips.objects.filter(User=user).exists():
            trips = Trips.objects.get(User = user)
            trips.trip.set(self.tripObj, clear=True)
            trips.mileage = self.getTotalMileage()
            trips.save()
        else:
            newUserTrips = Trips(User=user, mileage=self.getTotalMileage())
            newUserTrips.save()
            for i in self.tripObj:
                newUserTrips.trip.add(i)
            newUserTrips.save()


    def getUserTripDB(self, user):        #Get exisiting trips belonging to user
        if Trips.objects.filter(User = user).exists():
            trips = Trips.objects.get(User = user)
            self.trips = []
            self.tripObj = []

            # Overwrite trips and tripObj
            for i in trips.trip.values_list('id', flat=True):
                t = Trip.objects.get(id=i)
                source = t.source
                destination = t.destination
                distance = t.distance
                frequency = t.frequency
                self.tripObj.append(t)
                self.trips.append({"source":source, "destination":destination, "distance": distance, "frequency": frequency})
            return self.trips
        else:
            return None

    def getTotalMileage(self):
        totalMileage = 0
        for i in self.trips:
            totalMileage += float(i["distance"]) * float(i["frequency"])
        return totalMileage
