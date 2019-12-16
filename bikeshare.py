"""This script was written by Appau Ernest K.M 
purpose:To enable one interactively perform analysis and draw insight 
from the rideshare data found in chicago,new york and washington csv data files.
got some help from  sources: Medium.com,google.com ,stackoverflow,towardsdatacience and other python blogs 
"""

import time
import pandas as pd
import numpy as np


def get_filters():
    """
    gest specific city, month, and day from the user to begin  analysis.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    city = input("Hi,please enter the name of the city bike share data you want to explore__options[Chicago,new york city ,washington]:: ").lower()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
        "Sorry ,the city you entered is not cataloged yet,please input one of the following (chicago,new york city ,washington)!:: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter the month's data you want to analyze__options[january...june]:: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("what day of the week do you want to analyze...?please enter [Monday...sunday ]: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable and returns pandas 
    dataframe of city data analysis filtered month and day arguments

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    """
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """ stats on the most frequent times of travel."""

    print('\ncomputing the Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(" most common month is: {}".format(
        str(df['month'].mode().values[0]))
    )

    # display the most common day of week
    print(" most common day of the week: {}".format(
        str(df['day_of_week'].mode().values[0]))
    )

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("most common start hour: {}".format(
        str(df['start_hour'].mode().values[0]))
    )


    print("\nprocess time was %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """ stats on the most popular stations and trip."""

    print('\ncomputing Most Popular Stations and Trips....\n')
    start_time = time.time()

    # display most commonly used start station
    print("most common start station is: {} ".format(
        df['Start Station'].mode().values[0])
    )

    # display most commonly used end station
    print("most common end station is: {}".format(
        df['End Station'].mode().values[0])
    )

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    print(" most common start and end station combo is: {}".format(
        df['routes'].mode().values[0])
    )

    print("\nprocess took  %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """ statistics on the total and average trip duration."""

    print('\ncomputing Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("total travel time is: {}".format(
        str(df['duration'].sum()))
    )

    # display mean travel time
    print(" mean travel time is: {}".format(
        str(df['duration'].mean()))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """ statistics on bikeshare users."""

    print('\ncomputing  User Statistics ,will display soo.....\n')
    start_time = time.time()

    # Display counts of user types
    print("Below are the total  counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print(" Total counts of gender are :")
        print(df['Gender'].value_counts())


        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: {}".format(
            str(int(df['Birth Year'].min())))
        )
        print("The latest birth year is: {}".format(
            str(int(df['Birth Year'].max())))
        )
        print("The most common birth year is: {}".format(
            str(int(df['Birth Year'].mode().values[0])))
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start_loc = 0
    end_loc = 5

    display_active = input("Do you want to view the raw data?: ").lower()

    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Do you wish to view more rows?: ").lower()
            if end_display == 'no':
                break


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\n would you like to explore more bikeshare data ? please enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a nice day ')
            break


if __name__ == "__main__":
	main()