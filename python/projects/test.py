#We have list of tuples, 
#Each tuple represents a train start station and train end station.
#Please find stations that represents final stop.

#example for input of:
#lines = [('A','B'),('A','C'),('C','D')]

#the result is:
#B,D

# example1: [('E','A')]
# => A


def find_final_stops(lines):
    start_stations = {line[0] for line in lines}
    end_stations = {line[1] for line in lines}
    
    # Final stops are those that appear as an end station but not a start station
    final_stops = end_stations - start_stations
    return final_stops

# Test cases
lines1 = [('A', 'B'), ('A', 'C'), ('C', 'D')]
lines2 = [('E', 'A')]

print("Final stops:", find_final_stops(lines1))  # Output: {'B', 'D'}
print("Final stops:", find_final_stops(lines2))  # Output: {'A'}
