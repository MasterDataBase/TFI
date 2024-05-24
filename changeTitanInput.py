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

def get_decode_list(address_machine):
    # address_machine = '10.130.104.12' 
    base_url = f'http://{address_machine}/decoder/api/channels'
    suffix_url = "/configuration"
    # api_url = f"{base_url}{1}{suffix_url}"    
    api_url = f"{base_url}"    
    print(api_url)
    result = get_json_from_api(api_url)
    dec = list()
    for x in result:
        # dec.append(x['configuration']['name'])
        dec.append(Decoder(name=x['configuration']['name'], id=x['id']))
    return dec

def check_decod_to_set(decoders, listDec): 
    targets = list()
    
    if(listDec[0] != -1):
        for f in listDec:
            for j in decoders:
                if(str(f) == str(j.id)):
                    targets.append(j)
    else: 
        for f in decoders: 
            targets.append(f)
    
    return targets


class Decoder: 
    def __init__(self, name, id):
        self.name = name
        self.id = id

# Main process
# Load JSON data from the files
with open('DecoderToChange.json', 'r') as file_a:
    templateDec = json.load(file_a)

# Example usage:
address_machine = templateDec['address']
base_url = f'http://{address_machine}/decoder/api/channels/'
suffix_url = "/configuration"
decoders = get_decode_list(address_machine)

listDecoders = list()

try:
    listDecoders = templateDec['target']
except:
    print("targets not provided, entire titan decoders will be update")
    listDecoders.append(-1)

decoders = check_decod_to_set(decoders=decoders, listDec=listDecoders)

if not decoders: 
    with open('result' + '.json', 'w') as file_a:
        json.dump("not found any decoder based on the list provided", file_a, indent=2)     
else:
    # Dynamic value
    for x in decoders:
        # xIndex = str(decoders.index(x)+1)
        
        api_url = f"{base_url}{x.id}{suffix_url}"
        # Debug
        # print(str(x.name) + ": " + str(decoders.index(x.id)+1))
        
        json_data = get_json_from_api(api_url)
        # Debug
        print("start process for -> " + str(json_data['name']))
        
        # Update dec config
        newConfig = UpdateDecoderInput(json_data, templateDec)
        
        # Write the modified data back to json_a.json
        with open(str(json_data['name']) + '.json', 'w') as file_a:
            json.dump(newConfig, file_a, indent=2) 
        # api_url = f'{base_url}{x}{suffix_url}'
        if templateDec['debug'] == True:
            print(f"Completed print file -> " + str(newConfig['name']))
        else:
            response = put_config_decoder(api_url, newConfig)
            print(f"Completed update on -> " + str(newConfig['name']))