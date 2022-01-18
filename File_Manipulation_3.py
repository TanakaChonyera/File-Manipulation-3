########################################################################################################################
#
#   CS programming project #9
#
#       Algorithm
#
#           Start
#               Prompt user for years
#               Build super dictionary
#               Function definitions
#               Prompt user for selection
#               Loop while user input valid or until user quits program with special input (validation check on input)
#                   Go to user selection (validation check on input)
#                       Call relevant functions
#                           Perform computations on super dictionary
#                           Return specified data
#                       Output results
#           End
#
########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import csv
import copy
from operator import itemgetter


def open_file(year_str):
    ''' This function takes a string parameter that is the year string for the file name, opens the file, and
returns a file pointer to the opened data file. '''

    print("Opening Data file for year {}: ".format(year_str))
    fp = year_str + '.csv'

    try:

        # If file found, make file pointer
        with open(fp, 'r') as file:
            fp = open(fp, 'r')

    # If File name not found, raise error
    except FileNotFoundError:

        print('Invalid filename:')
        return False

    # Return file pointer
    return fp


def build_dictionary(fp):
    ''' This function accepts the previously generated file pointer as input and returns the required
dictionary. '''

    # Initialize dictionaries and region list
    region_dict = {}
    country_dict = {}
    region_list = []

    # Using with syntax ensures file is closed after use
    with fp as file:

        reader = csv.reader(file)

        # Skip header line
        next(reader, None)

        # Iterate through file to get list of regions as they appear in the file
        for line_list in reader:

            if line_list[1] in region_list:

                # If region already in region list, skip
                continue
            else:

                # If region not in region list, add
                region_list.append(line_list[1])

        for region in region_list:

            # Reset file pointer to beginning of file
            file.seek(0)

            # Iterate through file to generate country dictionary
            for line_list in reader:

                if line_list[1] == region:

                    # Add country key and country data value to country dictionary, skip if invalid data in cells
                    try:

                        int(line_list[2])
                        float(line_list[3])
                        float(line_list[5])
                        float(line_list[9])
                        float(line_list[6])
                        float(line_list[7])
                        float(line_list[8])

                        country_dict[line_list[0]] = ((int(line_list[2]), float(line_list[3])), \
                                                      (float(line_list[5]), float(line_list[9])), \
                                                      (float(line_list[6]), float(line_list[7]), float(line_list[8])))

                    except ValueError:

                        continue

                else:

                    # Skip line if region in line does not match current specified region
                    pass

            # Add region key and country and country data value to region dictionary
            region_dict[region] = country_dict

            # Reset country dictionary
            country_dict = {}

    # Returns region dictionary
    return region_dict


def combine_dictionaries(year, subD, superD):
    ''' This function puts that dictionary as a value within a dictionary
that has year as the key. '''

    # Add region dictionary to super dictionary
    superD[year] = subD

    # Return super dictionary
    return superD


def search_by_country(country, superD, print_boolean):
    ''' This function takes in a string (the country name), a dictionary (the super year-key dictionary
created by combine_dictionary above) and a Boolean variable that indicates whether to
print (True) the country details on the screen or not (False). '''

    # Display data
    if print_boolean:

        # Iterate through years in super dictionary
        for year in superD:

            # Print year
            print('\n{:<10s}{:<5d}'.format('Year:', int(year)))

            # Iterate through region in specific year in super dictionary
            for region in superD[year]:

                # Iterate through countries in specific region in super dictionary
                for state in superD[year][region]:

                    # If country found, display country and country data
                    if country == state:
                        print('{:<10s}{:<s}'.format('Country:', country))
                        print('{:<10s}{:<5d}'.format('Rank:', int(superD[year][region][country][0][0])))
                        print('{:<10s}{:<5.2f}'.format('Score:', float(superD[year][region][country][0][1])))
                        print('{:<10s}{:<5.2f}'.format('Family:', float(superD[year][region][country][2][0])))
                        print('{:<10s}{:<5.2f}'.format('Health:', float(superD[year][region][country][2][1])))
                        print('{:<10s}{:<5.2f}'.format('Freedom:', float(superD[year][region][country][2][2])))
                        print('-'*20)

    else:

        # Initialize lists
        data_list = []
        data_list_of_tuples = []

        # Iterate through years in super dictionary
        for year in superD:

            # Iterate through region in specific year in super dictionary
            for region in superD[year]:

                # Iterate through countries in specific region in super dictionary
                for state in superD[year][region]:

                    # If country found, store country data in data list
                    if country == state:

                        # Add data to list
                        data_list.append(float(superD[year][region][country][0][1]))
                        data_list.append(float(superD[year][region][country][2][0]))
                        data_list.append(float(superD[year][region][country][2][1]))
                        data_list.append(float(superD[year][region][country][2][2]))

                        # Add data to list of tuples, reset data list
                        data_tuple = tuple(data_list)
                        data_list_of_tuples.append(data_tuple)
                        data_list = []

        # Return specified data as a list of tuples
        return data_list_of_tuples


def top_10_ranks_across_years(superD, year1, year2):
    ''' This function accepts the super dictionary and produces 2 lists of tuples. List 1 contains the top
10 countries and their ranks for year 1. List 1 (for year 1) is sorted by the ranks for that year. '''

    # Initialize lists and local dictionary
    year1_list = []
    year2_list = []
    year2_rank = []
    country_list = []

    # Iterate through years in super dictionary
    for year in superD:

        # Search for first year
        if year == year1:

            # Iterate through regions in super dictionary
            for region in superD[year]:

                # Iterate through counties in super dictionary
                for country in superD[year][region]:

                    # Get list of countries
                    country_list.append((country, int(superD[year][region][country][0][0])))

            # Sort country list
            country_list.sort(key=itemgetter(1))

            # Get top 10 countries
            for i in range(10):

                year1_list.append(country_list[i])

            # Reset country list
            country_list = []

        # Search for second year
        elif year == year2:

            # Make deep copy of year 1 list
            year2_list_of_tuples = copy.deepcopy(year1_list)

            for l in range(10):

                country_list.append(year1_list[l][0])
                year2_list.append(list(year2_list_of_tuples[l]))

            # Iterate through regions in super dictionary
            for region in superD[year]:

                # Iterate through countries in super dictionary
                for country in superD[year][region]:

                    # If country found, append tuple to list
                    if country in country_list:

                        year2_rank.append((country, (int(superD[year][region][country][0][0]))))

            # Change happiness rank in year 2
            for j in range(10):

                for k in range(10):

                    if year2_list[j][0] == year2_rank[k][0]:

                        year2_list[j][1] = year2_rank[k][1]

            # Reformat year 2 list
            for m in range(10):

                year2_list[m] = tuple(year2_list[m])

    # return year 1 and year 2 list
    return year1_list, year2_list


def print_ranks(superD, list1, list2, year1, year2):
    ''' This function simply displays the data returned by the function above with the correct
formatting. The two lists are the two lists returned by top_10_ranks_across_years; the
int parameters are the years of the lists respectively.  '''

    print('{:<15s} {:>7s} {:>7s} {:>12s}'.format('Country', year1, year2, 'Avg.H.Score'))

    for i in range(10):

        years_data = search_by_country(list1[i][0], superD, False)
        year1_H_score = years_data[0][0]
        year2_H_score = years_data[1][0]
        avg_H_score = ((year1_H_score + year2_H_score) / 2)
        print('{:<15s} {:>7d} {:>7d} {:>12.2f}'.format(list1[i][0], list1[i][1], list2[i][1], avg_H_score))


def prepare_plot(country1, country2, superD):
    ''' This function takes the names of the two countries and the super dictionary and returns 2 tuples. '''

    got_data = False

    for year in superD:

        # When required data obtained, exit loop
        if got_data:
            break

        for region in superD[year]:

            for country in superD[year][region]:

                if country == country1:

                    country1_data = (float(superD[year][region][country][0][1]), \
                                     float(superD[year][region][country][2][0]), \
                                     float(superD[year][region][country][2][1]), \
                                     float(superD[year][region][country][2][2]))

                elif country == country2:

                    country2_data = (float(superD[year][region][country][0][1]), \
                                     float(superD[year][region][country][2][0]), \
                                     float(superD[year][region][country][2][1]), \
                                     float(superD[year][region][country][2][2]))

                got_data = True

    return country1_data, country2_data

def bar_plot(country1, country2, countrylist1, countrylist2):
    ''' Bar plot comparing two countries.'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    N = 4
    ind = np.arange(N)
    width = 0.25

    rects1 = ax.bar(ind, countrylist1, width,
                    color='black',
                    error_kw=dict(elinewidth=2, ecolor='blue'))

    rects2 = ax.bar(ind + width, countrylist2, width,
                    color='red',
                    error_kw=dict(elinewidth=2, ecolor='red'))

    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylabel('Quantity')
    ax.set_title('Comparison between the two countries')
    xTickMarks = ['Happiness Sc.', 'Family', 'Health', 'Freedom']
    ax.set_xticks(ind + width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=10)

    ax.legend((rects1[0], rects2[0]), (country1, country2))
    plt.show()


def main():
    ''' Docstring '''

    BANNER = '''
                    __ooooooooo__
                 oOOOOOOOOOOOOOOOOOOOOOo
             oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
          oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
        oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
      oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
     oOOOOOOOOOOO*  *OOOOOOOOOOOOOO*  *OOOOOOOOOOOOo
    oOOOOOOOOOOO      OOOOOOOOOOOO      OOOOOOOOOOOOo
    oOOOOOOOOOOOOo  oOOOOOOOOOOOOOOo  oOOOOOOOOOOOOOo
    oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
    oOOOO     OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO     OOOOo
    oOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOOOOo
    *OOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  OOOOO*
    *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
     *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
      *OOOOOOo  *OOOOOOOOOOOOOOOOOOOOOOO*  oOOOOOO*
        *OOOOOOOo  *OOOOOOOOOOOOOOOOO*  oOOOOOOO*
          *OOOOOOOOo  *OOOOOOOOOOO*  oOOOOOOOO*      
             *OOOOOOOOo           oOOOOOOOO*      
                 *OOOOOOOOOOOOOOOOOOOOO*    
                      ""ooooooooo""
    '''

    MENU = '''
    1. Search by country
    2. Top 10 countries
    3. Compare countries
    x. Exit 
    :'''
    print(BANNER)

    superD = {}

    years = input("Input Years comma-separated as A,B: ")
    years = years.split(',')
    year1_fp = open_file(years[0])
    year2_fp = open_file(years[1])
    year1_dict = build_dictionary(year1_fp)
    year2_dict = build_dictionary(year2_fp)
    combine_dictionaries(years[0], year1_dict, superD)
    combine_dictionaries(years[1], year2_dict, superD)

    while True:

        user_choice = input(MENU)

        if user_choice == 'x':

            break

        elif user_choice == '1':

            country_name = input("[ ? ] Please specify the country: ")
            print()
            search_by_country(country_name, superD, True)

        elif user_choice == '2':

            print()
            year1_top_10, year2_top_10 = top_10_ranks_across_years(superD, years[0], years[1])
            print_ranks(superD, year1_top_10, year2_top_10, years[0], years[1])

        elif user_choice == '3':

            country1_found = False
            country2_found = False
            break_loop = False

            while True:

                # Exit loop if both countries found
                if break_loop:
                    break

                countries = input("[ ? ] Please specify the two countries (A,B): ")
                countries_list = countries.split(',')

                # Iterate through years in super dictionary
                for year in superD:

                    # Iterate through regions in super dictionary
                    for region in superD[year]:

                        # Iterate through countries in super dictionary
                        for country in superD[year][region]:

                            if country == countries_list[0]:

                                country1_found = True

                            elif country == countries_list[1]:

                                country2_found = True

                    if country1_found and country2_found:

                        break_loop = True

                    else:

                        print("[ - ] Incorrect input. Try again.")

            print("{:<20s} {:<9s} {:<8s} {:<8s} {:<8s}".format("\nCountry", "Hap.Score", "Family", "Life Ex." \
                                                               , "Freedom"))

            country1_data, country2_data = prepare_plot(countries_list[0], countries_list[1], superD)

            print("{:<20s} {:<9.2f} {:<8.2f} {:<8.2f} {:<8.2f}".format(countries_list[0], country1_data[0], \
                                                                       country1_data[1], country1_data[2], \
                                                                       country1_data[3]))
            print("{:<20s} {:<9.2f} {:<8.2f} {:<8.2f} {:<8.2f}".format(countries_list[1], country2_data[0], \
                                                                       country2_data[1], country2_data[2], \
                                                                       country2_data[3]))

            plot = input("[ ? ] Plot (y/n)? ")

            if plot.lower() == 'y':

                bar_plot(countries_list[0], countries_list[1], country1_data, country2_data)

            else:

                continue

        else:

            print("\nInvalid input. Try again.")


if __name__ == '__main__':
    main()
