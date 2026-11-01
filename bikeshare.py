# Template for Project 2

# Add your name here
STUDENT_NAME = "Daniel Fitzgerald"


import argparse
import sys
from datetime import datetime

class RideTime:
    """Represent a timestamp for a bike-share trip.

    All times in this project must be written in the format YYYY-MM-DD HH:MM
    (24-hour clock). This class stores the original string and provides 
    helper methods for working with times.
    
    DO NOT change this class
    """
    # Time formatting
    FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self, time_str):
        """Construct a RideTime and store the original date-time string.
        
            Args:
                time_str (str): the date-time string in the format:
                                YYYY-MM-DD HH:MM
            
            Raises:
                ValueError: If time_str cannot be parsed into a datetime.
        """
        self.raw = time_str

        try:
            self._dt = datetime.strptime(time_str, self.FORMAT)
        except ValueError:
            try:
                dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                self._dt = dt.replace(second=0)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.raw}")

    @property
    def dt(self):
        """Return the internal datetime object."""
        return self._dt

    def minutes_since_midnight(self) -> int:
        """Return the number of minutes since midnight.

        Useful for computing trip durations in the following way:
            duration = time1.minutes_since_midnight() - time2.minutes_since_midnight()
        
        Returns:
            int: Number of whole minutes elapsed since midnight on the same
            calendar day as this time.
        """
        return self._dt.hour * 60 + self._dt.minute

    def canonical(self):
        """Return a tuple (year, month, day, hour, minute) all int."""
        return (self._dt.year, self._dt.month, self._dt.day,
                self._dt.hour, self._dt.minute)

    def display(self) -> str:
        """Return a display-friendly version of the time.

        Example: 2026-03-01@08:10
        """
        return self._dt.strftime("%Y-%m-%d@%H:%M")

    def __str__(self) -> str:
        """Return the time in the standard minute-level format."""
        return self._dt.strftime(self.FORMAT)



class Trip:
    def __init__(self, start_station, start_time:RideTime, end_station, end_time:RideTime ) -> None:
        """ Initializing trip

        Args:
            start_station (str): name of station the trip started at
            start_time (RideTime): when trip started
            end_station (str): name of station the trip ended at
            end_time (RideTime): when the trip ended

        """
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time


    def duration(self, start_time:RideTime, end_time:RideTime):
        """ Return the duration of a trip in whole minutes

        Args:
            start_time (RideTime): when the trip started
            end_time (RideTime): whne the trip ended
        Returns:
            int: minutes from start_time to end_time, negitive if end_time is before the start
        """

        change_time = end_time.dt - start_time.dt
        
        return int(change_time.total_seconds() // 60)
    

    def is_valid(self, start_time: RideTime, end_time: RideTime):
        """ Check if a trip is valid

        Args:
            start_time (RideTime): when the trip started
            end_time (RideTime): when the trip ended
        Returns:
            bool: True if duration is positive number, False if duration is negative
        """

        return self.duration(start_time, end_time) > 0


    def __str__(self):
        """ Return a summary of the trip in a readable format

        returns:
            str: 
                for valid trip: (duration) minute trip from (start_station) at (start) to (end_station) at (end)
                for invalid trip: Invalid trip from (start_station) at (start) to (end_station) at (end)
        """

        start = self.start_time.display()
        end = self.end_time.display()

        if self.is_valid(self.start_time, self.end_time):
            return (f"{self.duration(self.start_time, self.end_time)}- minute trip from {self.start_station} at {start} to {self.end_station} at {end}")
        else:
            return (f"Invalid trip from {self.start_station} at {start} to {self.end_station} at {end}")



class TripLog:

    def __init__(self) -> None:
        """ construct empty TripLog"""

        self.trips = []

    def add_trip(self, trip):
        """ Add trips to the log

        Args:
            trip (Trip): the trip to add
        """

        self.trips.append(trip)

    def total_trips(self):
        """ Returns the total number of trips loged

        Returns:
            int: counts all the trips, both valid and invalid 
        """

        return len(self.trips)


    def _is_valid_trips(self): # helper function to save time checking if trip is valid
        """ Returns only valid trips, in the order they were added

            Helper function used by other methods so the valitity check is in one place
        
        Returns:
            List[Trips]: trips whose duration is positive 
        """

        valid = []

        for t in self.trips:
            if t.is_valid(t.start_time, t.end_time):
                valid.append(t)

        return valid

        
    def average_duration(self):
        """ return the mean duration of the valid trips

        Returns:
            int: the mean duration in minutes rounded, 0 if no valid trips
        """

        valid = self._is_valid_trips()

        if not valid:
            return 0

        toltal = 0
        for t in valid:
            toltal += t.duration(t.start_time, t.end_time)

        return round(toltal / len(valid))

        

    def start_station_trips(self, station_name):
        """ Return the valid trips that start at a givin station

        Args:
            station_name (str): starting station name to match
        Returns:
            list[Trip]: matching valid trips in order, empty if no matches
        """

        result = []
        for t in self._is_valid_trips():
            if t.start_station == station_name:
                result.append(t)
        
        return result

    def longest_trip(self):
        """ Return valid trip with longest duration

        Returns:
            Trip: the longest valid trip, or None if there are no valid trips
        """

        longest = None
        longest_duration = 0

        for t in self._is_valid_trips():

            d = t.duration(t.start_time, t.end_time)

            if longest is None or d > longest_duration: # if two trips have same duration trip two doesn't replace trip one as 'best'
                longest = t
                longest_duration = d

        return longest

    def load_from_file(self, path):
        """ Read trips from file and add them to log

        Args:
            path (str): path to trip data file
        """

        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue 

                start_station, start_str, end_station, end_str = (field.strip() for field in line.split(","))

                try:
                    trip = Trip(start_station, RideTime(start_str), end_station, RideTime(end_str))
                    self.add_trip(trip)

                except ValueError:
                    print(f"Invalid trip: {line}")

    def report_summary(self):
        """ Return a clear summary report of the log

        Returns:
            str: a formated multi-line report
        """
        toltal = self.total_trips()
        valid = len(self._is_valid_trips())
        longest = self.longest_trip()

        if longest is None:
            start_information = None
            end_information = None
        else:
            start_information = (longest.start_station, longest.start_time.canonical())
            end_information = (longest.end_station, longest.end_time.canonical())

        lines = [
            "TRIP SUMMARY",
            "------------",
            f"total: {toltal}",
            f"valid: {valid}",
            f"invalid: {toltal - valid}",
            f"average-duration: {self.average_duration()} minutes",
            f"longest-trip-start: {start_information}",
            f"longest-trip-end: {end_information}",
        ]
        return "\n".join(lines)

                

    def report_all_trips(self):
        """ Report one line per trip, in the order the trips were added
            each line is the __str__() output

        Returns:
            str: the report
        """

        lines = []
        for t in self.trips:
            lines.append(str(t))

        return "\n".join(lines)
                    



def parse_args():
    """Parses one filepath argument when __name__ == "__main__" """
    parser = argparse.ArgumentParser(description="A bike-share script.")
    parser.add_argument('filepath', help="Input file path")
    return parser.parse_args()

            
def main(filepath):
    """ Load the trip file and print a summary report

    Args:
        filepath (str): path to the file data
    """
    
    log = TripLog()
    log.load_from_file(filepath)
    print(log.report_summary())
    

if __name__ == '__main__':
    args = parse_args()
    print(args)
    main(args.filepath)



