# -*- coding: utf-8 -*-
"""US Bikeshare Data analysis.

This module demonstrates analysis on the US Bikeshare program. User derived
data is anonymized.

Notes:
    User selects city, month, and day of the week to analysis
    on Bikeshare member usage. Data tracks trip timestamp, station leaving,
    station arriving, user type, gender, and birth year.

    Not all cities have gender and birth year data.

    Current cities available are Chicago, New York City, and Washington.

    Analysis currently looks at: time stats, station stats, trip duration stats,
    and user stats where available.

"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # Get user input for city (chicago, new york city, washington)
    print('-'*40 + '\n')

    #Menu for city input selection. Setup selection variable and city list.
    city_question = 0
    cities = ['Chicago', 'New York City', 'Washington']

    #Print city selection menu
    for index, city in enumerate(cities):
        print('{}> {}'.format(index + 1, city))

    #While loop that makes sure correct available menu item is selected
    while True:
        try:
            while (city_question < 1) or (city_question > 3):
                city_question = int(input("Which city to analyze? "))

                if(city_question < 1) or (city_question >3):
                    print("Please type a number between 1-3. \n")
            break
        except ValueError:
            print("Please type a number between 1-3. \n")

    #Pass along city information for data loading
    city = cities[int(city_question) - 1]

    #Being polite and making sure user is informed
    print("Thank you. You requested: {} \n".format(city))
    print('-'*40 + '\n')

    # User input for month. Month selection variable and month list for menu and data load.
    month_question = -1
    months = ['all', 'January', 'February', 'March', 'April', 'May', 'June']

    #Print menu for month selection
    for index, month in enumerate(months):
        print('{}> {}'.format(index, month))

    #While loop that makes sure correct available menu item is selected
    while True:
        try:
            while (month_question < 0) or (month_question > 6):
                month_question = int(input("Which month to analyze? "))

                if(month_question < 0) or (month_question >6):
                    print("Please type a number between 0-6. \n")
            break
        except ValueError:
            print("Please type a number between 0-6. \n")

    #Pass along month information for data loading
    month = months[month_question]

    #Being polite and making sure user is informed
    print("Thank you. You requested: {} \n".format(month))
    print('-'*40 +'\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    #Setup day question variable and day list
    day_question = -1
    day_list = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    #Print menu for day selection
    for index, d_list in enumerate(day_list):
        print('{}> {}'.format(index, d_list))

    #While loop that makes sure correct available menu item is selected
    while True:
        try:
            while (day_question < 0) or (day_question > 7):
                day_question = int(input("Which day to analyze? "))

                if(day_question < 0) or (day_question > 7):
                    print("Please type a number between 0-7. \n")
            break
        except ValueError:
            print("Please type a number between 0-7. \n")

    #Pass along month information for data loading
    day = day_list[day_question]

      #Being polite and making sure user is informed about their total selections.
    print("Thank you. Your choices were: city = {},"\
          " month = {}, and day = {} \n".format(city, month, day))

    #Time sleep to create small delay so data scroll looks cleaner
    time.sleep(2)
    print('-'*40 +'\n')
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read in user selected city data.
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month from Start Time column for analysis. Uses name.
    df['month'] = df['Start Time'].dt.month_name()

    # Extract day from Start Time column for analysis. Uses name.
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Extract hour from Start Time column for time analysis.
    df['hour'] = df['Start Time'].dt.hour

    #Dataframe selection filters if user requested
    # Filter by month if applicable
    if month != 'all':
        # Filter by month to create the new dataframe.
        df = df[df['month'] == month]

    # Filter by day of week if applicable.
    if day != 'all':
        # Filter by day of week to create the new dataframe and correct format.
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for {}...\n'.format(city))
    start_time = time.time()

    # Calculate the most frequent month using mode function.
    frequent_month = df['month'].mode()[0]

    # Calculate the most frequent day of week using mode function.
    frequent_day_of_week = df['day_of_week'].mode()[0]

    # Calculate the most frequent start hour using mode function.
    frequent_hour = df['hour'].mode()[0]

    # Print time stats
    print("Month, Day, and Hour Frequency Stats:\n")
    print("Most Frequent Month:  {}\n".format(frequent_month))
    print("Most Frequent Day:  {}\n".format(frequent_day_of_week))
    print("Most Frequent Hour:  {}\n".format(frequent_hour))

    # Print time stats calculation time
    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40 +'\n')


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips for {}...\n'.format(city))
    start_time = time.time()

    # Calculate most frequently used start station.
    frequent_start = df['Start Station'].mode()[0]

    # Calculate most commonly used end station.
    frequent_end = df['End Station'].mode()[0]

    # Calculate most frequent combination of start station and end station trip.
    # Create start and end station combo column.
    df['trip_combination'] = df['Start Station'] + ' and ' + df['End Station']
    frequent_combination = df['trip_combination'].mode()[0]
    trip_value_count = df['trip_combination'].value_counts().head(5)

    # Print station stats calculation.

    print("Station Use Frequency Stats:\n")
    print("Most Frequent Starting Station:  {}\n".format(frequent_start))
    print("Most Frequent Ending Station:  {}\n".format(frequent_end))
    print("Most Frequent Start and End Station Combination:  {}\n".format(frequent_combination))
    print("Top 5 Frequently Used Station Start and End Ccombinations & Trip Count...\n")
    print(trip_value_count)

    # Print station stats calculation time
    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40 +'\n')


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    # Calculate Trip Duration Stats

    print('\nCalculating Trip Duration Stats for {}...\n'.format(city))
    start_time = time.time()

    # Calculate total travel time
    total_duration = df['Trip Duration'].sum()

    # Convert total monthly trip duration from seconds to minutes and seconds
    tot_dur_min = (int(total_duration/60))
    tot_dur_sec = (int(total_duration % 60))

    # Calculate mean travel time
    mean_duration = df['Trip Duration'].mean()

    # Convert mean trip duration from seconds to minutes and seconds
    mean_dur_min = (int(mean_duration/60))
    mean_dur_sec = (int(mean_duration % 60))

    # Calculate total city wide trips
    tot_city_trips = (int(total_duration/mean_duration))

    # Print travel time stats calculation.
    print("Trip Duration Stats:\n")
    print("Total city-wide trips: {}\n".format(tot_city_trips))
    print("Total City Trip Duration (mins. and secs.):  {}:{}\n".format(tot_dur_min,tot_dur_sec))
    print("Mean Duration Per Trip: (mins. and secs.) {}:{}\n".format(mean_dur_min,mean_dur_sec))

    # Print travel time stats calculation time
    print("\nThis took {}s seconds.".format(round((time.time() - start_time),4)))
    print('-'*40 +'\n')


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for {}...\n'.format(city))
    start_time = time.time()

    # Available user stats calculation. Not all city files have complete user stats
    print("User Stats: \n")

    # Calculate summary count of user types
    user_types = df['User Type'].value_counts()
    print("Summary of User Types:  {}\n".format(user_types))

    #Seperate handler since not all cities include gender data
    if 'Gender' not in df:
        print("Sorry, {} does not have gender data...\n".format(city))

    else:
    # Calculate summary counts of gender

        gender_count = df['Gender'].value_counts().to_string()
        gender_ratio = df['Gender'].value_counts('Female').mul(100).to_string()
        print("Summary of User Genders (count):  {}\n".format(gender_count))
        print("Male vs Female ratio (per centage): {}\n".format(gender_ratio))

    #Seperate handler for Birth Year due to missing data issues
    if 'Birth Year' not in df:
        print("Sorry, {} does not have birth year data...\n".format(city))

    else:
        frequent_birth = df['Birth Year'].mode()[0]
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        print("Most Frequently Selected Birth Year:  {}\n".format(int(frequent_birth)))
        print("Oldest Selected Birth Year:  {}\n".format(int(oldest)))
        print("Youngest Selected Birth Year:  {}\n".format(int(youngest)))



    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40 +'\n')



def raw_data(df,city):
    """ Ask user if they wish to see 5 lines of raw data """
    head_count = 0

    # Ask user if they wish to see raw data
    init_request = input('Do you wish to see raw data?'\
                        '(Y)es or (N)o to continue...\n')
    if init_request.lower() not in ['yes', 'y']:
        print('Thank you. We will continue...\n')
        print('-'*40 +'\n')
        return
    else:
        print("First 5 rows of raw data from {}".format(city))
        print(df.iloc[head_count : head_count + 5, 1:])
        print('-'*40 +'\n')
        head_count = head_count + 5
    # Continue to show additional data as requested    
    while True:
        repeat_request = input('Do you wish to see more data from {}?'\
                              '(Y)es or (N)o to continue...\n'.format(city))
        if repeat_request.lower() in ['yes', 'y']:
            print(df.iloc[head_count : head_count + 5, 1:])
            head_count = head_count + 5
        else:
             break

def main():
    """ The main part of our program """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        raw_data(df,city)

        restart = input('\nWould you like to restart? Enter (y)es to restart.'\
                        ' Enter any other key to quit...')
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
    main()
