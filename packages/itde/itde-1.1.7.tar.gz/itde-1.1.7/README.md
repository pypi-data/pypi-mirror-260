# InnerTube Data Extractor (ITDE)
![Version](https://img.shields.io/badge/version-1.1.7-blue)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)


ITDE is a Python-based tool designed to extract valuable information, including multimedia content and associated metadata, from the data provided by InnerTube, Google's private API. 
InnerTube serves as a comprehensive source of data, and ITDE empowers developers to seamlessly retrieve and organize essential details from this platform.

### Features

- **Organized Data Structures:**  ITDE organizes extracted data in a structured and typed manner.
- **Versatility:** Designed to handle various types of multimedia content.
- **Python Compatibility:** Written in Python, making it accessible and easy to integrate into existing projects.

### Installation
```shell
pip install itde
```


### Usage
```python
from innertube import InnerTube           # Python Client for Google's Private InnerTube API
from itde import extractor                # Module for extraction

client = InnerTube('WEB_REMIX')           # Construct a client
data = client.search('Squarepusher')      # Get data
extracted_data = extractor.extract(data)  # Extract data.

for shelf in extracted_data.contents:
    print("Shelf")
    print(" ", shelf.name)
    print(" ", shelf.endpoint)
    print(" ", shelf.continuation)
    print(" ", shelf.type)
    
    for item in shelf:
        print("  Item")
        print("  ", item.type)
        print("  ", item.endpoint)
        print("  ", item.name)
        print("  ", item.thumbnail_url)
        print("  ", item.description)  
```

Depending on the type of item, additional data may be present such as release date, view, subscribers, etc.

## Disclaimer

**Note:** ITDE heavily relies on data provided by InnerTube. The reliability and functionality of this code may vary over time, as they are subject to any changes or updates made by InnerTube's data structure or API.

Please keep in mind the following:

- The codebase is designed to adapt to potential changes in InnerTube's data format.
- It's recommended to stay updated with any releases or announcements related to ITDE.

## Status

⚠️ **Work in Progress:** This repository is currently in a state that requires additional development and may not include all intended features. While the core functionality is present, small improvements and additional features are planned for future releases.

Feel free to contribute, report issues, or check back for updates as we continue to enhance and expand ITDE.

Your contributions and feedback are highly appreciated to help maintain and improve the reliability of ITDE.
