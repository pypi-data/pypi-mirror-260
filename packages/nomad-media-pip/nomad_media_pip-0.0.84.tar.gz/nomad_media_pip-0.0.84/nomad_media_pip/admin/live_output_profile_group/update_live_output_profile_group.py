from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _update_live_output_profile_group(AUTH_TOKEN, URL, LIVE_OUTPUT_PROFILE_GROUP_ID, NAME, IS_ENABLED, MANIFEST_TYPE, IS_DEFAULT_GROUP, LIVE_OUTPUT_TYPE, ARCHIVE_LIVE_OUTPUT_PROFILE, LIVE_OUTPUT_PROFILES, DEBUG):

	API_URL = f"{URL}/liveOutputProfileGroup"

	HEADERS = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {AUTH_TOKEN}"
	}

	BODY = {
		"liveOutputProfileGroupId": LIVE_OUTPUT_PROFILE_GROUP_ID,
		"name": NAME,
		"isEnabled": IS_ENABLED,
		"manifestType": MANIFEST_TYPE,
		"isDefaultGroup": IS_DEFAULT_GROUP,
		"liveOutputType": LIVE_OUTPUT_TYPE,
		"archiveLiveOutputProfile": ARCHIVE_LIVE_OUTPUT_PROFILE,
		"liveOutputProfiles": LIVE_OUTPUT_PROFILES
	}
	if DEBUG:
		print(f"API_URL: {API_URL}\nMETHOD: PUT\nBODY: {json.dumps(BODY)}")

	try:
		RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

		if not RESPONSE.ok:
			raise Exception()

		return RESPONSE.json()
	except:
		_api_exception_handler(RESPONSE, "Update Live Output Profile Group Failed")