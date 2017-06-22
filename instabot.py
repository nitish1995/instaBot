import requests                                                                                                         # Library for web requests.
import urllib
from colorama import init
from colorama import Fore , Style
from keys import ACCESS_TOKEN
init()
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
    print "%s" % request_url
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
    print "Requesting info for: "
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
    print "Requesting info for: "
    my_id = fetch_data(req_method,trail_url)
    if my_id is not None:
        my_id = my_id['data']['id']
        return my_id
#.......................................................................................................................




#self_post will return the id of most recent media.(no parameter and return media id.)
#.......................................................................................................................
def get_own_post():
    trail_url = 'users/self/media/recent/?access_token=%s' % ACCESS_TOKEN
    req_method = 'get'
    print "Requesting for media: "
    post_details = fetch_data(req_method,trail_url)
    if post_details is not None:
        if len(post_details['data']):
            if post_details['data'][0]['type'] == 'image':
                url = post_details['data'][0]['images']['standard_resolution']['url']
                name = post_details['data'][0]['id'] + '.jpeg'
            elif post_details['data'][0]['type'] == 'video':
                url = post_details['data'][0]['videos']['standard_resolution']['url']
                name = post_details['data'][0]['id'] + '.mp4'

            urllib.urlretrieve(url,name)
            return post_details['data'][0]['id']
        else:
            print "There is no recent post!."
    return None
#.......................................................................................................................





#
#.......................................................................................................................
def all_post(post_details):
    i = 1
    for item in post_details['data']:
        try:
            text = item['caption']['text' ]
        except:
            text = 'No_caption.'
        print  "%d ."% (i) + "Caption_TEXT: " + (Fore.BLUE + text) + Style.RESET_ALL + " Total_likes: " + (Fore.GREEN + '%d' % item['likes']['count'])
        print Style.RESET_ALL
        i += 1
    selection = take_input('number','Select from above posts. ')
    if selection is not None:
        selection = selection - 1
        print "Downloading post. "
        if post_details['data'][selection]['type'] == 'image':
            url = post_details['data'][selection]['images']['standard_resolution']['url']
            name = post_details['data'][selection]['id'] + '.jpeg'
        elif post_details['data'][selection]['type'] == 'video':
            url = post_details['data'][selection]['videos']['standard_resolution']['url']
            name = post_details['data'][selection]['id'] + '.mp4'

        urllib.urlretrieve(url, name)
        return post_details['data'][selection]['id']
    return None
#.......................................................................................................................





#get_most_recent_post will fetch the most recent post.(no parameter return post id).
#.......................................................................................................................
def get_most_recent_post(post_details):
    print "Downloading post. "
    if post_details['data'][0]['type'] == 'image':
        url = post_details['data'][0]['images']['standard_resolution']['url']
        name = post_details['data'][0]['id'] + '.jpeg'
    elif post_details['data'][0]['type'] == 'video':
        url = post_details['data'][0]['videos']['standard_resolution']['url']
        name = post_details['data'][0]['id'] + '.mp4'

    urllib.urlretrieve(url, name)
    return post_details['data'][0]['id']
#.......................................................................................................................





#
#.......................................................................................................................
def minimum_liked_post(post_details):
    likes = post_details['data'][0]['likes']['count']
    selection = 0
    i = 0
    for item in post_details['data']:
        if item['likes']['count'] < likes:
            likes = item['likes']['count']
            selection = i
        i += 1

    print "Downloading post. "
    if post_details['data'][selection]['type'] == 'image':
        url = post_details['data'][selection]['images']['standard_resolution']['url']
        name = post_details['data'][selection]['id'] + '.jpeg'
    elif post_details['data'][selection]['type'] == 'video':
        url = post_details['data'][selection]['videos']['standard_resolution']['url']
        name = post_details['data'][selection]['id'] + '.mp4'

    urllib.urlretrieve(url, name)
    return post_details['data'][selection]['id']
#.......................................................................................................................





#
#.......................................................................................................................
def most_liked_post(post_details):
    likes = post_details['data'][0]['likes']['count']
    selection = 0
    i = 0
    for item in post_details['data']:
        if item['likes']['count'] > likes:
            likes = item['likes']['count']
            selection = i
        i += 1

    print "Downloading post. "
    if post_details['data'][selection]['type'] == 'image':
        url = post_details['data'][selection]['images']['standard_resolution']['url']
        name = post_details['data'][selection]['id'] + '.jpeg'
    elif post_details['data'][selection]['type'] == 'video':
        url = post_details['data'][selection]['videos']['standard_resolution']['url']
        name = post_details['data'][selection]['id'] + '.mp4'

    urllib.urlretrieve(url, name)
    return post_details['data'][selection]['id']
#.......................................................................................................................





#
#.......................................................................................................................
def post_with_keywords(post_details):
    keyword = take_input('string',"enter keyword that you want to search in caption.")
    keyword = keyword.upper()
    i = 0
    selection = None
    if keyword is not None:
        for item in post_details['data']:
            try:
                text = item['caption']['text']
                text = text.upper()
            except:
                text = ''
            if text.find(keyword) != -1:
                selection = i
                break
            i += 1
        if selection is not None:
            if post_details['data'][selection]['type'] == 'image':
                url = post_details['data'][selection]['images']['standard_resolution']['url']
                name = post_details['data'][selection]['id'] + '.jpeg'
            elif post_details['data'][selection]['type'] == 'video':
                url = post_details['data'][selection]['videos']['standard_resolution']['url']
                name = post_details['data'][selection]['id'] + '.mp4'
            print "Downloading post. q  "
            urllib.urlretrieve(url, name)
            return post_details['data'][selection]['id']
    return None

#.......................................................................................................................





#user_post will return the id of most recent media.(one parameter of string type username and return post id.)
#.......................................................................................................................
def get_users_post(user_name):
    user_id = get_user_id(user_name)
    if user_id is not None:
        trail_url = 'users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
        req_method = 'get'
        print "Requesting for media: "
        post_details = fetch_data(req_method, trail_url)
        if post_details is not None:
            if len(post_details['data']):
                if len(post_details['data']) == 1:
                    if post_details['data'][0]['type'] == 'image':
                        url = post_details['data'][0]['images']['standard_resolution']['url']
                        name = post_details['data'][0]['id'] + '.jpeg'
                    elif post_details['data'][0]['type'] == 'video':
                        url = post_details['data'][0]['videos']['standard_resolution']['url']
                        name = post_details['data'][0]['id'] + '.mp4'

                    urllib.urlretrieve(url, name)
                    return post_details['data'][0]['id']
                else:
                    print "There are more than one recent post. Which one you want to select: "
                    selection = take_input('number',' 1. To see all the post. \n 2. For most recent post. \n 3. For post with minimum likes. \n 4. For post with maximum likes \n 5. For post containing particular keyword.')
                    if selection is not None:
                        if selection == 1:
                            return all_post(post_details)
                        elif selection == 2:
                            return get_most_recent_post(post_details)
                        elif selection == 3:
                            return minimum_liked_post(post_details)
                        elif selection == 4:
                            return most_liked_post(post_details)
                        elif selection == 5:
                            return post_with_keywords(post_details)
                        else:
                            print "Please select from given option."
            else:
                print "There is No recent post!."
    return None
#.......................................................................................................................





#Get_user_id will fetch user_id.(One string parameter,user_name and return type of string,user_id.)
#.......................................................................................................................
def get_user_id(user_name):
    user_id = None
    trail_url = 'users/search?q=%s&access_token=%s'%(user_name,ACCESS_TOKEN)
    req_method = 'get'
    print "Requesting info for: "
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
def user_info(user_name):
    user_id = get_user_id(user_name)                                                                                    # Calling get_user_id method for id.
    if user_id is not None:                                                                                             # Checking for valid id.
        req_method = 'get'
        trail_url = "users/%s/?access_token=%s" %(user_id,ACCESS_TOKEN)
        print "Requesting info for: "
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
def like_a_post(username):
    media_id = get_users_post(username)
    if media_id is not None:
        req_method = 'post'
        trail_url = 'media/%s/likes' %(media_id)
        payload = {"access_token" : ACCESS_TOKEN}
        print "liking the post: "
        info = fetch_data(req_method,trail_url,payload)
        if info is not None:
            print "Like was successful!."
        else:
            print "Your like was unsuccessful. Try again!"
#end of like_post method................................................................................................





#get comments will get the list of comments on given media id(one parameter usernae and no return type.)
#.......................................................................................................................
def get_comments(username):
    media_id = get_users_post(username)
    if media_id is not None:
        req_method = 'get'
        trail_url = 'media/%s/comments?access_token=%s' % (media_id,ACCESS_TOKEN)
        print "Accessing for comments:"
        info = fetch_data(req_method,trail_url)
        if info is not None:
            if len(info['data']):
                for item in info['data']:
                    print "FROM: " + (Fore.BLUE +item['from']['full_name']) + Style.RESET_ALL + ". TEXT: " + (Fore.GREEN + item['text'])
                    print (Style.RESET_ALL)
                print "All comments printed successfully."
            else:
                print "No comments on this post."
        else:
            print "Unable to fetch comments. Try again."
#.......................................................................................................................



#post_a_comment will post the comment on a media.(one parameter is username and no return type).
#.......................................................................................................................
def post_a_comment(username):
    media_id = get_users_post(username)
    comment_text = take_input('string','your_comment:')
    if media_id is not None and comment_text is not None:
        req_method = 'post'
        trail_url = 'media/%s/comments' % (media_id)
        payload = {"access_token" : ACCESS_TOKEN, "text" : comment_text}
        print "Making comment on post: "
        info = fetch_data(req_method,trail_url,payload)
        if info is not None:
            print "Successfully added a new comment!."
        else:
            print "Unable to add comment. Try again!"
#.......................................................................................................................





#get_recent_like will download fetch the list recently liked by owner.
#.......................................................................................................................
def get_recent_like():
    req_method = 'get'
    trail_url = 'users/self/media/liked?access_token=%s' % (ACCESS_TOKEN)
    print "Requesting for recent likes: "
    info = fetch_data(req_method,trail_url)
    if info is not None:
        if len(info['data']):
            print "recently liked images: "
            for item in info['data']:
                print "user: " + (Fore.BLUE + item['user']['full_name']) + Style.RESET_ALL + '. caption text: ' + (Fore.GREEN + item['caption']['text'])
                print(Style.RESET_ALL)
            return info
        else :
            print "No recent comments on this post."
    else:
        print "Unable to fetch data. try again! "
    return None

#.......................................................................................................................




#Start of photobot application.
#.......................................................................................................................
print "Welcome to Instabot."
self_info()

#.......................................................................................................................