from pathlib import Path
import csv
from railway import Station, RailNetwork

def read_rail_network(filepath:Path):
    """Imports rail network from a .csv file

    Args:
        filepath (Path): Path object to .csv file containing all the stations in the network.
        File must contain headers 
            name
            region
            crs
            latitude 
            longitude
            hub

    Raises:
        ValueError: Latitude and Longitude must be convertable to float values
        ValueError: Hub must be a boolean value

    Returns:
        railway.RailNetwork: RailNetwork object containing all imported data
    """    
    with open(filepath) as csv_file:
        csv_content = list(csv.reader(csv_file, delimiter=','))
    csv_headers = csv_content[0]
    csv_headers_index = {}
    csv_content = csv_content[1:]
    for i, header in enumerate(csv_headers): # we create a header dict object to locate 
        csv_headers_index[header] = i        # the index of each header, no matter the order
    
    station_list = []
    param_keys = ['name', 'region', 'crs', 'latitude', 'longitude', 'hub']

    for station_data in csv_content:
        params = {}
        for p_key in param_keys:
            params[p_key] = station_data[csv_headers_index[p_key]]
        try:
            params['latitude'] = float(params['latitude'])
            params['longitude'] = float(params['longitude'])
        except:
            raise ValueError(f'The values of latitude and/or longitude for {params["crs"]} must represent numbers which are convertable to float') 
        try:
            params['hub'] = bool(params['hub'])
        except:
            raise ValueError(f'The values of hub for {params["crs"]} must represent a bool')

        cur = Station(params['name'], params['region'], params['crs'], params['latitude'], params['longitude'], params['hub'])
        station_list.append(cur)

    return RailNetwork(station_list)
