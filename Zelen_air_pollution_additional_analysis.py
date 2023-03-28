from groupproject3_finalversion import *

measurements_from_UHF, measurements_from_dates = read_data("air_quality.csv")
measurements_from_zipcodes, measurements_from_boroughs = read_uhf("uhf.csv")

def new_york_city_pollution(zipcode):
    nyc_uhf = measurements_from_zipcodes[zipcode]
    nyc_uhf = str(nyc_uhf[0])
    pollution_indexes = []
    nyc_uhf_pollution = measurements_from_UHF[nyc_uhf]

    for instance in nyc_uhf_pollution:
        pollution_indexes.append(instance[3])

    highest_pollution = max(pollution_indexes)
    lowest_pollution = min(pollution_indexes)

    text = f"Highest pollution index in zipcode {zipcode} was {highest_pollution} and the lowest pollution index was {lowest_pollution}"
    return text

def uhf_worst_pollution(year):
    year_users_data = year[2:]
    uhf_measurements = measurements_from_UHF.values()
    worst_pollution_index = 0
    most_polluted_uhf = 0
    for data_list in uhf_measurements:
        for measurement_tuple in data_list:
            date = measurement_tuple[2]
            year_from_date = date[len(date)-2:len(date)]
            if(year_users_data == year_from_date and measurement_tuple[3] > worst_pollution_index):
                worst_pollution_index = measurement_tuple[3]
                most_polluted_uhf = measurement_tuple[0]

    text = f"{most_polluted_uhf} UHF had the worst pollution with the pollution index of {worst_pollution_index} in the year of {year}"
    return text

def average_pollution(borough, year):
    borough_uhfs = measurements_from_boroughs[borough]
    year_users_data = year[2:]
    sum_pollution_indexes = 0
    counter = 0
    for uhf_id in borough_uhfs:
        uhf_id = str(uhf_id)
        measurement_tuples = measurements_from_UHF[uhf_id]
        for measurement_tuple in measurement_tuples:
            date = measurement_tuple[2]
            year_from_date = date[len(date)-2:len(date)]
            if(year_users_data == year_from_date):
                sum_pollution_indexes += measurement_tuple[3]
                counter += 1
    average = sum_pollution_indexes/counter
    return average

def most_polluted_borough_nyc(user_input_year):
    most_polluted_borough = ""
    most_polluted_borough_pollution_index = 0
    borough_names = ["Manhattan", "Queens", "Brooklyn", "Bronx", "StatenIsland"]

    for nyc_borough in borough_names:
        average_borough_pollution_index = average_pollution(nyc_borough,user_input_year)
        if(average_borough_pollution_index > most_polluted_borough_pollution_index):
            most_polluted_borough_pollution_index = average_borough_pollution_index
            most_polluted_borough = nyc_borough
    
    text2 = f"The most polluted borough in {user_input_year} was {most_polluted_borough} with average pollution index of {most_polluted_borough_pollution_index:.2f}"
    print(text2)
    return most_polluted_borough

def index_lower_10(measurements_from_UHF):
    uhf_lower_10 = set()
    uhf_measures = measurements_from_UHF.values()
    for data_set in uhf_measures:
        for measurement_tuple in data_set:
            uhf_pollution_index = measurement_tuple[3]
            if(measurement_tuple[2] == "6/1/09" and uhf_pollution_index < 10):
                uhf_lower_10.add(measurement_tuple[0])
    return uhf_lower_10

def main():
    zip_codes_nyc = measurements_from_zipcodes.keys()
    user_input_zipcode = ""
    while(user_input_zipcode not in zip_codes_nyc):
        user_input_zipcode = input("Enter a zip code: ")
    highest_lowest_pollution = new_york_city_pollution(user_input_zipcode)
    print(highest_lowest_pollution)
    user_input_year = 0
    while(user_input_year!="quit"):
        user_input_year = int(input("Enter a year from 2009 to 2019 or type quit to go to the next prompt: "))
        if(user_input_year >= 2009 and user_input_year<=2019):
            user_input_year = str(user_input_year)
            print(uhf_worst_pollution(user_input_year))
            break
        else:
            print("There is no data for the selected year. Try again")

    user_input_borough = ""
    borough_names = ["Manhattan", "Queens", "Brooklyn", "Bronx", "StatenIsland"]
    while(user_input_borough not in borough_names):
        user_input_borough = input("Type in the name of one of the following boroughs: Manhattan, Queens, Brooklyn, Bronx, StatenIsland: ")

    average_pollution_in_area = average_pollution(user_input_borough, user_input_year)
    avg = f"Average pollution index in {user_input_borough} in {user_input_year} is {average_pollution_in_area:.2f}"
    print(avg)

    print("Which borough was by average the most polluted in ", user_input_year, "?")
    nyc_borough = most_polluted_borough_nyc(user_input_year)

    print("Which UHFs had a pollution index lower than 10 on 6/1/09?")
    
    index_lower_than_10 = index_lower_10(measurements_from_UHF)
    print(index_lower_than_10)

if __name__ == "__main__": 
  main()