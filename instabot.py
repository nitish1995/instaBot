import requests                                                                                                         # Library for web requests.
from colorama import init                                                                                               # Library for producing colored terminal output.
from colorama import Fore
from keys import ACCESS_TOKEN

init()
BASE_URL = "https://api.instagram.com/v1/"                                                                              # Base url for instagram api, this will be same trough out application.





#Self_info will print information of Access Token owner.(No parameter and return type.)
#.......................................................................................................................
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % ACCESS_TOKEN                                             # Forming url for self info as per documentation.
    print "Requesting information for: " + request_url
    try:
        my_info = requests.get(request_url).json()                                                                      # Hitting get request with requests library.
        print "My name is %s" %(my_info['data']['full_name'])                                                           # Printing Information about user.
        print "My followers : %s" %(my_info['data']['counts']['followed_by'])
        print "People I follow : %s" %(my_info['data']['counts']['follows'])
        print "No. of posts : %s" %(my_info['data']['counts']['media'])
    except:
        print "invalid response or check your connection."                                                              # For handling unexpected error.
#End of self_info() method..............................................................................................





#Get_user_id will fetch user_id.(One string parameter,user_name and return type of string,user_id.)
#.......................................................................................................................
def get_user_id(user_name):
    user_id = None
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') %(user_name,ACCESS_TOKEN)                            # Forming url for user id as per documentation.
    print "Requesting information for: " + request_url
    try:
        search_result = requests.get(request_url).json()                                                                # Hitting get request with requests library.
        if search_result['meta']['code'] == 200:                                                                        # Checking for successfull response.
            if len(search_result['data']):                                                                              # Checking for empty response result.
                user_id = search_result['data'][0]['id']                                                                # Fetching user_id.
            else:
                print "User does not exist"
        else:
            print "Status code other than 200 received!"

    except:
        print "invalid response or check your connection."
    return user_id
#End of get_user_id method..............................................................................................





#Get_user_info method will print user info(One string parameter,user_name and no return type.)
#.......................................................................................................................
def get_user_info(user_name):
    user_id = get_user_id(user_name)                                                                                    # Calling get_user_id method for id.
    if user_id is not None:                                                                                             # Checking for valid id.
        request_url = (BASE_URL + "users/%s/?access_token=%s") %(user_id,ACCESS_TOKEN)                                  # Forming url for user id as per documentation.
        print "Requesting information for: " + request_url
        try:
            user_info = requests.get(request_url).json()                                                                # Hitting get request with help of requests library.
            print "%s full information is: " %user_name                                                                 # Printing user information.
            print "Name: %s" %(user_info['data']['full_name'])
            print "Followers: %s" %(user_info['data']['counts']['followed_by'])
            print "Follows: %s" %(user_info['data']['counts']['follows'])
            print "number of posts: %s" %(user_info['data']['counts']['media'])
        except:
            print "Invalid response or check your connection."
#End of get_user_info Method............................................................................................





#Start of photobot application.
#.......................................................................................................................
print "Welcome to Instabot."
self_info()
user_name = raw_input("Please enter name of your friend to search.").strip()
if len(user_name):
    get_user_info(user_name)
else:
    print "please enter a valid name."
#.......................................................................................................................