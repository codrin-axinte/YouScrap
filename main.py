import requests
from bs4 import BeautifulSoup
import csv

# Path to file from where to get the URLs
db_path = 'database.csv'
# The output path where the subscribers should be written
out_path = 'output.txt'


# This function searches in the html source
# for the button's class (yt-subscription-button-subscriber-count-branded-horizontal)
# to get the actual subscribers text/value
# This must be hardcoded and you must manually search for it in the source code for each website
# or piece of information you want to scrape
def get_subscribers(soup):
    data = soup.select('.yt-subscription-button-subscriber-count-branded-horizontal')
    if len(data) > 0:
        return data[0].text
    else:
        return 'N/A'


# This functions makes a request to the given url
# and uses BeautifulSoup to parse the html source code
def get_channel(url):
    # Check if the url is empty or a '-' (dash) and return N/A if so
    if url == '-' or url == '':
        return 'N/A'
    # Makes the request to the url, verify=True it enables ssl verification which meas secure sockets layer.
    # Basically encrypts the communication between the application and the website
    result = requests.get(url, verify=True)
    # result.text is the raw source of the response/website
    soup = BeautifulSoup(result.text, 'html.parser')
    return get_subscribers(soup)


# Before fetching subscribers, we use this function to make a list of the urls from the database file
def get_links(database_path):
    # Some feedback for to user
    print('Getting urls...')
    # Prepare the array
    links = []
    # Open the file at the specified path using the utf8 encoding to support any special characters
    with open(database_path, encoding="utf8") as csv_file:
        # using th csv library we can read/parse the csv file correctly
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # We loop through each line of the file and append only the Url
        # which is the second column in this csv file
        for row in csv_reader:
            # Here whe check if this is the first iteration or the first row,
            # if so, we do nothing, otherwise we append the url to the links array defined above
            if line_count > 0:
                links.append(row[1])
            # increment the line count
            line_count += 1
        # A feedback for the user to know how many results should expect at the end.
        print(f'Processed {line_count} urls.')
    # Return the array of urls
    return links


# This function is doing the actual scraping by going through each link in the array,
# and calling the get_channel function to fetch the subscribers number
def fetch_subs(links):
    # Feedback for the user to announce him that scraping has started
    print("Start scraping...")
    # Preparing a list of subs
    subs = []
    # Looping through each link in the array
    for link in links:
        # Append the subscribers value to the list
        subs.append(get_channel(link))
    # feedback for the user that scraping has ended
    print("Done!")
    # Return the subs
    return subs


# Write the subscribers to a file
def write_subs(output_path, subscribers):
    # Feedback the user that the writing has started
    print('Writing subscribers...')
    # Open the file at the output path in the write mode (mode='w')
    with open(output_path, mode='w') as output:
        # Iterate through each line
        for row in subscribers:
            # Write to file the value concatenated by a new line ('\n')
            output.write(row + '\n')
    # Feedback the user that the writing has finished by providing him the path where the data was written
    print('File written at path ' + output_path)


# Small feedback to show that the application started
print('Work, work')
# Calling the needed functions defined above
write_subs(out_path, fetch_subs(get_links(db_path)))
# Feedback the user that everything has finished and he can enjoy his list
print('Jobs Done!')