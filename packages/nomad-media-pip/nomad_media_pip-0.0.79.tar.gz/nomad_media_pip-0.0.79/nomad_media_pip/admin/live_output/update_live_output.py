from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.admin.live_output.get_output_types import _get_output_types

import requests, json

def _update_live_output(AUTH_TOKEN, URL, ID, NAME, OUTPUT_TYPE, ENABLED, AUDIO_BITRATE,
                        OUTPUT_STREAM_KEY, OUTPUT_URL, SECONDARY_OUTPUT_STREAM_KEY,
                        SECONDARY_OUTPUT_URL, VIDEO_BITRATE, VIDEO_BITRATE_MODE,
                        VIDEO_CODEC, VIDEO_FRAMES_PER_SECOND, VIDEO_HEIGHT, VIDEO_WIDTH,
                        DEBUG):

    API_URL = f"{URL}/liveOutputProfile"

    HEADERS = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer " + AUTH_TOKEN
    }

    OUTPUT_TYPES = _get_output_types(AUTH_TOKEN, URL, DEBUG)
    OUTPUT_TYPE_OBJECT = next((item for item in OUTPUT_TYPES if item["description"] == OUTPUT_TYPE), None)

    BODY = {
        "id": ID,
        "name": NAME,
        "outputType": OUTPUT_TYPE_OBJECT,
        "enabled": ENABLED,
        "audioBitrate": AUDIO_BITRATE,
        "outputStreamKey": OUTPUT_STREAM_KEY,
        "outputUrl": OUTPUT_URL,
        "secondaryOutputStreamKey": SECONDARY_OUTPUT_STREAM_KEY,
        "secondaryOutputUrl": SECONDARY_OUTPUT_URL,
        "videoBitrate": VIDEO_BITRATE,
        "videoBitrateMode": VIDEO_BITRATE_MODE,
        "videoCodec": VIDEO_CODEC,
        "videoFramesPerSecond": VIDEO_FRAMES_PER_SECOND,
        "videoHeight": VIDEO_HEIGHT,
        "videoWidth": VIDEO_WIDTH
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: PUT,\nBODY: {json.dumps(BODY)}")

    try:
        RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Update Live Output Failed")