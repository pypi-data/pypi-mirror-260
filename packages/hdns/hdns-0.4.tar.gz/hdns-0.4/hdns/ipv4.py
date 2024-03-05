import requests

def get_ipv4():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve public IPv4 address: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to retrieve public IPv4 address: {e}")
        return None

