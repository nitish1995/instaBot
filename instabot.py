import requests                                                                                                         # Library for web requests.
import urllib
from random import randint
from keys import ACCESS_TOKEN

BASE_URL = "https://api.instagram.com/v1/"                                                                              # Base url for instagram api, this will be same trough out application.





#take_input will take and handle different type of inputs.(Two parameter of string type and return type of string.)
#.......................................................................................................................
def take_input(input_type,message):
    if input_type == 'Y':                                                                                               # if want to take input as yes or no.
        input_data = raw_input(message).replace(" ","")
        input_data = input_data.upper()                                                                                 # Handling invalid cases.
        if len(input_data):
            if input_data == 'Y' or input_data == 'YES':
                return 'Y'
            elif input_data == 'N' or input_data == 'NO':
                return 'N'
            else:
                print "Please enter (Y/N)."
        else:
            print "Please don't leave it blank."

    elif input_type == 'number':                                                                                        # If want to take a number.
        input_data = raw_input(message).replace(" ","")
        if len(input_data):                                                                                             # handling invalid cases.
            try:
                input_data = int(input_data)
                return input_data
            except:
                print "Please enter a number"
        else:
            print "Please don't leave it blank."

    elif input_type == 'string':                                                                                        # If want to take a string.
        input_data = raw_input(message).strip()
        if len(input_data):                                                                                             # Handling invalid cases.
            return input_data

        else:
            print "Please don't leave it blank."
    return None
#End of take_input method...............................................................................................





#fetch_data method will fetch get and post requests.(More than two paramter,and a json return type).
#.......................................................................................................................
def fetch_data(req_method,trail_url,*extras):
    request_url = BASE_URL + trail_url
    print "requesting for: " + request_url
    if req_method == 'get':
        try:
            info = requests.get(request_url).json()
            if info['meta']['code'] == 200:
                return info
            else:
                print "status code other than 200 recieved."
        except:
            print "invalid response or check your internet connection."
    elif req_method == 'post':
        try:
            info = requests.post(request_url,extras[0]).json()
            if info['meta']['code'] == 200:
                return info
            else:
                print "Status code other than 200 recieved."
        except:
            print "invalid response or check your internet connection."
    return None
#end of fetch_data method...............................................................................................





#Self_info will print information of Access Token owner.(No parameter and return type.)
#.......................................................................................................................
def self_info():
    trail_url = 'users/self/?access_token=%s' % ACCESS_TOKEN                                                            # Forming url for self info as per documentation.
    req_method = 'get'
    my_info = fetch_data(req_method,trail_url)
    if my_info is not None:
        print "My name is %s" % (my_info['data']['full_name'])                                                          # Printing Information about user.
        print "My followers : %s" % (my_info['data']['counts']['followed_by'])
        print "People I follow : %s" % (my_info['data']['counts']['follows'])
        print "No. of posts : %s" % (my_info['data']['counts']['media'])

#End of self_info() method..............................................................................................






#self_id will return the id of the owner of access_token.(no input parameter and return the user_id).
#.......................................................................................................................
def self_id():
    trail_url = 'users/self/?access_token=%s' % ACCESS_TOKEN
    req_method = 'get'
    my_id = fetch_data(req_method,trail_url)
    if my_id is not None:
        my_id = my_id['data']['id']
        return my_id
#.......................................................................................................................




#self_post will return the id of most recent media.(no parameter and return media id.)
#.......................................................................................................................
def self_post():
    trail_url = 'users/self/media/recent/?access_token=%s' % ACCESS_TOKEN
    req_method = 'get'
    post_details = fetch_data(req_method,trail_url)
    if post_details is not None:
        if len(post_details['data']):
            if post_details['data'][0]['type'] == 'image':
                url = post_details['data'][0]['images']['standard_resolution']['url']
            elif post_details['data'][0]['type'] == 'video':
                url = post_details['data'][0]['videos']['standard_resolution']['url']

            name = 'my_post' + str(randint(0,1000000000)) + '.jpg'
            urllib.urlretrieve(url,name)
            return post_details['data'][0]['id']
        else:
            print "No recent post."
#.......................................................................................................................





#user_post will return the id of most recent media.(one parameter of string type username and return post id.)
#.......................................................................................................................
def get_post_id(user_name):
    user_id = get_user_id(user_name)
    if user_id is not None:
        trail_url = 'users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
        req_method = 'get'
        post_details = fetch_data(req_method, trail_url)
        if post_details is not None:
            if len(post_details['data']):
                if post_details['data'][0]['type'] == 'image':
                    url = post_details['data'][0]['images']['standard_resolution']['url']
                elif post_details['data'][0]['type'] == 'video':
                    url = post_details['data'][0]['videos']['standard_resolution']['url']

                name = post_details['data'][0]['caption']['from']['full_name'] + str(randint(0, 1000000000)) + '.jpg'
                urllib.urlretrieve(url, name)
                return post_details['data'][0]['id']
            else:
                print "No recent post."
    return None
#.......................................................................................................................





#Get_user_id will fetch user_id.(One string parameter,user_name and return type of string,user_id.)
#.......................................................................................................................
def get_user_id(user_name):
    user_id = None
    trail_url = 'users/search?q=%s&access_token=%s'%(user_name,ACCESS_TOKEN)
    req_method = 'get'
    search_result = fetch_data(req_method,trail_url)
    if search_result is not None:
        if len(search_result['data']):
            user_id = search_result['data'][0]['id']
        else:
            print "User not found."
    return user_id
#End of get_user_id method..............................................................................................





#Get_user_info method will print user info(One string parameter,user_name and no return type.)
#.......................................................................................................................
def get_user_info(user_name):
    user_id = get_user_id(user_name)                                                                                    # Calling get_user_id method for id.
    if user_id is not None:                                                                                             # Checking for valid id.
        req_method = 'get'
        trail_url = "users/%s/?access_token=%s" %(user_id,ACCESS_TOKEN)
        user_info = fetch_data(req_method,trail_url)
        if user_info is not None:
            print "%s full information is: " % user_name  # Printing user information.
            print "Name: %s" % (user_info['data']['full_name'])
            print "Followers: %s" % (user_info['data']['counts']['followed_by'])
            print "%s follows %s people" % (user_info['data']['full_name'], user_info['data']['counts']['follows'])
            print "number of posts: %s" % (user_info['data']['counts']['media'])
#End of get_user_info Method............................................................................................





#like_post will like the post on given media.(takes one parameter of username and no return type.)
#.......................................................................................................................
def like_post(username):
    media_id = get_post_id(username)
    if media_id is not None:
        req_method = 'post'
        trail_url = 'media/%s/likes' %(media_id)
        payload = {"access_token" : ACCESS_TOKEN}
        print "liking the post"
        info = fetch_data(req_method,trail_url,payload)
        if info is not None:
            print "Successfully liked"
#end of like_post method................................................................................................




#Start of photobot application.
#.......................................................................................................................
print "Welcome to Instabot."
self_info()
message = "Please enter name of your friend to search."
user_name = take_input('string',message)
if user_name is not None:
    like_post(user_name)
#.......................................................................................................................