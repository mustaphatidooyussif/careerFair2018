#YUSSIF MUSTAPHA TIDOO
#CLASS OF 2020
import argparse
import csv
import datetime as dt
from datetime import datetime
import timeit

#Read a csv file and returns ordered dictionary
def read_csv(filename):
    t1 = datetime.now()
    file = open(filename, 'r', encoding='utf-8-sig') 
    csv_reader = csv.DictReader(file)
    return csv_reader, datetime.now()-t1

#This finds when the last case or the last date were recorded
def last_dates_of(indicator,reader):
    t2 = datetime.now()
    datetime_list =[]

    #Make pass through the data
    #append all the specified indicator dates in to the datetimee_List
    #Fine the latest date from the list
    for line in reader:
        if (line['Indicator']== indicator):
            date = datetime.strptime(line['Date'],"%d/%m/%Y")
            datetime_list.append(date)
    return max(datetime_list), datetime.now()-t2

#This returns the ebola free date of the country
def ebola_free(last_case):
    t3 = datetime.now()

    #add 42 days to the last case recorded date
    days_ = dt.timedelta(days = 42)
    free_date = last_case + days_
    return free_date, datetime.now()- t3

def rate(indicator,reader):
    t4 = datetime.now()
    #Take first value and first date if indicatotor is cumulative case
    #Otherwise take the second value and the second date
    if indicator == "cumulative_cases":
        line= next(reader)
    else:
        line= next(reader)
        line= next(reader)

    #Initialize previous date and value with the value and date obtained
    prev_date = datetime.strptime(line['Date'],"%d/%m/%Y")
    prev_val = line['Value']
        

    #Make pass through the data
    #check whether indicator is cummulative cases or cummulative deaths
    #Calculate rate and compare to previous rate
    #return the date of the highest rate
    rate = 0
    date = ''
    for line in reader:
        if (line['Indicator']== indicator):
            current_date = datetime.strptime(line['Date'],"%d/%m/%Y")
            cal_rate = (int(line['Value'])-int(prev_val))/int((current_date -prev_date).days)
            if (rate<cal_rate):
               rate = cal_rate
               date = current_date
            
            prev_val = line['Value']
            prev_date = current_date
    return date, datetime.now()-t4
               
def findPeaks(indicator,reader):
    t5 = datetime.now()
    if indicator == "cumulative_cases":
        line= next(reader)
    else:
        line= next(reader)
        line= next(reader)
    prev_date = datetime.strptime(line['Date'],"%d/%m/%Y")
    prev_val = line['Value']

    slope = []
    dates = []
    rate = 0
    #Make pass through the data
    #check whether indicator is cummulative cases or cummulative deaths
    #Calculate rate and compare to previous rate
    #append 1 to the list if infection rates or death rates are increasing and -1 when they decreasing.
    #append the dates too
    for line in reader:
        if (line['Indicator']== indicator):
            current_date = datetime.strptime(line['Date'],"%d/%m/%Y")
            cal_rate = (int(line['Value'])-int(prev_val))/int((current_date -prev_date).days)
            if rate < cal_rate:
                slope.append(1)
            else:
                slope.append(-1)
            rate = cal_rate
            dates.append(line['Date'])

    peak_dates =[]
    peak_count = 0
    #Go through the slope 
    #check for pairs [1,-1]. If exist
    #append the corresponding date in dates list to peak_dates
    #keep counting number of  pairs [1,-1]
    for peak in range(len(slope)):
        if slope[peak]==1 and slope[peak+1]== -1:
            peak_count = peak_count +1
            peak_dates.append(dates[peak])
    return peak_count, peak_dates,datetime.now()-t5  

def task1():
    t6 = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Specify the file to read")
    args = parser.parse_args()
    
    case, a_time = last_dates_of("cumulative_cases",read_csv(args.fname)[0])
    death, b_time = last_dates_of("cumulative_deaths",read_csv(args.fname)[0])
    free_date, c_time = ebola_free(case)
    inf_rate_d, d_time = rate("cumulative_cases",read_csv(args.fname)[0])
    death_rate_d, e_time = rate("cumulative_deaths",read_csv(args.fname)[0])
    inf_peaks, peaks_dates, f_time = findPeaks("cumulative_cases",read_csv(args.fname)[0])
    death_peaks,d_peaks_dates, g_time = findPeaks("cumulative_deaths",read_csv(args.fname)[0])

    program_time = (datetime.now() - t6).total_seconds()*1000
    with open("task1_answers-" +str(args.fname), "w", newline='') as file_two:
        csv_writer = csv.writer(file_two)
        csv_writer.writerow(['Task1 answers'])
        csv_writer.writerow(['Last case date: ' + str(case)])   #(a)Date the last case was recorded
        csv_writer.writerow(['Last death date: ' + str(death)])  #(b)Date the last death was recorded
        csv_writer.writerow(['Ebola-free date: '+ str(free_date)])#(c) Date the country will be declared Ebola free
        csv_writer.writerow(['Highest infection rate date: '+str(inf_rate_d)])  #(d)Date the highest infection rate was recorded
        csv_writer.writerow(['Highest death rate date: '+str(death_rate_d)]) #(e)Date the highest death rate was recorded
        csv_writer.writerow(['Total Infection rate peaks: '+ str(inf_peaks)])#(f)Number of infection rate peaks
        for j, i in enumerate(peaks_dates):         #(f)Dates when the infection rate peaks occur
            csv_writer.writerow(['Peak ' + str(j+1)+ " Date: "+ str(i)])
        csv_writer.writerow(['Total Death rate peaks: '+ str(death_peaks)]) #(g)Number of  death rate peaks
        for m, k in enumerate (d_peaks_dates):              #(g)Dates when the death rate peaks occur
            csv_writer.writerow(['Peak ' + str(m+1)+ " Date: "+ str(k)])

    with open("task1_times-" +str(args.fname), "w", newline='') as file_three:
        csv_writer2 = csv.writer(file_three)
        csv_writer2.writerow(['Runtime of'])
        csv_writer2.writerow(['File reading: '+ str(read_csv(args.fname)[1].total_seconds()) + " milliseconds"])#runtime of file reading
        csv_writer2.writerow(['(a): '+str(a_time.total_seconds() * 1000)  + " milliseconds"]) #runtime of (a)
        csv_writer2.writerow(['(b): '+str(b_time.total_seconds() * 1000)  + " milliseconds"]) #runtime of (b)
        csv_writer2.writerow(['(c): '+str(c_time.total_seconds() * 1000)  + " milliseconds"]) # runtime of (c) 
        csv_writer2.writerow(['(d): '+str(d_time.total_seconds() * 1000) + " milliseconds"]) # runtime of (d)
        csv_writer2.writerow(['(e): '+str(e_time.total_seconds() * 1000) + " milliseconds"]) # runtime of (e)
        csv_writer2.writerow(['(f): '+str(f_time.total_seconds() * 1000) + " milliseconds"])# runtime of (f)
        csv_writer2.writerow(['(g): '+str(g_time.total_seconds() * 1000) + " milliseconds"])# runtime of (g)
        csv_writer2.writerow(['Program: '+str(program_time) + " milliseconds"])# runtime of the program
    
    e2 = datetime.now()

    
if __name__=="__main__":
    task1()
    
