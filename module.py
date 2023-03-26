import requests
import pandas as pd


def get_derbyshire_place_ids():
    url = "https://opendomesday.org/api/1.0/county/dby"
    response = requests.get(url)
    data = response.json()

    place_ids = []
    for place in data['places_in_county']:
        place_ids.append(place['id'])

    return place_ids
    
    

def get_manor_ids(place_id):
    url = ("http://opendomesday.org/api/1.0/place/" + str(place_id))
    response = requests.get(url)
    data = response.json()

    manor_ids = []
    for manor in data['manors']:
        manor_ids.append(manor['id'])

    return manor_ids



def get_all_manors_in_derbyshire():
    all_manor_ids = []
    place_ids = get_derbyshire_place_ids()
    for place_id in place_ids:
        manor_ids = get_manor_ids(place_id)
        all_manor_ids.extend(manor_ids)
    return all_manor_ids
    
    
def get_manor_data(manor_id):
    url = ("https://opendomesday.org/api/1.0/manor/"+str(manor_id))
    response = requests.get(url)
    data = response.json()

    geld_paid = data['geld']
    total_ploughs = data['totalploughs']

    return geld_paid, total_ploughs
    

def create_derbyshire_dataframe():
    manor_ids = get_all_manors_in_derbyshire()
    data = []

    for manor_id in manor_ids:
        geld_paid, total_ploughs = get_manor_data(manor_id)
        data.append({"Manor ID": manor_id, "Geld Paid": geld_paid,"TotalPloughs":total_ploughs})

    df = pd.DataFrame(data)
    return df
    
    
    
df = create_derbyshire_dataframe()  

total_geld_paid = df["Geld Paid"].sum()
total_ploughs = df["Total Ploughs"].sum()

print("Total geld paid in Derbyshire: "+str(total_geld_paid))
print("Total ploughs owned in Derbyshire: "+str(total_ploughs))
	
	

