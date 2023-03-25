# Import necessary libraries and modules
import argparse # for parsing command line arguments
import requests # for downloading files
import gzip # for working with gzipped files
from collections import defaultdict # for counting files per package

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Get top 10 packages with most files for given architecture')
parser.add_argument('architecture', metavar='ARCH', type=str,
                    help='the architecture to search for (e.g. amd64, arm64, mips)')
args = parser.parse_args()

# Set up the URL for the Contents file based on the provided architecture
url = f'http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{args.architecture}.gz'

# Download and parse the file
response = requests.get(url, stream=True) # send a GET request to the URL to download the file
response.raw.decode_content = True # decode the response content as gzip
contents = gzip.GzipFile(fileobj=response.raw) # open the gzipped file as a file object

# Count the number of files for each package
package_files = defaultdict(int) # create a defaultdict to hold the count of files for each package
for line in contents: # iterate over each line in the file
    parts = line.decode('utf-8').split() # split the line into parts using whitespace as delimiter
    filename = parts[-1] # the last part of the line is the filename
    package_name = parts[0] # the first part of the line is the package name
    package_files[package_name] += 1 # increment the count of files for the package by 1

# Output the top 10 packages with the most number of files
top_packages = sorted(package_files.items(), key=lambda x: x[1], reverse=True)[:10] # sort the dictionary by values and get top 10
print('{:<40}{}'.format('Package Name', 'Number of Files')) # print the header
print('-' * 50) # print a separator line
for package, num_files in top_packages: # iterate over the top packages
    print('{:<40}{}'.format(package, num_files)) # print the package name and the number of files
