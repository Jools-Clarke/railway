import matplotlib.pyplot as plt
import numpy as np

def fare_price(distance: float, different_regions: bool, hubs_in_dest_region: int) -> float:
    """### Returns the fare price for a journey over a given distance - 
    based on the number of regions traversed and the demand for services at the destination region (estimated by regional hub density)"""

    fare_price = 1 + distance * np.exp(-distance/100) * (1 + (different_regions*hubs_in_dest_region)/10)

    return fare_price

class Station:
    """### Station object - 
    records details about a given station"""
    name: str
    region: str
    crs: str
    lat: float
    lon: float
    hub: bool

    def __init__(self, name:str, region:str, crs:str, lat:float, lon:float, hub:bool):
        self.name = name
        self.region = region
        self.hub = hub

        if len(crs) != 3: #validate the CRS code, otherwise raising errors
            raise ValueError(f"'{crs}' is not a valid CRS code, it must contain 3 characters")
        elif not crs.isupper():
            raise ValueError(f"'{crs}' is not a valid CRS code, it must contain only uppercase characters")
        elif not crs.isalpha():
            raise ValueError(f"'{crs}' is not a valid CRS code, it can not contain numeric characters")
        else:
            self.crs = crs

        if lat > 90 or lat < -90: #validate the latitude, otherwise raising errors
            raise ValueError(f"{lat} is not a valid latitude value, it must be between -90 and 90")
        else:
            self.lat = lat

        if lon > 180 or lon < -180: #validate the longitude, otherwise raising errors
            raise ValueError(f"{lon} is not a valid longitude value, it must be between -180 and 180")
        else:
            self.lon = lon

    def __str__(self) -> str:
        if self.hub:
            out = f'Station({self.crs}-{self.name}/{self.region}-hub)'
        else:
            out = f'Station({self.crs}-{self.name}/{self.region})'

        return out
    
    def __repr__(self) -> str:
        if self.hub:
            out = f'Station({self.crs}-{self.name}/{self.region}-hub)'
        else:
            out = f'Station({self.crs}-{self.name}/{self.region})'

        return out


    def distance_to(self, destination) -> float:
        phi_1 = self.lat
        phi_2 = destination.lat
        llambda_1 = self.lon
        llambda_2 = destination.lon
        R = 6371 #rad_earth in km

        sin_sq_phi = np.sin((phi_2-phi_1)/2)**2
        sin_sq_llambda = np.sin((llambda_2-llambda_1)/2)**2

        d = 2*R*np.arcsin(np.sqrt(sin_sq_phi+np.cos(phi_1)*np.cos(phi_2)*sin_sq_llambda))
        return d


class RailNetwork:
    """### Rail Network Object - 
    Contains informations about the stations within a rail network"""
    
    def __init__(self, input_stations:list):
        self.stations: dict = {}
        if len(input_stations) != len(set(input_stations)):
            raise ValueError(f"there are 1 or more duplicate CRS codes in input list, CRS codes are required to be unique")
        for station in input_stations:
            self.stations[station.crs] = station

    def regions(self):
        self.unique_regions = []
        for station in self.stations.values():
            if station.region not in self.unique_regions:
                self.unique_regions.append(station.region)
        return self.unique_regions # TODO I dont know what you want from me!!!

    def n_stations(self):
        return len(self.stations)

    def hub_stations(self, region=False) -> list:
        self.hub_list: list = []
        if not region:
            for station in self.stations.values():
                if station.hub:
                    self.hub_list.append(station)
        
        else:
            for station in self.stations.values():
                if station.hub and station.region == region:
                    self.hub_list.append(station)
        
        return self.hub_list


            

    def closest_hub(self, s):
        self.hub_list: list = [] # list of hubs
        self.d_list: list = [] # distance from hub to station
        try: 
            self._ = self.stations[s.crs]
        except:
            raise ValueError(f'station {s.crs} is not on this network')

        for station in self.stations.values():
            if station.hub and station.region == s.region:
                self.hub_list.append(station)
                self.d_list.append(station.distance_to(s))

        if len(self.hub_list) < 1:
            raise LookupError('No hubs exist in this region')
        return self.hub_list[np.argmin(self.d_list)]



    def journey_planner(self, start, dest):
        if start.region == dest.region:
            return [start, dest]
        else:
            self.journey_list: list = [start]

            self.start_hub = self.closest_hub(start)
            self.dest_hub = self.closest_hub(dest)

            if self.start_hub != start:
                self.journey_list.append(self.start_hub)
            if self.dest_hub != dest:
                self.journey_list.append(self.dest_hub)

            self.journey_list.append(dest)
            return self.journey_list
    

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return
