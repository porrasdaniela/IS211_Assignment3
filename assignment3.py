import argparse
import urllib.request
import csv
import re
from datetime import datetime
from collections import defaultdict

def download_file(url):
    """Download file from a given URL and return the data as a list of strings."""
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8').splitlines()

def process_log(data):
    """Convert the downloaded data into a list of lists using CSV reader."""
    log = csv.reader(data)
    return list(log) #store each row in a list

def find_image_hits(data):
    """Find hits related to images and calculate percentage of total hits."""
    image_pattern = re.compile(r'.*\.(jpg|png|gif)$')
    image_hits = 0
    total_hits = 0

    for row in data:
        total_hits += 1
        if image_pattern.match(row[0]):
            image_hits += 1

    percentage = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Image requests account for {percentage:.2f}% of all requests.")

def most_popular_browser(data):
    """Determine which browser is most popular from the log data."""
    browsers = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    browser_pattern = re.compile(r'(Firefox|Chrome|MSIE|Safari)')

    for row in data:
        match = browser_pattern.search(row[2])
        if match:
            browser = match.group(0)
            if 'MSIE' in browser:
                browsers['Internet Explorer'] += 1
            elif 'Firefox' in browser:
                browsers['Firefox'] += 1
            elif 'Chrome' in browser:
                browsers['Chrome'] += 1
            elif 'Safari' in browser and 'Chrome' not in browser:
                browsers['Safari'] += 1

    most_popular = max(browsers, key=browsers.get)
    print(f"The most popular browser is {most_popular}.")

def hourly_hits(data):
    """Print hits by hour using the datetime module to parse timestamps."""
    hits_by_hour = defaultdict(int)

    for row in data:
        date_time_str = row[1]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        hour = date_time_obj.hour
        hits_by_hour[hour] += 1

    for hour in range(24): # Ensure every hour is printed
        print(f"Hour {hour:02d} has {hits_by_hour[hour]} hits.")

def main(url):
    print(f"Running main with URL = {url}...")

    # Download and process data
    data = download_file(url)
    log_data = process_log(data)

    # Analyze the log data
    find_image_hits(log_data)
    most_popular_browser(log_data)
    hourly_hits(log_data)  # For Extra Credit

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
