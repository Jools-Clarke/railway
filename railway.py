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

    def __str__(self):
        if self.hub:
            out = f'Station({self.crs}-{self.name}/{self.region}-hub)'
        else:
            out = f'Station({self.crs}-{self.name}/{self.region})'

        return out

        
    
    def distance_to(self) -> float:
        raise NotImplementedError


class RailNetwork:
    """### Rail Network Object - 
    Contains informations about the stations within a rail network"""
    stations: dict = {}

    def __init__(self, stations:list):
        if len(stations) != len(set(stations)):
            raise ValueError(f"there are 1 or more duplicate CRS codes in input list, CRS codes are required to be unique")
        for station in stations:
            self.stations[station.crs] = station

    def regions(self):
        unique_regions = []
        for station in self.stations.values():
            if station.region not in unique_regions:
                unique_regions.append(station.region)
        self.regions = unique_regions # TODO I dont know what you want from me!!!

    def n_stations(self):
        raise NotImplementedError

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

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
