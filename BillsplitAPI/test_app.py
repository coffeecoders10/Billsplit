import requests

def call_api():
    url = "http://localhost:5000"  # Replace with your actual API endpoint

    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("API responses:", response.text)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.ConnectionError:
        print("Failed to connect to the server. Make sure it's running.")

if __name__ == "__main__":
    call_api()
