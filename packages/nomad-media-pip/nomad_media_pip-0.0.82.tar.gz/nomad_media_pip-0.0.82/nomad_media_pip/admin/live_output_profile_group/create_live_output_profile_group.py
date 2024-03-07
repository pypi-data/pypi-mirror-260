from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _create_live_output_profile_group(AUTH_TOKEN, URL, NAME, IS_ENABLED, MANIFEST_TYPE, IS_DEFAULT_GROUP, LIVE_OUTPUT_TYPE, ARCHIVE_LIVE_OUTPUT_PROFILE, LIVE_OUTPUT_PROFILES, DEBUG):

	API_URL = f"{URL}/liveOutputProfileGroup"

	HEADERS = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {AUTH_TOKEN}"
	}

	BODY = {
		"name": NAME,
		"isEnabled": IS_ENABLED,
		"manifestType": MANIFEST_TYPE,
		"isDefaultGroup": IS_DEFAULT_GROUP,
		"liveOutputType": LIVE_OUTPUT_TYPE,
		"archiveLiveOutputProfile": ARCHIVE_LIVE_OUTPUT_PROFILE,
		"liveOutputProfiles": LIVE_OUTPUT_PROFILES
	}
	if DEBUG:
		print(f"API_URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY)}")

	try:
		RESPONSE = requests.post(API_URL, headers=HEADERS, data=json.dumps(BODY))

		if not RESPONSE.ok:
			raise Exception()

		return RESPONSE.json()
	except:
		_api_exception_handler(RESPONSE, "Create Live Output Profile Group Failed")