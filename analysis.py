import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import chi2_contingency
'''
TODO: 
Segment into week or month groups
1. Graph the posts over time for: everyone, each group, each group except focus group individually. Make a basic Correlation value (maybe R^2)
2. Do the same graph except for post*length of video
3. Do the same graph except for views
4. Gragh post*length*(view_count+like_count+comment_count+favorite_count) over time for the same groups. Run a R^2 here too. 

5. Now add in the shootings. Add a dotted line to each graph for where the shootings are located.
6. Create a df with the shootings dates, and then convert it into a binary if shootings occured at the start of that week or not.
7. Segment the youtuber data into week-long time units
8. Perform Phi coeffieicnet correlation test on this. correlation, _ = pointbiserialr(df['Shootings'], df['Week_posts'])
print("Point-Biserial Correlation:", correlation)
9. Make a Cross Tab chart and perform a Chi Sqauared test
# Crosstab and Chi-Square Test
crosstab = pd.crosstab(df['RareVariable'], df['Frequency'])
chi2, p, _, _ = chi2_contingency(crosstab)
print("Chi-Square p-value:", p)
10. Do the same correlation adn cross tabs with controls for the weighted views, and then accounting for the engagment sum, and then both together. 
'''


# Returns total number of minutes for video duration string, e.g. PT6M17S -> 6:17 -> 377 seconds -> minutes
def parse_video_duration(duration_string):
    assert duration_string.startswith('P'), f'{duration_string}'
    duration_string = duration_string[1:]
    total_seconds = 0
    if 'D' in duration_string:
        days, _, duration_string = duration_string.partition('D')
        total_seconds += 24 * 60 * 60 * int(days)
    _, _, duration_string = duration_string.partition('T')
    if 'H' in duration_string:
        hours, _, duration_string = duration_string.partition('H')
        total_seconds += 60 * 60 * int(hours)
    if 'M' in duration_string:
        minutes, _, duration_string = duration_string.partition('M')
        total_seconds += 60 * int(minutes)
    if 'S' in duration_string:
        total_seconds += int(duration_string.partition('S')[0])
    return min(total_seconds / 60, 60)


# interval = 'day'/'week'/'month', returns list of dates spaced by that interval
def get_date_ranges(interval):
    if interval == 'month':
        dates = [datetime(year, month, 1) for year in range(2016, 2025) for month in range(1, 13)]
    else:
        dates = [datetime(2016, 1, 1)] if interval == 'day' else [datetime(2015, 12, 27)]
        td = timedelta(days=(1 if interval == 'day' else 7))
        while dates[-1] < LAST_DATE:
            dates.append(dates[-1] + td)
    return [date for date in dates if date < LAST_DATE]


def get_date_index(date, date_ranges):
    for i in range(len(date_ranges)):
        if date < date_ranges[i]:
            return i - 1
    return len(date_ranges) - 1


def parse_csvs(csv_files, date_ranges):
    results = [[0, 0, 0, 0] for _ in date_ranges]
    for file in csv_files:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            week = get_date_index(datetime.fromisoformat(row['Published At'][:-1]), date_ranges)
            if week < 0:
                continue
            results[week][0] += 1
            results[week][1] += parse_video_duration(row['Duration'])
            results[week][2] += row['View Count']
            results[week][3] += (row['View Count'] + row['Like Count'] + row['Comment Count'] + row['Favorite Count']) * parse_video_duration(row['Duration'])
    return pd.DataFrame([[date, *(x/len(csv_files) for x in r)] for date, r in zip(date_ranges, results)],
                        columns=['Start Date', 'Total Posts', 'Total Video Minutes', 'Total Views', 'Total Interactions * Duration'])

# ben vs cintrol. Less crodwed grpahs. 
# shooting dotted vertical lines
# rleative change. Divide by last 6 months


# Column should be one of 'Start Date', 'Total Posts', 'Total Video Minutes', 'Total Views', 'Total Interactions * Duration'
def create_graph(name, groups, interval='week', column='Total Posts', add_shootings=False):
    x = get_date_ranges(interval)
    for group_name, group_files in groups.items():
        y = parse_csvs(group_files, x)[column]
        plt.plot(x, y, label=group_name)
    if add_shootings:
        y = [0] * len(x)
        for date, _, _, _, casualties in shootings:
            i = get_date_index(datetime.strptime(date, '%Y-%m-%d'), x)
            if casualties >= 10:
                y[i] += 1
        plt.plot(x, y, label='Shooting casualties')
    plt.title(name)
    plt.legend()
    plt.show()

# Function to calculate post frequency per week
def calculate_post_frequency(csv_files, date_ranges):
    results = [[date, 0] for date in date_ranges]
    for file in csv_files:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            week = get_date_index(datetime.fromisoformat(row['Published At'][:-1]), date_ranges)
            if week < 0:
                continue
            results[week][1] += 1
    df = pd.DataFrame(results, columns=['Start Date', 'Num Posts'])
    df['Num Posts'] = round(df['Num Posts']/len(csv_files))
    # Gives average post frequency (dvided by number of channels in the group)
    return df

def calculate_shooting_frequency(date_ranges):
    results = [[date, 0, '', 0, 0, 0] for date in date_ranges]
    # [num_shootings_inweek, list of locations, total deaths, total injuries, total casualties]
    for date, location, deaths, injuries, total_casualties in shootings:
        i = get_date_index(datetime.strptime(date, '%Y-%m-%d'), date_ranges)
        results[i][1] += 1
        results[i][2] += f'{location}\n'
        results[i][3] += deaths
        results[i][4] += injuries
        results[i][5] += total_casualties
    return pd.DataFrame(results, columns=['Start Date', 'Num Shootings', 'Locations', 'Total deaths', 'Total Injuries', 'Total Casualties'])


# Function to create a crosstab and perform a Chi-Square test
def create_crosstab(df, v1, v2):
    crosstab = pd.crosstab(df[v1], df[v2])
    chi2, p, _, _ = chi2_contingency(crosstab)
    print("Chi-Square p-value:", p)
    return crosstab


LAST_DATE = datetime(2024, 2, 22)
BASE_FOLDER = Path(__file__).parent
FOLDERS = [BASE_FOLDER / 'Conservative_Focus_Group',
           BASE_FOLDER / 'Con_news',
           BASE_FOLDER / 'Con_vid_essays',
           BASE_FOLDER / 'Controls',
           BASE_FOLDER / 'Lib_essays',
           BASE_FOLDER / 'Lib_news', 
           BASE_FOLDER / 'Libs',
           BASE_FOLDER / 'Cons']
GROUPS_INDIVIDUAL = {file.name.partition('_')[0]: [file] for folder in FOLDERS for file in folder.iterdir()}
GROUPS_FOCUS = {**{file.name.partition('_')[0]: [file] for file in FOLDERS[0].iterdir()},
                **{folder.name: list(folder.iterdir()) for folder in FOLDERS[1:]}}
GROUPS_ALL = {folder.name: list(folder.iterdir()) for folder in FOLDERS}

JUST_SHAPIRO = {'Shapiro': [BASE_FOLDER / 'Conservative_Focus_Group' / 'ben_shapiro_videos.csv'],
                'Lib_essays': list((BASE_FOLDER / 'Lib_essays').iterdir()),
                'Lib_news': list((BASE_FOLDER / 'Lib_news').iterdir())}

# 2020-04-28T20:00:17Z,
# PT6M17S  --> period of time, 6 minutes, 17 seconds

# [(date, location, deaths, injuries, total casualties)]
shootings = [
    # 2024
    # ("2024-02-18", "Burnsville, Minnesota", 4, 1, 5),
    ("2024-02-14", "Kansas City, Missouri", 1, 40, 41),
    ("2024-02-11", "Los Angeles County, California", 4, 1, 5), # two days
    ("2024-02-07", "East Lansdowne, Pennsylvania", 6, 2, 8),
    ("2024-01-21", "Joliet, Illinois", 9, 1, 10), # two days
    ("2024-01-04", "Perry, Iowa", 3, 6, 9),

    # 2023
    ("2023-12-06", "Paradise, Nevada", 4, 3, 7),
    ("2023-12-05", "Austin, Texas/Bexar County, Texas", 6, 3, 9),
    ("2023-10-29", "Tampa, Florida", 2, 16, 18),
    ("2023-10-25", "Lewiston, Maine", 19, 13, 32),
    ("2023-08-26", "Jacksonville, Florida", 4, 0, 4),
    ("2023-08-23", "Trabuco Canyon, California", 4, 6, 10),
    ("2023-07-14", "Fargo, North Dakota", 2, 3, 5),
    ("2023-07-03", "Philadelphia, Pennsylvania", 5, 2, 7),
    ("2023-07-02", "Baltimore, Maryland", 2, 28, 30),
    ("2023-06-15", "Monroe Township, Ohio", 3, 1, 4),
    ("2023-06-06", "Richmond, Virginia", 2, 5, 7),
    ("2023-05-15", "Farmington, New Mexico", 4, 6, 10),
    ("2023-05-06", "Allen, Texas", 9, 7, 16),
    ("2023-05-03", "Atlanta, Georgia", 1, 4, 5),
    ("2023-05-01", "Henryetta, Oklahoma", 7, 0, 7),
    ("2023-04-28", "Cleveland, Texas", 5, 0, 5),
    ("2023-04-18", "Bowdoin and Yarmouth, Maine", 4, 3, 7),
    ("2023-04-15", "Dadeville, Alabama", 4, 32, 36),
    ("2023-04-10", "Louisville, Kentucky", 6, 8, 14),
    ("2023-03-27", "Nashville, Tennessee", 7, 1, 8),
    ("2023-02-22", "Pine Hills, Florida", 3, 2, 5),
    ("2023-02-13", "East Lansing, Michigan", 4, 5, 9),
    ("2023-01-28", "Los Angeles, California", 3, 4, 7),
    ("2023-01-23", "Half Moon Bay, California", 7, 1, 8),
    ("2023-01-21", "Monterey Park, California", 12, 9, 21),
    ("2023-01-16", "Goshen, California", 6, 0, 6),
    ("2023-01-04", "Enoch, Utah", 8, 0, 8),

    # 2022
    ("2022-11-22", "Chesapeake, Virginia", 7, 4, 11),
    ("2022-11-19", "Colorado Springs, Colorado", 5, 26, 31), #two days
    ("2022-11-13", "Charlottesville, Virginia", 3, 2, 5),
    ("2022-10-24", "St. Louis, Missouri", 3, 7, 10),
    ("2022-10-13", "Raleigh, North Carolina", 5, 2, 7),
    ("2022-09-28", "Oakland, California", 1, 5, 6),
    ("2022-08-28", "Bend, Oregon", 3, 2, 5),
    ("2022-07-26", "Fairbanks, Alaska", 4, 0, 4),
    ("2022-07-17", "Denver, Colorado", 0, 7, 7),
    ("2022-07-17", "Greenwood, Indiana", 4, 2, 6),
    ("2022-07-04", "Highland Park, Illinois", 7, 48, 55),
    ("2022-06-30", "Allen, Kentucky", 3, 4, 7),
    ("2022-06-05", "Chattanooga, Tennessee", 3, 14, 17),
    ("2022-06-04", "Philadelphia, Pennsylvania", 3, 11, 14),
    ("2022-06-02", "Centerville, Texas/Jourdanton, Texas", 6, 0, 6),
    ("2022-06-01", "Tulsa, Oklahoma", 5, 0, 5),
    ("2022-05-24", "Uvalde, Texas", 22, 18, 40),
    ("2022-05-19", "Chicago, Illinois", 2, 8, 10),
    ("2022-05-15", "Laguna Woods, California", 1, 5, 6),
    ("2022-05-14", "Buffalo, New York", 10, 3, 13),
    ("2022-04-17", "Pittsburgh, Pennsylvania", 2, 13, 15),
    ("2022-04-16", "Columbia, South Carolina", 0, 14, 14),
    ("2022-04-12", "New York City, New York", 0, 29, 29),
    ("2022-04-03", "Sacramento, California", 6, 12, 18),
    ("2022-02-19", "Portland, Oregon", 1, 5, 6),
    
    ("2021-12-27", "Denver/Lakewood, Colorado", 6, 2, 8),
    ("2021-11-30", "Oxford, Michigan", 4, 7, 11),
    ("2021-09-23", "Collierville, Tennessee", 2, 14, 16),
    ("2021-05-30", "Hialeah, Florida", 3, 20, 23),
    ("2021-05-26", "San Jose, California", 10, 0, 10),
    ("2021-04-15", "Indianapolis, Indiana", 9, 7, 16),
    ("2021-04-07", "Rock Hill, South Carolina", 7, 0, 7),
    ("2021-03-31", "Orange, California", 4, 2, 6),
    ("2021-03-22", "Boulder, Colorado", 10, 2, 12),
    ("2021-03-16", "Atlanta and Cherokee County, Georgia", 8, 1, 9),
    ("2021-02-09", "Buffalo, Minnesota", 1, 4, 5),
    ("2021-02-02", "Muskogee, Oklahoma", 6, 1, 7),
    ("2021-02-02", "Sunrise, Florida", 3, 3, 6),
    ("2021-01-09", "Chicago and Evanston, Illinois", 6, 2, 8),
    
    ("2020-12-08", "Williamsburg, West Virginia", 6, 0, 6),
    ("2020-11-20", "Wauwatosa, Wisconsin", 0, 8, 8),
    ("2020-11-03", "Henderson, Nevada", 4, 1, 5),
    ("2020-09-19", "Rochester, New York", 2, 14, 16),
    ("2020-03-15", "Springfield, Missouri", 5, 2, 7),
    ("2020-02-26", "Milwaukee, Wisconsin", 6, 0, 6),
    ("2020-01-17", "Grantsville, Utah", 4, 1, 5),
    
    ("2019-12-10", "Jersey City, New Jersey", 6, 3, 9),
    ("2019-12-06", "Pensacola, Florida", 4, 8, 12),
    ("2019-12-05", "Miramar, Florida", 4, 1, 5),
    ("2019-11-17", "Fresno, California", 4, 6, 10),
    ("2019-11-14", "Santa Clarita, California", 3, 3, 6),
    ("2019-10-31", "Orinda, California", 5, 4, 9),
    ("2019-10-14", "San Juan, Puerto Rico", 6, 0, 6),
    ("2019-08-04", "Dayton, Ohio", 10, 27, 37),
    ("2019-08-03", "El Paso, Texas", 23, 22, 45),
    ("2019-07-28", "Gilroy, California", 4, 15, 19),
    ("2019-05-31", "Virginia Beach, Virginia", 13, 4, 17),
    ("2019-05-07", "Highlands Ranch, Colorado", 1, 8, 9),
    ("2019-04-30", "Charlotte, North Carolina", 2, 4, 6),
    ("2019-04-27", "Poway, California", 1, 3, 4),
    ("2019-02-15", "Aurora, Illinois", 6, 6, 12),
    ("2019-01-28", "Houston, Texas", 2, 5, 7),
    ("2019-01-26", "Ascension and Livingston Parish, Louisiana", 5, 0, 5),
    ("2019-01-23", "Sebring, Florida", 5, 0, 5),
    
    ("2018-11-11", "Globe, Arizona", 3, 1, 4),
    ("2018-11-11", "Robbins, Illinois", 1, 4, 5),
    ("2018-11-07", "Thousand Oaks, California", 13, 16, 29),
    ("2018-11-02", "Tallahassee, Florida", 3, 5, 8),
    ("2018-10-27", "Pittsburgh, Pennsylvania", 11, 7, 18),
    ("2018-10-03", "Florence, South Carolina", 2, 10, 12),
    ("2018-09-20", "Aberdeen, Maryland", 4, 3, 7),
    ("2018-09-06", "Cincinnati, Ohio", 4, 2, 6),
    ("2018-08-26", "Jacksonville, Florida", 3, 11, 14),
    ("2018-06-28", "Annapolis, Maryland", 5, 2, 7),
    ("2018-06-17", "Trenton, New Jersey", 1, 22, 23),
    ("2018-05-30", "Scottsdale, Arizona", 7, 0, 7),
    ("2018-05-18", "Santa Fe, Texas", 10, 14, 24),
    ("2018-04-22", "Nashville, Tennessee", 4, 2, 6),
    ("2018-04-03", "San Bruno, California", 1, 4, 5),
    ("2018-03-09", "Yountville, California", 5, 0, 5),
    ("2018-02-14", "Parkland, Florida", 17, 17, 34),
    ("2018-01-23", "Benton, Kentucky", 2, 16, 18),

    ("2017-12-31", "Highlands Ranch, Colorado", 2, 6, 8),
    ("2017-11-05", "Sutherland Springs, Texas", 27, 22, 49),
    ("2017-10-01", "Paradise, Nevada", 61, 411, 472),
    ("2017-09-24", "Antioch, Tennessee", 1, 8, 9),
    ("2017-09-10", "Plano, Texas", 9, 1, 10),
    ("2017-08-28", "Clovis, New Mexico", 2, 4, 6),
    ("2017-07-01", "Little Rock, Arkansas", 0, 28, 28),
    ("2017-06-30", "New York City, New York", 2, 6, 8),
    ("2017-06-14", "San Francisco, California", 4, 5, 9),
    ("2017-06-14", "Alexandria, Virginia", 1, 6, 7),
    ("2017-06-08", "Eaton Township, Pennsylvania", 4, 0, 4),
    ("2017-06-06", "Sandy, Utah", 3, 2, 5),
    ("2017-06-05", "Orlando, Florida", 6, 0, 6),
    ("2017-05-27", "Lincoln County, Mississippi", 8, 1, 9),
    ("2017-05-12", "Kirkersville, Ohio", 4, 0, 4),
    ("2017-03-26", "Cincinnati, Ohio", 2, 16, 18),
    ("2017-01-06", "Broward County, Florida", 5, 6, 11),

    ("2016-09-28", "Townville, South Carolina", 2, 3, 5),
    ("2016-09-23", "Burlington, Washington", 5, 0, 5),
    ("2016-08-20", "Citronelle, Alabama", 6, 0, 6),
    ("2016-07-30", "Mukilteo, Washington", 3, 1, 4),
    ("2016-07-17", "Baton Rouge, Louisiana", 5, 2, 7),
    ("2016-07-11", "St. Joseph, Michigan", 3, 2, 5),
    ("2016-07-07", "Dallas, Texas", 6, 11, 17),
    ("2016-06-12", "Orlando, Florida", 50, 58, 108),
    ("2016-03-09", "Wilkinsburg, Pennsylvania", 6, 3, 9),
    ("2016-03-07", "Kansas City, Kansas and Montgomery County, Missouri", 5, 0, 5),
    ("2016-02-25", "Hesston and Newton, Kansas", 4, 14, 18),
    ("2016-02-20", "Kalamazoo, Michigan", 6, 2, 8)
]

def group_num_posts(num_posts):
    if num_posts == 0:
        return 0  # '0'
    elif num_posts <= 3:
        return 1  # '1-3'
    elif num_posts <= 6:
        return 4  #  '4-6'
    elif num_posts <= 9:
        return 7  # '7-9'
    elif num_posts <= 20: # 10-20
        return 10
    else: 
        return 21 # '10+'

def get_data(name):
    if name in GROUPS_ALL:
        return GROUPS_ALL[name]
    elif name in GROUPS_INDIVIDUAL:
        return GROUPS_INDIVIDUAL[name]
    else:
        raise KeyError(f'Unknown name/group: {name}')

def main():
    '''
    # TODO: Possibly devide by the average
    create_graph('some title', JUST_SHAPIRO, interval='week', column='Total Posts')
    create_graph('some title', JUST_SHAPIRO, interval='week', column='Total Posts', add_shootings=True)
    # 1. Graph the posts over time for: everyone, each group, each group except focus group individually. Make a basic Correlation value (maybe R^2)
    create_graph("Posts_over_time_individual", GROUPS_INDIVIDUAL, interval='week', column='Total Posts')
    create_graph("Posts_over_time_groups", GROUPS_ALL, interval='week', column='Total Posts')
    create_graph("Posts_over_time_focus", GROUPS_FOCUS, interval='week', column='Total Posts')
    # 2. Do the same graph except for post*length of video
    create_graph("Duration_over_time_individual", GROUPS_INDIVIDUAL, interval='week', column='Total Video Minutes')
    create_graph("Duration_over_time_groups", GROUPS_ALL, interval='week', column='Total Video Minutes')
    create_graph("Duration_over_time_focus", GROUPS_FOCUS, interval='week', column='Total Video Minutes')
    # 3. Do the same graph except for views
    create_graph("Engagement_over_time_individual", GROUPS_INDIVIDUAL, interval='week', column='Total Views')
    create_graph("Engagement_over_time_groups", GROUPS_ALL, interval='week', column='Total Views')
    create_graph("Engagement_over_time_focus", GROUPS_FOCUS, interval='week', column='Total Views')
    # 4. Gragh post*length*(view_count+like_count+comment_count+favorite_count) over time for the same groups. Run a R^2 here too. 
    create_graph("Engagement_over_time_individual", GROUPS_INDIVIDUAL, interval='week', column='Total Interactions * Duration')
    create_graph("Engagement_over_time_groups", GROUPS_ALL, interval='week', column='Total Interactions * Duration')
    create_graph("Engagement_over_time_focus", GROUPS_FOCUS, interval='week', column='Total Interactions * Duration')
    '''

    shootings_df = calculate_shooting_frequency(get_date_ranges('week'))

    # Calculate post frequency per week for shootings
    # ben, CandaceOwens, DailyWire, JordanPeterson
    shootings_week_posts = calculate_post_frequency(get_data('Conservative_Focus_Group'), get_date_ranges('week'))
    combined_df = shootings_df.merge(shootings_week_posts, on='Start Date')
    combined_df['Has Shootings'] = combined_df.apply(lambda row: row['Num Shootings'] >= 1, axis=1)
    combined_df['Grouped Posts'] = combined_df.apply(lambda row: group_num_posts(row['Num Posts']), axis=1)

    # Create a crosstab and perform Chi-Square test
    crosstab = create_crosstab(combined_df, 'Has Shootings', 'Num Posts')
    crosstab = create_crosstab(combined_df, 'Has Shootings', 'Grouped Posts')
    print("Crosstab:")
    print(crosstab)
    # plt.plot(crosstab)
    temp = crosstab.transpose()
    temp[True] /= temp[True].sum()
    temp[False] /= temp[False].sum()
    temp.plot()
    plt.show()
    
    # TODO: Some of the controls have like no videos and thats fucking up the average to make it almost always once per week.
    # TODO: Do this for engament metrics too.

if __name__ == "__main__":
    main()