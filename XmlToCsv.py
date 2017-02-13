import urllib2
import xml.etree.ElementTree
import pandas
import os

def parse_xml(url):
    """
    Parse given XML feed for the fields needed
    :param url: XML feed to parse
    :return:
    """
    # Open the URL to retrieve a file like handle to the data
    # TODO: Add error handling if the URL cannot be requested
    xml_feed_file = urllib2.urlopen(url)

    # Convert the contents of the file like handle to a string
    # Get all the data by using .read() of the file like handle
    xml_data = xml_feed_file.read()

    # Clean up by closing the file like handle as we do not need it anymore
    xml_feed_file.close()

    # Create an ElementTree object so the XML can be parsed
    xml_etree = xml.etree.ElementTree.fromstring(xml_data)

    # Find all instances of necesscary elements
    # The following elements require no special handling and findall can be used
    # findall finds all instances of an element by path or tag bane in document order
    # MlsId
    # MlsName
    # DateListed
    # StreetAddress
    # Price
    # Bedrooms
    # Bathrooms
    # Description
    all_elements = xml_etree.findall('.//MlsId')
    all_elements.extend(xml_etree.findall('.//MlsName'))
    all_elements.extend(xml_etree.findall('.//DateListed'))
    all_elements.extend(xml_etree.findall('.//Location//StreetAddress'))
    all_elements.extend(xml_etree.findall('.//Price'))
    all_elements.extend(xml_etree.findall('.//Bedrooms'))
    all_elements.extend(xml_etree.findall('.//FullBathrooms'))
    all_elements.extend(xml_etree.findall('.//HalfBathrooms'))
    all_elements.extend(xml_etree.findall('.//ThreeQuarterBathrooms'))
    all_elements.extend(xml_etree.findall('.//BasicDetails//Description'))

    # Declare dictionary that will map elements to their tags
    element_dict = {}

    # Go through all the above elements
    for element in all_elements:
        # Map the element tag to the text value
        element_dict.setdefault(element.tag, []).append(element.text)

    # The following elements require special handling
    # Appliances
    # Rooms
    # Need to be added as lists to the dictionary as sub-nodes need be comma joined
    # Appliances and Rooms are sub-nodes of RichDetails so findall RichDetails
    all_elements = xml_etree.findall('.//RichDetails')

    # Create a list of sub-nodes to loop over
    sub_nodes = ['Appliances', 'Rooms']

    for element in all_elements:
        for sub_node in sub_nodes:
            # Declare an empty list that will contain all children of the sub-nodes
            children = []
            # Check if the element is None
            if element.find(sub_node) is None:
                # If it is, append empty list
                element_dict.setdefault(sub_node, []).append([])
            else:
                # Iterate through all children
                for child in element.find('{xpath}{sub_node_tag}'.format(xpath = './/', sub_node_tag = sub_node)).iter():
                    # Check if the text is not none
                    if child.text is not None:
                        # Strip any space or newline characters if the text is not none
                        children.append(str(child.text).strip())
                # Filter out empty strings
                children = filter(None, children)
                # Add the list to the dictionary mapping the tag to the list
                element_dict.setdefault(sub_node, []).append(children)

    return element_dict

def create_data_frame(dictionary):
    """
    Create dataframe from dictionary of needed XML elements
    :param dictionary: Dictioary of needed XML elements
    :return:
    """
    # Convert the dictionary to dataframe
    return pandas.DataFrame(dictionary)

def manipulate_data_frame(data_frame):
    """
    Manipulate dataframe to abide by csv requirements
    :param data_frame: Dataframe of needed XML elements
    :return:
    """

    # Limit to the listings that only contain and in the description field
    description_contains_and = data_frame['Description'].str.contains('and')
    data_frame = data_frame[description_contains_and]

    # Limit the description field to 200 characters
    # Filtering on and then 200 characters could potentially make it seem like the above filter did not work
    # TODO: Figure out if spaces count as characters
    # TODO: Fix warnings but not necesscary as original Dataframe is being overwritten each time so it does not matter if copy or view is returnedi
    # Seem to be false positive warnings based on reading this http://pandas-docs.github.io/pandas-docs-travis/indexing.html
    data_frame['Description'] = data_frame['Description'].str[:200]

    # Make rooms a comma separated list
    data_frame['Rooms'] = data_frame['Rooms'].apply(','.join)

    # Make appliances a comma separated list
    data_frame['Appliances'] = data_frame['Appliances'].apply(','.join)

    # Make listings from only 2016 display
    date = data_frame['DateListed'] >= '2016-01-01'
    data_frame = data_frame[date]

    return data_frame

def output_to_csv(data_frame):
    """
    Output dataframe to csv
    :param data_frame: Dataframe to output to csv
    :return:
    """

    # Get current working directory
    cwd = os.getcwd()

    # Print columns to current working directory
    # Remove numbered index
    # TODO: Change where the file is written to where it needs to go
    data_frame.to_csv('{current_working_dir}/{filename}'.format(current_working_dir = cwd, filename = 'listing.csv'), index=False)

def main():
    """
    Generate a csv with the necesscary columns for http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml
    :return:
    """
    URL = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    output_to_csv(manipulate_data_frame(create_data_frame(parse_xml(URL))))


if __name__ == '__main__':
    main()
