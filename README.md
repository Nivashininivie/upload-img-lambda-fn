# upload-img-lambda-fn

A repo containing logics that handles the images via API to lambda. The lambda function in turn uploads the images to s3 bucket &amp; the metadata to RDS (MySQL). 
The function also handles a get request, which returns the metadata stored against the user id

# Cognito Login
https://ap-south-1ouuyfjtao.auth.ap-south-1.amazoncognito.com/login?client_id=62t1ljmj03ksim15ri58dnmn0c&response_type=code&scope=email+openid+phone&redirect_uri=https%3A%2F%2Fgoogle.com

# Token endpoint
Fetch the auth code from cognito login & replace to the value in code parameter
curl --location 'https://ap-south-1ouuyfjtao.auth.ap-south-1.amazoncognito.com/oauth2/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: XSRF-TOKEN=05a210d5-66e6-457b-ac23-87390f29424b' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'code=206102c3-d40c-40bc-8fb9-c2e017b64459' \
--data-urlencode 'redirect_uri=https://google.com' \
--data-urlencode 'client_id=62t1ljmj03ksim15ri58dnmn0c' \
--data-urlencode 'client_secret=3qdu9ukge119qsa83skv4kl2s9gosa7pviotfa1uhke2h50pic'

# Upload image to S3 & metadata to RDS
Replace the token in Bearer from the above request 
curl --location 'https://rz3h6jjfm1.execute-api.ap-south-1.amazonaws.com/dev/images/upload' \
--header 'Authorization: Bearer eyJraWQiOiJrVHJIZGVrUXpWYUs2VFRVbUpweHB5aFBhdVQwXC90cVRxRUxiWU1LYkdmZz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlMWMzZmQ5YS01MGIxLTcwYjMtNDVmYy0xZGFmNzA3OTBjNjkiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGgtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aC0xX29VVXlGSnRhTyIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjYydDFsam1qMDNrc2ltMTVyaTU4ZG5tbjBjIiwib3JpZ2luX2p0aSI6IjgwMWU0MjUyLWU0MjgtNDIyMi1iMDhiLWI0M2NjODJmMGI3OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoicGhvbmUgb3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNzMyODg5MDIwLCJleHAiOjE3MzI4OTI2MjAsImlhdCI6MTczMjg4OTAyMCwianRpIjoiN2VmMTQxYjgtOTBmYi00Yjg2LWFjMTgtMjg0MDBmZmU5OWRhIiwidXNlcm5hbWUiOiJlMWMzZmQ5YS01MGIxLTcwYjMtNDVmYy0xZGFmNzA3OTBjNjkifQ.V88t22qXh5dWYyfElC6Flba5Urfs37mSCUakhxtQQg2z0IeEpzY6yH8SgChVEPvtY9VGmA3ivv2CbO2ubXThUJe5stLreQXx21mAYsYAqo88NyaEmYCbv1FI75kAEd12pFc41Vv64PdN7mRfcdl-6PkRz5HJkGjEvUrfXl0lrKwDLyo8OodrBWaM3BtgURBf-5GejZJd60w7macorZJ__S7kj9azK-yQvxxqroD_5DC3qAwUxmzmeaVMlYJfDLtnSH09G3CQ4kp63NTooFOURsKDynkjEC9PSJLrA32boSPA_KiEOwbIwsZP_GyhzxrebpHCDvV9RNcPkBlA63_Z1A' \
--header 'Content-Type: text/plain' \
--data-binary '@/Users/nivashinikm/Desktop/test.jpeg'

# Fetch Metadata
Replace the user_id to the query params
curl --location 'https://rz3h6jjfm1.execute-api.ap-south-1.amazonaws.com/dev/images/fetch?user_id=e1c3fd9a-50b1-70b3-45fc-1daf70790c69'
 