from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests

def _get_live_outputs(AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/liveOutputProfile"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: GET")

    try:
        RESPONSE = requests.get(API_URL, headers=HEADERS)
        
        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Get Live Outputs Failed")