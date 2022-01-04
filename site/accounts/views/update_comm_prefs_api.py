"""API endpoint for updating user's communication preferences.
The request body must be in a stringified JSON format which can be loaded into
a dictionary. Each key must be a boolean value.
"""

# import json
# from django.contrib import messages
# from django.utils import timezone
# from core_functions import fetch_config, dataclasses
# from accounts.models import CommPrefs


# def update_comm_prefs_api(request):
#     """API endpoint for updating user's communication preferences."""

#     # Edge case - reject any non post requests.
#     if request.method != 'POST':
#         return dataclasses.APIResponse(
#             success=False,
#             error_type='invalid method',
#             error='Only compatible with a POST request.'
#         ).as_json_response(405)

#     # Ensure that the user is authenticated.
#     if not request.user.is_authenticated:
#         messages.error(request, 'User is not logged in.')
#         return dataclasses.APIResponse(
#             success=False,
#             error_type='unauthenticated',
#             error='User is not authenticated.'
#         ).as_json_response(401)

#     # Fetch the user's row from the table, if it does not exist, then create a
#     # new empty row.
#     commPrefs = CommPrefs.objects.filter(user=request.user)
#     if commPrefs:
#         commPrefs = commPrefs[0]
#     else:
#         commPrefs = CommPrefs.objects.create(
#             user=request.user,
#             promotions=False,
#             blogs=False,
#             newsletters=False,
#             terms_last_agreed=None
#         )

#     # Update the communication preferences.
#     # Note: the request body should be stringified JSON response where each key
#     # value is a boolean value.
#     postRequest = json.loads(request.body)
#     commPrefKeys = fetch_config('sales')['comm_pref_keys']
#     if postRequest.get(commPrefKeys['newsletters']) is not None:
#         commPrefs.newsletters = postRequest.get(commPrefKeys['newsletters'])
#     if postRequest.get(commPrefKeys['promotions']) is not None:
#         commPrefs.promotions = postRequest.get(commPrefKeys['promotions'])
#     if postRequest.get(commPrefKeys['blogs']) is not None:
#         commPrefs.blogs = postRequest.get(commPrefKeys['blogs'])

#     # A timestamp is stored for the last time the terms were agreed. Update
#     # this timestamp.
#     if postRequest.get(commPrefKeys['termsAccepted']):
#         commPrefs.newsletters = timezone.now()

#     commPrefs.save()

#     return dataclasses.APIResponse(True).as_json_response()
