
###### COURSE_ID
# Get the course ID to update
# 1. Open course in Canvas
# 2. Copy the number at the end of the URL.
#    For example, if the URL is https://wustl.instructure.com/courses/66694, it'd be 66694
COURSE_ID = 00000  # Ex: it was 68891 for 247 FL21

###### CANVAS URL
#API_URL = "https://wustl.instructure.com/"
#API_URL = "https://wustl.test.instructure.com/"
API_URL = "https://wustl.beta.instructure.com/"   
# BETA is inaccessible to students and a good place for testing. 
#      It syncs (pulls in) the production version once a week
# TEST is inaccessible to students and lags beta.  It syncs about once a month

####### Canvas API key
# Generate a key: 
# 1. Go to: https://wustl.instructure.com/profile/settings
# 2. Select "+ Access Token"
# 3. Enter an appropriate name and expiration date (suggest keeping expiration aligned with semester)
# 4. Generate token and copy/paste in string below
API_KEY = "TODO"
#Ex: API_KEY = "6079~hGM0ytngC2k4p2jzDLMTT43cHmUslMuQVV41mflJrKEyYWoxtIFnt9OE8capspm9"
