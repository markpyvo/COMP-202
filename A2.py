# Program Description:
# This program simulates vessel navigation with waypoints, movement, wave impacts, and a storm countdown. 
# It uses functions for coordinate validation, distance calculation, and updating the vessel's position.

# 2. Write your program here:
import random
import math

#Global variables
MIN_LAT = -90 
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180
EARTH_RADIUS = 6378
STORM_STEPS = 5

def degrees_to_radians(degrees: float):
    '''
    Convert an angle in degrees to radians, rounded to 2 decimals.

    Parameters:
        degrees (float): Angle in degrees.

    Returns:
        float: Angle in radians, rounded to 2 decimals.

    Examples:
        >>> degrees_to_radians(180)
        3.14
        >>> degrees_to_radians(1)
        0.02
        >>> degrees_to_radians(90)
        1.57
    '''

    radians = degrees * math.pi/180
    return round(radians, 2)

def get_valid_coordinate(val_name: str, min_float: float, max_float: float):
    '''
    Ask the user for a coordinate until a valid number 
    within (min_float, max_float) is entered.

    Parameters:
        val_name (str): Name of the coordinate ("latitude" or "longitude").
        min_float (float): Minimum valid value (exclusive).
        max_float (float): Maximum valid value (exclusive).

    Returns:
        float: A valid float coordinate within the specified interval.

    Examples:
        >>> get_valid_coordinate('latitude', -90, 90)
        What is your latitude?-100
        Invalid latitude
        What is your latitude?-87.6
        -87.6
        >>> get_valid_coordinate('longitude', -180, 180)
        What is your longitude?-200
        Invalid longitude
        What is your longitude?34.0
        34.0
        >>> get_valid_coordinate('y-coordinate', -10, 10)
        What is your y-coordinate?5.0
        5.0
    '''

    value = min_float - 1

    while not min_float < value < max_float:
        value = float(input("What is your " + val_name + " ?"))
        
        if not min_float < value < max_float:
            print("Invalid", val_name)

    return value

def get_gps_location():
    '''
    Get the vessel's GPS coordinates by prompting the user for a latitude
    float within (MIN_LAT, MAX_LAT) and 
    a longitude float between (MIN_LONG, MAX_LONG).

    Returns:
        tuple: (latitude, longitude) as floats.

    Examples:
        >>> get_gps_location()
        What is your latitude?45.5
        What is your longitude?-73.5
        (45.5, -73.5)
        >>> get_gps_location()
        What is your latitude?-220
        Invalid latitude
        What is your latitude?-60
        What is your longitude?90
        (-60.0, 90.0)
        >>> get_gps_location()
        What is your latitude?55.4
        What is your longitude?-200
        Invalid Longitude
        What is your longitude?60.5
        (55.4, 60.5)
    '''

    gps_lat = get_valid_coordinate('latitude', MIN_LAT, MAX_LAT)
    gps_long = get_valid_coordinate('longitude', MIN_LONG, MAX_LONG)
    return(gps_lat, gps_long)

def distance_two_points(lat_1: float, long_1: float,\
 lat_2: float, long_2: float):
    '''
    Compute the great-circle distance between two points 
    using the Haversine formula.

    Parameters:
        lat_1 (float): Latitude of point 1 in degrees.
        long_1 (float): Longitude of point 1 in degrees.
        lat_2 (float): Latitude of point 2 in degrees.
        long_2 (float): Longitude of point 2 in degrees.

    Returns:
        float: Distance between the points in kilometers, 
        rounded to 2 decimals.

    Examples:
        >>> distance_two_points(45.508888, -73.561668, 19.432608, -99.133209)
        3723.31
        >>> distance_two_points(0, 0, 0, 0)
        0.0
        >>> distance_two_points(10, 20, -10, -20)
        3315.14
    '''

    lat_1 = degrees_to_radians(lat_1)
    long_1 = degrees_to_radians(long_1)
    lat_2 = degrees_to_radians(lat_2)
    long_2 = degrees_to_radians(long_2)
    
    a = ((math.sin((lat_2 - lat_1) / 2)) ** 2) \
    + math.cos(lat_1) * math.cos(lat_2) * \
    ((math.sin((long_2 - long_1) / 2)) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_RADIUS * c
    return round(d, 2)

def apply_wave_impact(position: float, min_float: float, max_float: float):
    '''
    Apply a random wave impact to a coordinate, 
    keeping it within (min_float, max_float).

    Parameters:
        position (float): Original position (latitude or longitude).
        min_float (float): Minimum allowed value (exclusive).
        max_float (float): Maximum allowed value (exclusive).

    Returns:
        float: New position after wave impact, rounded to 2 decimals.

    Examples:
        >>> apply_wave_impact(0, -90, 90)
        0.73
        >>> apply_wave_impact(45, -90, 90)
        44.35
        >>> apply_wave_impact(-10, -90, 90)
        -9.5
    '''

    num = random.random() * 2 - 1
    new_position = position + num
    
    if min_float < new_position < max_float:
        return round(new_position, 2)

    else:
        while not min_float < new_position < max_float:
            num = random.random() * 2 - 1
            new_position = position + num
        return round(new_position, 2)

def wave_hit_vessel(latitude: float,longitude: float):
    '''
    Simulate a wave hitting the vessel, affecting both latitude and longitude.

    Parameters:
        latitude (float): Current latitude of the vessel.
        longitude (float): Current longitude of the vessel.

    Returns:
        tuple: New (latitude, longitude) after wave impact.

    Examples:
        >>> wave_hit_vessel(0, 0)
        (0.65, -0.32)
        >>> wave_hit_vessel(45, -73)
        (44.78, -73.21)
        >>> wave_hit_vessel(-20, 100)
        (-19.55, 100.77)
    '''

    latitude_new = apply_wave_impact(latitude, MIN_LAT, MAX_LAT)
    longitude_new = apply_wave_impact(longitude, MIN_LONG, MAX_LONG)
    return (latitude_new, longitude_new)

def move_toward_waypoint(current_latitude: float, current_longitude: float,\
waypoint_latitude: float, waypoint_longitude: float):
    '''
    Move the vessel a single step toward a waypoint.

    Parameters:
        current_latitude (float): Current latitude of the vessel.
        current_longitude (float): Current longitude of the vessel.
        waypoint_latitude (float): Target latitude of the waypoint.
        waypoint_longitude (float): Target longitude of the waypoint.

    Returns:
        tuple: Updated (latitude, longitude) after moving,
         rounded to 2 decimals.

    Examples:
        >>> move_toward_waypoint(0, 0, 10, 10)
        (6.5, 6.8)
        >>> move_toward_waypoint(45, -73, 50, -70)
        (47.8, -71.7)
        >>> move_toward_waypoint(-10, 20, 0, 30)
        (-5.2, 25.3)
    '''

    scale = random.random() + 1
    new_latitude = current_latitude + \
    (waypoint_latitude - current_latitude) / scale

    new_longitude = current_longitude + \
    (waypoint_longitude - current_longitude) / scale

    if new_latitude <= MIN_LAT:
        new_latitude = MIN_LAT

    if new_latitude >= MAX_LAT:
        new_latitude = MAX_LAT

    if new_longitude <= MIN_LONG:
        new_longitude = MIN_LONG

    if new_longitude >= MAX_LONG:
        new_longitude = MAX_LONG

    return round(new_latitude, 2), round(new_longitude, 2)

def vessel_menu():
    '''
    Run the interactive vessel console for navigation.

    Displays a menu allowing the captain to:
        1) Set a waypoint (asks for coordinates),
        2) Move toward the waypoint with a status report, and
        3) Exit the console.

    Handles:
        - Storm countdown (STORM_STEPS)
        - Wave impact with 20% chance
        - Success if within 10 km of waypoint
        - Failure if storm countdown reaches 0

    Parameters:
        None

    Returns:
        None
    '''

    print("Welcome to the boat menu!")
    current_latitude, current_longitude = get_gps_location()

    waypoint_latitude = -200
    waypoint_longitude = -200
    storm_countdown = STORM_STEPS
    count = 0

    while count < 1:
        print("Please select an option below:")
        print("1) Set waypoint")
        print("2) Move toward waypoint and Status report")
        print("3) Exit boat menu")

        choice = int(input("Choose: "))

        if choice == 1:
            print("Enter waypoint coordinates.")
            waypoint_latitude, waypoint_longitude = get_gps_location()
            print("Waypoint set to latitude of", waypoint_latitude, \
            "and longitude of", waypoint_longitude)

        elif choice == 2:
            if waypoint_latitude == -200 and waypoint_longitude == -200:
                print("No waypoint set.")

            else:
                current_latitude, current_longitude = \
                move_toward_waypoint(current_latitude, \
                current_longitude, waypoint_latitude, waypoint_longitude)
                print("Captain Log: Journeyed towards waypoint.")

                if random.random() < 0.20:
                    current_latitude, current_longitude = \
                    wave_hit_vessel(current_latitude, current_longitude)
                    print("Captain Log: Wave impact recorded.")
                        
                print("Current position is latitude of", \
                current_latitude, "and longitude of", current_longitude, )

                distance = distance_two_points(current_latitude, \
                current_longitude, waypoint_latitude, waypoint_longitude)
                print("Distance to waypoint:", distance,"km")
                
                storm_countdown -= 1
                print("Storm T-minus:", storm_countdown)
                
                if distance <= 10.0:
                    return print\
                    ("Mission success: waypoint reached before storm.")
                    
        elif choice == 3:
            return print("Console closed by captain.")