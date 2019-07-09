import time
import pandas as pd
#import numpy as np
"""
initialize main variables here to assist in error correction.
"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
daysofweek = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        #receive the input city
        city = input("Please enter the name of the city you want to analyze: ").lower()
        if(city not in CITY_DATA):
            city = input("Are you sure that was a valid city? Program will quit if invalid again. \n Only enter Chicago, New York City, or Washington (case insensitve). Try again:").lower()
            if(city not in CITY_DATA):
                print("Second attempt failed. Program terminating.")
                quit()
            break
        break
    # get user input for month (all, january, february, ... , june)
    while True:
        #receive the input month
        month = input("Please enter the month you want to analyze, type all for all months: ").lower()
        if(month not in months):
            month = input("Are you sure that was a valid month? Program will quit if invalid again. \nOnly enter January-June (case insensitive): ").lower()
            if(month not in months):
                print("Second attempt failed. Program terminating.")
                quit()
            break
        break
   # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day of the week: ").lower()
        if(day not in daysofweek):
            #receive day of the week
            day = input("Please enter a valid day of the week. Program will quit if invalid again. (full name only, case insensitive): ").lower()
            if(day not in daysofweek):
                print("Second attempt failed. Program terminating.")
                quit()
            break
        break
    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int - specs of the data specify that there will only be datat from the first 6 months
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month ]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week']==day.title()]
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()
    # display the most common month
    print('\nMost common month: ', months[df['month'].mode()[0]-1].title())
    # display the most common day of week
    print('\nMost common day of week: ', df['Day of Week'].mode()[0])
    # display the most common start hour
    print('\nMost common start hour (in military time): ', df['Start Time'].dt.hour.mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    # display most commonly used start station
    moststarts = df['Start Station'].mode()[0]
    print("Most starts happened at: ", moststarts)
    # display most commonly used end station
    mostends = df['End Station'].mode()[0]
    print("Most endings happened at: ", mostends)
    # display most frequent combination of start station and end station trip
    df['Tally'] = 1
    newerframe = df.merge(pd.DataFrame({'Tally':df.groupby(['Start Station','End Station'])['Tally'].size()}), left_on=['Start Station', 'End Station'], right_index=True)
    #print("Most common start and end: ", mostcombined, '/n')
    #determine what the highest tally is
    maxcombo = int(newerframe['Tally_y'].max())
    newerframe = newerframe.loc[(newerframe['Tally_y'] == maxcombo)].head(1)
    print("Most frequent combination of stations: \n", newerframe[['Start Station','End Station']])
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    totaltraveltime = df['Trip Duration'].sum()
    print("Total travel time: ", totaltraveltime)
    # display mean travel time
    meantraveltime = df['Trip Duration'].mean()
    print("Mean travel time: ", meantraveltime)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        df['User Type'].fillna("Unknown User Type",inplace=True)
        user_types = df['User Type'].value_counts()
        print("Summarizing subscriber data: \n", user_types)
    else:
        print("No User Type data for this dataset.")

    if 'Gender' in df.columns:
        # Display counts of gender
        df['Gender'].fillna("Unknown gender",inplace=True)
        user_gender = df['Gender'].value_counts()
        print("\nSummarizing gender data: \n", user_gender)
    else:
        print("No Gender data for this dataset.")

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        minbday = df['Birth Year'].min()
        if(minbday > 1981 and minbday < 1997):
            print("\nEarliest birth year: ", int(minbday))
        elif(minbday < 1930):
            print("\nNot sure how this possible, but the earliest birth year for riders was: ", int(minbday),"!")
        maxbday = df['Birth Year'].max()
        print("Most recent birth year: ", int(maxbday))
    else:
        print("No Birth Year data for this datset.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_rawdata(df):
    """
    use this function to show the first 5 records of stats. After that, program will ask if the user would like to see more stats/specify a number or rows. This number must be received as an int
    we just continue with 5 lines and repeat until the user says no.
    """
    counter=0
    numlines=len(df.index)
    userlinecnt = 0
    #limiting while to the number of lines in the df for the sake of running this again and again until we run out of data.
    while (counter <= numlines):
        #prompt the user for whether they would like to see data or not
        data_yn = input("Would you like to see the raw data? yes or no: ").lower()
        if(counter > 0 and data_yn == 'yes'):
            userinputline = input("Would you like to specify a number of lines? yes or no: ").lower()
            if(userinputline == 'yes'):
                print("Max lines: ", numlines)
                #using try here incase the input can't be resolved to an integer for example 4345l;,sdk
                try:
                    userlinecnt = int(input("How many lines would you like to see?"))
                    print(df.head(int(userlinecnt)))
                    continue
                except:
                    print("Invalid response. Here's 5 lines instead.")
                    #print the next 5 in the following if statement
            else:
                print("Invalid response or no. Here's 5 lines instead. Moving on...")
                #print the next 5 in the following if statement

        #handle the response from the data_yn prompt yes or no
        if (data_yn == 'yes'):
            print(df.iloc[counter:counter+5])
            counter+=5
            continue
        elif (data_yn == 'no'):
            break
        else:
            print("Invalid response entered. Must enter yes or no.")


def extrafun(df):
    """
    Prompts the user if they would like to copy the data to the clipboard for further analysis
    """
    clipboard = input("Would you like to copy all the data to the clipboard for extra analysis fun? \nYou can copy this into Excel. \n yes or no: ").lower()
    if(clipboard == 'yes'):
        df.to_clipboard(excel=True,sep=',')
        print("Data copied.\n")
    elif(clipboard == 'no'):
        print("You selected no, moving on...\n")
    else:
        print("Invalid option entered, moving on...\n")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_rawdata(df)
        extrafun(df)
        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart.lower() != 'yes':
            print("You selected no or input an invalid option. Shutting down program...\n")
            break


if __name__ == "__main__":
    main()
