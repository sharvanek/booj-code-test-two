# booj-code-test-two


Write a script to download and parse the given XML feed, manipulate some of the data, and deliver a CSV of the required fields. You may use any additional libraries that you wish, please include a requirements.txt if you do.

## CSV Requirements:
Contains only properties listed this year (2016) [DateListed]
Contains only properties that contain ‘and’ in the Description field
CSV ordered by DateListed
Required fields:
MlsId
MlsName
DateListed
StreetAddress
Price
Bedrooms
Bathrooms
Appliances (all sub-nodes comma joined)
Rooms (all sub-nodes comma joined)
Description (the first 200 characters)


## Feed url
(to be downloaded by script, do not manually download and locally parse)
http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml


## Details

A lot of the work in our department is parsing and manipulating data from a variety of sources. The given example is one of our XML files that we send to Zillow for property syndication. 

Our goal in this test is to see how you will approach the processing of this feed. Your solution should take into the account that there will be other XML feeds that need parsing as well, so how modular/reusable you make the code is very important. 


## Time considerations

This assignment is expect to take a few hours. We ask that you do not spend too much time on this solution. If you are stuck or have questions, feel free to reach out and we will answer quickly. 

## Running the code
Install all necessary modules found in requirements.txt. Then, download the code and run the following:
```
python XmlToCsv.py
```
A csv file will be generated for http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml and written to the current working directory
