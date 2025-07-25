import googlemaps
import pandas as pd

# replace this with your actual api key
api_key = 'YOUR_API_KEY'

# initialize googlemaps instance
gmaps = googlemaps.Client(key=api_key)

# lat/long pairs for origins
origins = [(35.9119, -79.057),
           (35.8119, -79.157), 
           (35.7119, -79.257)]

# lat/long pairs for destinations
destinations = [(35.9044, -79.04907),
                (35.9544, -79.09907)]

# make the api query
result = gmaps.distance_matrix(origins=origins,
                                destinations=destinations)

# extract origin addresses
origin_addresses = result['origin_addresses']
# extract destination addresses
destination_addresses = result['destination_addresses']

# counters for looping through results list
origin_counter = 0
dest_counter = 0

# set up output DataFrame
results_columns = ['origin', 'destination', 'originLat', 'originLong', 'destLat', 'destLong', 'distance (m)', 'travel time (s)']
results_df = pd.DataFrame(columns = results_columns)

# outer loop for origin locations
for origin_latLong, origin_add in zip(origins, origin_addresses):
  dest_counter = 0
  # inner loop for destination locations
  for dest_latLong, dest_add in zip(destinations, destination_addresses):
    pair_index = dest_counter + origin_counter * len(destinations)
    # get results from this specific origin/destination pairs
    result_elements = result['rows'][origin_counter]['elements'][dest_counter]
    # extract distance values in meters
    dist_value = result_elements['distance']['value']
    # extract time values in seconds
    time_value = result_elements['duration']['value']
    
    # write output data to DataFrame
    results_df.loc[pair_index, 'origin'] = origin_add
    results_df.loc[pair_index, 'destination'] = dest_add
    results_df.loc[pair_index, 'originLat'] = origin_latLong[1]
    results_df.loc[pair_index, 'originLong'] = origin_latLong[0]
    results_df.loc[pair_index, 'destLat'] = dest_latLong[1]
    results_df.loc[pair_index, 'destLong'] = dest_latLong[0]
    results_df.loc[pair_index, 'distance (m)'] = dist_value
    results_df.loc[pair_index, 'travel time (s)'] = time_value
    
    # step counters
    dest_counter += 1
  origin_counter += 1
  
# write output file
results_df.to_csv('travel_time_calcs.csv')
