import requests
import json

def get_json_from_api(url):
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON data
            return response.json()
        else:
            # If the request was unsuccessful, print the error message
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def put_config_decoder(url, jsonBody):
    try:
        response = requests.put(url, json=jsonBody)
        if response.status_code == 200:
            return response.json()
        else:
            # If the request was unsuccessful, print the error message
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None            

def UpdateDecoderInput(baseDec, inputDec):
    # Merge nodes from json_b into json_a
    baseDec['source'] = inputDec['source']
    baseDec['composition'] = inputDec['composition']
    # Add more lines for additional nodes to merge
    return baseDec

# Load JSON data from the files
with open('DecoderToChange.json', 'r') as file_a:
    templateDec = json.load(file_a)

# Example usage:
address_machine = templateDec['address']
base_url = f'http://{address_machine}/decoder/api/channels/'
suffix_url = "/configuration"
# Dynamic value
for x in range(1,9):
    api_url = f"{base_url}{x}{suffix_url}"
    json_data = get_json_from_api(api_url)
    # Debug
    print("start process for -> " + str(json_data['name']))
    
    # Update dec config
    newConfig = UpdateDecoderInput(json_data, templateDec)
    
    # Write the modified data back to json_a.json
    with open(str(json_data['name']) + '.json', 'w') as file_a:
        json.dump(newConfig, file_a, indent=2) 
    api_url = f'{base_url}{x}{suffix_url}'
    if templateDec['debug'] == True:
        response = put_config_decoder(api_url, newConfig)
        print(f"Completed print file -> " + str(newConfig['name']))
    else:
        print(f"Completed update on -> " + str(newConfig['name']))