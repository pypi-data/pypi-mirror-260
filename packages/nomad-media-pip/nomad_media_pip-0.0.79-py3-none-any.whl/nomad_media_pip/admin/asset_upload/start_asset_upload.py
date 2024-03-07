from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import json, os, requests

def _start_upload(AUTH_TOKEN, URL, NAME, EXISTING_ASSET_ID, RELATED_ASSET_ID, 
                  CREATE_TRANSCRIBE_RELATED_ASSET, RELATED_CONTENT_ID, LANGUAGE_ID, 
                  UPLOAD_OVERWRITE_OPTION, FILE, PARENT_ID, DEBUG):

    API_URL = f"{URL}/asset/upload/start"
    FILE_STATS = os.stat(FILE)


    FILE_NAME = os.path.basename(FILE)

    AWS_MIN_LIMIT = 5242880
    chunkSize = FILE_STATS.st_size / 10000

    if (chunkSize < (AWS_MIN_LIMIT * 4)):
        chunkSize = 20971520
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    # Build the payload BODY
    BODY = {
        "displayName": NAME or FILE_NAME,
      	"contentLength":FILE_STATS.st_size,
      	"uploadOverwriteOption": "replace",
      	"chunkSize": chunkSize,
      	"relativePath": FILE_NAME,
        "parentId":	PARENT_ID,
        "existingAssetId": EXISTING_ASSET_ID,
        "relatedAssetId": RELATED_ASSET_ID,
        "createTranscribeRelatedAsset": CREATE_TRANSCRIBE_RELATED_ASSET,
        "relatedContentId": RELATED_CONTENT_ID,
        "languageId": LANGUAGE_ID,
        "uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        # Send the request
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()

        return RESPONSE.json()

    except:
        _api_exception_handler(RESPONSE, "Start asset upload failed")

