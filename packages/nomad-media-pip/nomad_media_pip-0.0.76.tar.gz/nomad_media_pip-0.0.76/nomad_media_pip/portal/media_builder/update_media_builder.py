from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.portal.media_builder.get_media_builder import _get_media_builder

import requests, json

def _update_media_builder(AUTH_TOKEN, URL, ID, NAME, DESTINATION_FOLDER_ID, COLLECTIONS,
                          RELATED_CONTENT, PROPERTIES, DEBUG):
    
    API_URL = f"{URL}/mediaBuilder/{ID}"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    INFO = _get_media_builder(AUTH_TOKEN, URL, ID, DEBUG)

    BODY = {
        "name": NAME or INFO.get("name"),
        "destinationFolderId": DESTINATION_FOLDER_ID or INFO.get("destinationFolderId"),
        "collections": COLLECTIONS or INFO.get("collections"),
        "relatedContent": RELATED_CONTENT or INFO.get("relatedContent"),
        "properties": PROPERTIES or INFO.get("properties")
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: PUT,\nBODY: {json.dumps(BODY)}")

    try:
        RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()

        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Update Media Builder Failed")