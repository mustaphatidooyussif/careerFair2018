#Yussif Mustapha Tidoo
#Class of 2020

import argparse
import csv
import datetime as dt
from datetime import datetime

#Reads the seconf csv file and returns the column as a list    
def read_file_two(file_two):
    a_list=[]
    with open(file_two, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            a_list.append(line[0])
    return a_list

#Matches a sublist to a list and returns the index of pattern
#that is, where the pattern begins
def compare_lists(pat, txt):
    pat_len = len(pat)
    text_len = len(txt)

    #Make (text_len - pat_len + 1)passes
    #for each pass check if from current index, the sublist is
    #equal to the remaining list
    #finally returns the index where the lists are the same
    for i in range(text_len - pat_len + 1):
        if txt[i : i + pat_len] == pat:
            return i
            
def task2():
    t = datetime.now() #start time
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Specify the file to read")
    parser.add_argument("fname2", help="Specify the file to read")
    args = parser.parse_args()

    #read the sample_complex_ebola_data.csv 
    with open(args.fname, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)

        partial_series = read_file_two(args.fname2)

        
        myDict = {}
        myDict2={}
        #Make passes through the data
        #Put all values belonging to the same country, locality and indicator
        #in a list and use the (country name, locality and indicator) as a key to the list
        #Put all dates belonging to the same country, locality and indicator
        #in a list and use the (country name, locality and indicator) as a key to the list
        for line in csv_reader:
            key = str(line['Country']) +","+ str(line['Locality']) +"," + str(line['Indicator']) 
            if key not in myDict:
                myDict[key] = [line['Value']]
                myDict2[key] = [line['Date']]
            else:
                myDict[key].append(line['Value'])
                myDict2[key].append(line['Date'])

                
        myList=[]
        #Go through the cumulative values in the dictionary
        #Check if any of list contains all the sample_partial_times_series values
        #Return the key(it comprises country, locality and indicator) for the list containing the values
        for key, value in myDict.items():
            if set(partial_series).issubset(set(value)):
                my_key = key
                my_list = value
                the_country= key.split(",")[0]
                the_locality = key.split(",")[1]
                the_indicator = key.split(",")[2]

        index = compare_lists(partial_series, my_list)
        e = datetime.now() #end time
        delta = e-t      #Take time difference
        
    with open("task2_result-" + str(args.fname2), "w", newline='') as write_to:
        csv_writer = csv.writer(write_to)
        csv_writer.writerow([the_country+","+the_locality])   #write the country and the locality to file
        csv_writer.writerow([the_indicator])                  #write the indicator to  the file
        csv_writer.writerow([myDict2[my_key][index]])         #write the starting date to the file
        csv_writer.writerow([str(delta.total_seconds()*1000) + " milliseconds"])   #write the total runtime in milliseconds to the file

if __name__=="__main__":
    task2()
