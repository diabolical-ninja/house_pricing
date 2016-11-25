import urllib
import time

# Auction Results Location
url = 'http://www.homepriceguide.com.au/saturday_auction_results/Melbourne_Domain.pdf'

# Location to save results
directory = "/Users/yassineltahir/Google Drive/Real Estate Analysis/"

# Get auction results date to use in name
date = time.strftime("%Y%m%d")

# Build file name
name = date + "_melbourne_auction_results.pdf"

# Download file
urllib.urlretrieve(url,directory+name)

