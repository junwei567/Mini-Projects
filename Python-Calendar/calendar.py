from pprint import pprint
import numpy as np

def leap_year(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True

def R(y,x):
    return y%x
    
# Gauss' algorithm to detemine first day of the particular year
def day_of_week_jan1(year):
     
    d = R(1 + 5*R(year - 1, 4) + 4*R(year - 1, 100) + 6*R(year - 1, 400), 7)
    return d

def num_days_in_month(month_num, leap_year):
    if month_num in [1,3,5,7,8,10,12]:
        return 31
    elif month_num == 2:
        if leap_year == True:
            return 29
        else:
            return 28
    else:
        return 30

# Outputs a list, which contains the print statement of each line of the calendar month
def construct_cal_month(month_num, first_day_of_month, num_days_in_month):
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'} 
    week = []
    for spacing in range(first_day_of_month):
        week.append('   ')
    display_day = '  S  M  T  W  T  F  S'
    cal_list = [month_names[month_num]]
    for date_num in range(1, num_days_in_month + 1):
        if len(week) == 7:
            cal_list.append(''.join(week))
            week = []
        week.append(str(date_num).rjust(3))
    cal_list.append(''.join(week)) # to add last week
    return(cal_list) #cal_list is a list of strings, with each entry refering to a new line in a calender
    
def print_cal_month (list_of_str):
    ret_val = ''
    for l in list_of_str:
        ret_val += l
    return ret_val #ret_val is a string that has combined the input list in a printable format

# compiling the functions together
def construct_cal_year(year):
    first_day = day_of_week_jan1(year)
    output_lst = [year]
    leap_true = leap_year(year)
    for month in range(1,13):
        num_days = num_days_in_month(month,leap_true)
        new_entry = construct_cal_month(month, first_day, num_days)
        output_lst.append(new_entry)
        first_day = (first_day + num_days) % 7
    return output_lst
        
def display_calendar(year):
    ret_val = construct_cal_year(year)[1:]
    ret_str = ''
    for i in ret_val:
        i.insert(1, "  S  M  T  W  T  F  S")
        ret_str += '\n'.join(i) + '\n'*2     
    return ret_str[:-2]

pprint(construct_cal_year(2020))


# modified to only give a particular month
def display_calendar_modified(year, month = None):
    if month == None:
        return display_calendar(year)
    mod_cal = construct_cal_year(year)
    mod_cal = mod_cal[month]
    
    ret_str = ''
    
    mod_cal.insert(1, "  S  M  T  W  T  F  S")
    ret_str += '\n'.join(mod_cal) + '\n'*2     
    return ret_str[:-2]