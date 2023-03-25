import argparse
import requests
import gzip
from collections import defaultdict

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Get top 10 packages with most files for given architecture')
parser.add_argument('architecture', metavar='ARCH', type=str,
                    help='the architecture to search for (e.g. amd64, arm64, mips)')
args = parser.parse_args()

# Set up the URL for the Contents file
url = f'http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{args.architecture}.gz'

# Download and parse the file
response = requests.get(url, stream=True)
response.raw.decode_content = True
contents = gzip.GzipFile(fileobj=response.raw)

# Count the number of files for each package
package_files = defaultdict(int)
for line in contents:
    parts = line.decode('utf-8').split()
    filename = parts[-1]
    package_name = parts[0]
    package_files[package_name] += 1

# Output the top 10 packages with the most number of files
top_packages = sorted(package_files.items(), key=lambda x: x[1], reverse=True)[:10]
print('{:<40}{}'.format('Package Name', 'Number of Files'))
print('-' * 50)
for package, num_files in top_packages:
    print('{:<40}{}'.format(package, num_files))
