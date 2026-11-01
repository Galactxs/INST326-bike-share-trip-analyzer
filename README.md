# INST326-bike-share-trip-analyzer
Project for my OOP class. This project is a bike-share trip analyzer written in Python. It reads a text file of trip records (start station, start time, end station, end time) and prints a summary report.

Three main pieces:

RideTime: Parses a YYYY-MM-DD HH-MM string into a datetime and contains helpers like display() and canonical()

Trip: Holds one ride's stations and times, calculates duration in minutes, and decides if it is valid or not (greater than 0) and discribes itself through __str__

TripLog: Stores a list of trip objects and provides the analytics: total trips, average duration, valid trips starting at a given station, the longest valid trip, and two reports ( report_summary() and report_all_trips()). The load_from_file() method reads the data file line by line, skips blanks, and prints Invalid trip: for any line with an unparseable time. 
