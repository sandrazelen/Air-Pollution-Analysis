import csv

def read_data(filename):
    data_by_uhf = {}
    data_by_date = {}
    measurement = ()
    list_of_measurements =[]

    with open(filename, mode = 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames = ("geo_id", "geo_description", "date", "particulate_matter"))
        for line in csv_reader:
            geo_id = line["geo_id"]
            geo_description = line["geo_description"]
            date = line["date"]
            
            particulate_matter = float(line["particulate_matter"])
            measurement = (geo_id, geo_description, date, particulate_matter)
            
            list_of_measurements.append(measurement)
            
            if geo_id not in data_by_uhf.keys():
                data_by_uhf[geo_id]= list_of_measurements
                    
            else:
                data_by_uhf[geo_id]+=list_of_measurements
                
            list_of_measurements = []
            list_of_measurements.append(measurement)
            
            if date not in data_by_date.keys():
                data_by_date[date] = list_of_measurements
                    
            else:
                data_by_date[date]+= list_of_measurements
            
            list_of_measurements = []
        return (data_by_uhf, data_by_date)



def measurement_to_string(measurement):
    geo_id = measurement[0]
    geo_description = measurement[1]
    date = measurement[2]
    particulate_matter = measurement[3]

    text = f"{date} UHF {geo_id} {geo_description} {particulate_matter} mcg/m^3"
    return text

def read_uhf(filename):

    with open(filename, mode = 'r', encoding='utf-8-sig') as csv_file:
        data_by_zip_code = {}
        data_by_borough = {}
        uhf_id_list = []
        csv_reader = csv.DictReader(csv_file, fieldnames = ("borough", "uhf_id", "geo_id"), restkey = 'zip_codes')
        for line in csv_reader:
            borough = line["borough"]
            uhf_id = line["uhf_id"]
            geo_id = int(line["geo_id"])
            zip_codes = line["zip_codes"] 
    
            for specific_zip_code in zip_codes:
                uhf_id_list.append(geo_id)
                if specific_zip_code not in data_by_zip_code.keys():
                    data_by_zip_code[specific_zip_code]= uhf_id_list
                    
                else:
                    data_by_zip_code[specific_zip_code]+=uhf_id_list
                uhf_id_list = []

            uhf_id_list.append(geo_id)
            if borough not in data_by_borough.keys():
                data_by_borough[borough]=uhf_id_list
                
            else:
                data_by_borough[borough]+=uhf_id_list
            uhf_id_list = []   
    return (data_by_zip_code, data_by_borough)


def main():
    data_filename = "air_quality.csv"
    uhf_filename = "uhf.csv"

    data_by_uhf_and_date = read_data(data_filename)
    data_by_zip_code_and_borough =read_uhf(uhf_filename)

    data_by_uhf = data_by_uhf_and_date[0]
    data_by_date = data_by_uhf_and_date[1]
    data_by_zip_code = data_by_zip_code_and_borough[0]
    data_by_borough = data_by_zip_code_and_borough[1]
    user_input = ""

    while(user_input != "quit"):
        user_input =input("Do you want to search the data by zip code, UHF id, borough, or date? Write 'quit' if you don't want any more searches. ")
        if(user_input == "zip code"):
            user_input_zip_code = input("Type in a zipcode: ")
            uhf_from_zipcode = data_by_zip_code[user_input_zip_code]
            for uhf_value in uhf_from_zipcode:
                uhf_value = str(uhf_value)
                data_from_uhf = data_by_uhf[uhf_value]
                for measurement in data_from_uhf:
                    measurement_string = measurement_to_string(measurement)
                    print(measurement_string)

        elif(user_input == "UHF id"):
            user_input_uhf_id = input("Enter a UHF id: ")
            data_from_uhf = data_by_uhf[user_input_uhf_id]
            for measurement in data_from_uhf:
                measurement_string = measurement_to_string(measurement)
                print(measurement_string)

            
        elif(user_input == "borough"):
            user_input_borough = input("Enter a borough: ")
            uhf_from_borough = data_by_borough[user_input_borough]
            for uhf_value in uhf_from_borough:
                uhf_value = str(uhf_value)
                data_from_uhf = data_by_uhf[uhf_value]
                for measurement in data_from_uhf:
                    measurement_string = measurement_to_string(measurement)
                    print(measurement_string)
            
        elif(user_input == "date"):
            user_input_date = input("Enter a date: ")
            data_from_date = data_by_date[user_input_date]
            for measurement in data_from_date:
                measurement_string = measurement_to_string(measurement)
                print(measurement_string)

        elif(user_input == "quit"):
            break
        else:
             print("Please input one of the following: 'zip code', 'UHF id', 'borough', 'date' or 'quit'")

if __name__ == "__main__": 
  main()