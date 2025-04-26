import requests
import json 

# API trenutno za zdaj samo returna to kar je v queriju, ce je potrebno lahko spremenim

# testing z curl: curl -X POST -H "Content-Type: application/json" -d "{\"query\": \"testing \"}" https://v3adabkxhaqh73hnzr4wroizsy0mbqgr.lambda-url.eu-central-1.on.aws/query

url = "https://v3adabkxhaqh73hnzr4wroizsy0mbqgr.lambda-url.eu-central-1.on.aws/query"


payload = {
    "query": "doc1.pdf"
}


headers = {
    "Content-Type": "application/json"
}

print(f"Sending POST request to: {url}")
print(f"Payload: {json.dumps(payload)}")

try:
    
    response = requests.post(url, headers=headers, json=payload)

    
    response.raise_for_status()


    print(f"Success! Status Code: {response.status_code}")
    try:
        response_data = response.json()


        stored_json_response = response_data


        print("Received JSON response:")
        print(json.dumps(stored_json_response, indent=4))



    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode JSON from response.")
        print(f"Raw response text: {response.text}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response Text: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred during the request: {req_err}")