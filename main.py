# import the necessary modules and libraries
import json, unittest
from datetime import datetime, timezone

# use the open function to open read the three json files
with open("./data-1.json","r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json","r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json","r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)
    
# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):

    # split the location string
    locationParts = jsonObject["location"].split("/")

    # optional safety check
    if len(locationParts) != 5:
        raise ValueError("Invalid location format")

    # create unified format
    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):

    # ✅ FIXED: Proper UTC-safe timestamp conversion
    data = datetime.strptime(jsonObject['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    data = data.replace(tzinfo=timezone.utc)
    timestamp = int(data.timestamp() * 1000)

    # create unified format
    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }

    return result


def main(jsonObject):

    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Test cases using unittest module
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')


if __name__ == '__main__':
    unittest.main()