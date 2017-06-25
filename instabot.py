# -*- coding : utf-8 -*-
import urllib                                                                                                           # Library used for downloading posts.
from colorama import init                                                                                               # For colored output on console.
from colorama import Fore , Style
from keys import ACCESS_TOKEN
from extra_method import take_input, fetch_data, download_post

init()

#list for disasters for testing natural calamity test.
disasters = ['KARTING','AVALANCHES','AVALANCHE','LANDSLIDES','LANDSLIDE','EARTHQUAKES','EARTHQUAKE','SINKHOLES','SINKHOLE','VOLCANIC ERUPTIONS','VOLCANIC ERUPTION','FLOODS','FLOOD','LIMNIC ERUPTIONS','LIMNIC ERUPTION','TSUNAMI','BLIZZARDS','BLIZZARD','CYCLONIC STORMS','CYCLONIC STORM','DROUGHTS','DROUGHT','THUNDERSTORMS','THUNDERSTORM','HAILSTORMS','HAILSTORM','HEAT WAVE','HEAT WAVES','TORNADOES','TORNADOE','WILDFIRES','WILDFIRE','AIRBURST','SOLAR FLARES','SOLAR FLARE']





#Self_info will print information of Access Token owner.(No parameter and return type.)
#.......................................................................................................................
def self_info():
    trail_url = 'users/self/?access_token=%s' % ACCESS_TOKEN                                                            # Forming url for self info as per documentation.
    req_method = 'get'
    print (Fore.YELLOW + "Requesting information: ")
    print(Style.RESET_ALL)
    my_info = fetch_data(req_method,trail_url)                                                                          # Calling fetch_data for get request.
    if my_info is not None:
        print (Fore.CYAN)
        print "My name is %s" % (my_info['data']['full_name'])                                                          # Printing Information about user.
        print "My followers : %s" % (my_info['data']['counts']['followed_by'])
        print "People I follow : %s" % (my_info['data']['counts']['follows'])
        print "No. of posts : %s" % (my_info['data']['counts']['media'])
        print (Style.RESET_ALL)
#End of self_info() method..............................................................................................





#self_id will return the id of the owner of access_token.(no input parameter and return the user_id).
#.......................................................................................................................
def self_id():
    trail_url = 'users/self/?access_token=%s' % ACCESS_TOKEN                                                            # Forming url for owner id.
    req_method = 'get'
    print (Fore.YELLOW + "Requesting for user_id: ")
    print (Style.RESET_ALL)
    my_id = fetch_data(req_method,trail_url)                                                                            # Calling global method for get request.
    if my_id is not None:                                                                                               # Handling for invalid cases.
        my_id = my_id['data']['id']
        return my_id

    return None
#End of self_id.........................................................................................................





#get_own_post will return the id of most recent media and download it.(no parameter and return media id.)
#.......................................................................................................................
def get_own_post():
    trail_url = 'users/self/media/recent/?access_token=%s' % ACCESS_TOKEN                                               # Forming url for recent post.
    req_method = 'get'
    print (Fore.YELLOW + "Requesting for recent post: ")
    print (Style.RESET_ALL)
    post_details = fetch_data(req_method,trail_url)                                                                     # Calling global function for fetching data.
    if post_details is not None:                                                                                        # Handling invalid cases.
        recent_post_id = download_post(post_details,0)
        if recent_post_id is not None:
            return recent_post_id                                                                                       # Return post id.

    return None
#End of get_own_post....................................................................................................





#get_recent_like will download fetch the list recently liked by owner.
#.......................................................................................................................
def get_recent_like():
    req_method = 'get'                                                                                                  # Forming for get request.
    trail_url = 'users/self/media/liked?access_token=%s' % (ACCESS_TOKEN)
    print (Fore.YELLOW + "Requesting for recent likes: ")
    print (Style.RESET_ALL)
    info = fetch_data(req_method,trail_url)                                                                             # Requesting for recent liked image.
    if info is not None:
        if len(info['data']):                                                                                           # printing data.
            print "recently liked images: "
            for item in info['data']:
                try:                                                                                                    # Handling null caption.
                    text = item['caption']['text']
                    text = text.encode('utf-8')
                except:
                    text = "No caption."
                print "user: " + (Fore.BLUE + item['user']['full_name']) + Style.RESET_ALL + '. caption text: ' + (Fore.GREEN + text)
                print(Style.RESET_ALL)
            print (Fore.YELLOW + "Downloading most recent media liked by user")
            print (Style.RESET_ALL)
            post_id = download_post(info, 0)                                                                            # downloading most recent post.
            if post_id is not None:
                return post_id
        else :
            print (Fore.RED + "No recent liked.")
            print (Style.RESET_ALL)
    else:
        print (Fore.RED + "Unable to fetch data. try again! ")
        print (Style.RESET_ALL)

    return None
#End of get_recent_like.................................................................................................





#get_user_id will fetch user_id.(One string parameter,user_name and return type of string,user_id.)
#.......................................................................................................................
def get_user_id(user_name):
    trail_url = 'users/search?q=%s&access_token=%s'%(user_name,ACCESS_TOKEN)                                            # Forming trail url.
    req_method = 'get'
    print (Fore.YELLOW + "Searching for user: ")
    print (Style.RESET_ALL)
    search_result = fetch_data(req_method,trail_url)                                                                    # Calling fetch_data for get request.
    if search_result is not None:                                                                                       # Checking for invalid cases.
        if len(search_result['data']) == 1:                                                                             # If only one result.
            user_id = search_result['data'][0]['id']
            print search_result['data'][0]['full_name']
            return user_id                                                                                              # Return user id.
#...................................................................................
        elif len(search_result['data']) > 1:                                                                            # If more than one search results.
            i = 1
            for item in search_result['data']:                                                                          # Iterate over the result.
                print "%d. " % i + item['full_name']
                i += 1
            selection = take_input('number','Select from above user. ')                                                 # Ask for choice.
            if selection is not None:                                                                                   # Handling for invalid cases.
                if 0 < selection <= len(search_result['data']):
                    user_id = search_result['data'][selection-1]['id']
                    return user_id
                else:
                    print (Fore.RED + "Invalid input. does not exist in list. ")
                    print (Style.RESET_ALL)
#...................................................................................
        else:
            print (Fore.RED + "User not found.")
            print (Style.RESET_ALL)

    return None
#End of get_user_id method..............................................................................................





#user_info method will print user info(One string parameter,user_name and no return type.)
#.......................................................................................................................
def user_info(user_name):
    user_id = get_user_id(user_name)                                                                                    # Calling get_user_id method for id.
    if user_id is not None:                                                                                             # Checking for valid id.
        trail_url = "users/%s/?access_token=%s" %(user_id,ACCESS_TOKEN)
        req_method = 'get'
        print (Fore.YELLOW + "Requesting for user information: ")
        print (Style.RESET_ALL)
        user_info = fetch_data(req_method,trail_url)                                                                    # Calling fetch_data for get request.
        if user_info is not None:
            print (Fore.CYAN)
            print "%s full information is: " % user_name                                                                # Printing user information.
            print "Name: %s" % (user_info['data']['full_name'])
            print "Followers: %s" % (user_info['data']['counts']['followed_by'])
            print "%s follows %s people" % (user_info['data']['full_name'], user_info['data']['counts']['follows'])
            print "number of posts: %s" % (user_info['data']['counts']['media'])
            print (Style.RESET_ALL)

#End of user_info Method................................................................................................





# all_post will print all post and select one.(parameter json type, return post id.)
#.......................................................................................................................
def all_post(post_details):
    i = 1
    for item in post_details['data']:                                                                                   # iterating over all the posts.
        try:
            text = item['caption']['text']
            text = text.encode('utf-8')
        except:
            text = 'No_caption.'
        print  "%d. "% (i) + "Caption_TEXT: " + (Fore.BLUE + text) + Style.RESET_ALL + " Total_likes: " + (Fore.GREEN + '%d' % item['likes']['count'])
        print Style.RESET_ALL
        i += 1
#..............................................................................................
    selection = take_input('number','Select from above posts. ')                                                        # Asking for selecting one post.
    if selection is not None:
        if 0 < selection <= len(post_details['data']):
            selection = selection - 1                                                                                   # converting to zero base index.
            post_id = download_post(post_details,selection)                                                             # Calling download post for post_id.
            if post_id is not None:
                return post_id
        else:
            print (Fore.RED + "Please select from given options.")
            print (Style.RESET_ALL)

    return None
#End of all_post method.................................................................................................





#get_most_recent_post will fetch the most recent post.(one parameter of json type. return post id).
#.......................................................................................................................
def get_most_recent_post(post_details):
    post_id = download_post(post_details,0)                                                                             # Calling download post with zero for most recent.
    if post_id is not None:                                                                                             # Handling invalid cases.
        return post_id

    return None
#End of get_most_recent_post............................................................................................





#minimum_likes_post will return post with minimum like.(one parameter of json type and return post id.)
#.......................................................................................................................
def minimum_liked_post(post_details):
    likes = post_details['data'][0]['likes']['count']                                                                   # Initializing variable.
    selection = 0
    i = 0
    for item in post_details['data']:                                                                                   # Finding index of post with minimum likes.
        if item['likes']['count'] < likes:
            likes = item['likes']['count']
            selection = i
        i += 1

    count = 0
    for item in post_details['data']:
        if item['likes']['count'] == likes:
            count += 1
    if count > 1:
        print (Fore.RED + "Conflict in minimum liked post. Please see all post.")
        print (Style.RESET_ALL)
        post_id = all_post(post_details)
        selection = None
#.......................................................................................
    if selection is not None:
        post_id = download_post(post_details, selection)                                                                # Calling download post with selection.
    if post_id is not None:
        return post_id

    return None
#End of minimum_liked_post..............................................................................................





#most_liked_post will return post with maximum like.(one parameter of json type and return post id.)
#.......................................................................................................................
def most_liked_post(post_details):
    likes = post_details['data'][0]['likes']['count']                                                                   # Initializing variable.
    selection = 0
    i = 0
    for item in post_details['data']:                                                                                   # searching for maximum likes.
        if item['likes']['count'] > likes:
            likes = item['likes']['count']
            selection = i
        i += 1

    count = 0
    for item in post_details['data']:
        if item['likes']['count'] == likes:
            count += 1
    if count > 1:
        print (Fore.RED + "Conflict in most liked post. Please see all post.")
        print (Style.RESET_ALL)
        post_id = all_post(post_details)
        selection = None
#......................................................................................
    if selection is not None:
        post_id = download_post(post_details, selection)                                                                # Calling download post for post id.
    if post_id is not None:
        return post_id

    return None
#End of most_liked_post.................................................................................................





#this method with search for particular keyword in caption.(one parameter of json type and return post id.)
#.......................................................................................................................
def post_with_keywords(post_details):
    keyword = take_input('string',"Enter keyword that you want to search in caption.")                                  # asking for keyword to search.
    if keyword is not None:                                                                                             # checking for invalid cases.
        keyword = keyword.upper()
        i = 0
        selection = None
#....................................................................................
        print (Fore.BLUE + "Searching for keyword in captions.")
        print (Style.RESET_ALL)
        for item in post_details['data']:                                                                               # Searching for keyword.
            try:
                text = item['caption']['text']                                                                          # handling if caption is null.
                text = text.upper()
            except:
                text = ''
            if text.find(keyword) != -1:
                selection = i
                break
            i += 1
#.....................................................................................
        if selection is not None:
            post_id = download_post(post_details,selection)                                                             # Calling download post for post id.
            if post_id is not None:
                return post_id
        else:
            print (Fore.RED + "Keyword not found in any caption. Try again!")
            print (Style.RESET_ALL)

    return None
#End of post_with_keyword...............................................................................................





#user_post will return the id of most recent media.(one parameter of string type username and return post id.)
#.......................................................................................................................
def get_users_post(user_name):
    user_id = get_user_id(user_name)                                                                                    # Calling get_user_id for user id.
    if user_id is not None:
        trail_url = 'users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)                                  # Forming trail url.
        req_method = 'get'
        print (Fore.YELLOW + "Requesting for media: ")
        print (Style.RESET_ALL)
        post_details = fetch_data(req_method, trail_url)                                                                # Fetching post details.
        if post_details is not None:
#....................................................................................
            if len(post_details['data']) == 0:                                                                          # Handling if no post found.
                print (Fore.RED + "No recent post found.")
                print (Style.RESET_ALL)
                return None
#....................................................................................
            elif len(post_details['data']) == 1:                                                                          # Handling if only record found.
                print "Only one post found. "
                post_id = download_post(post_details,0)
                if post_id is not None:
                    return post_id
#.....................................................................................
            else:
                print "There are more than one recent post. Which one you want to select: "
                selection = take_input('number',' 1. To see all the post. \n 2. For most recent post. \n 3. For post with minimum likes. \n 4. For post with maximum likes \n 5. For post containing particular keyword: \n')
                if selection is not None:                                                                               # Handling if more than one post by asking user.
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
                        print (Fore.RED + "Please select from given option.")
                        print (Style.RESET_ALL)

    return None
#End of get_user_post...................................................................................................





#like_post will like the post on given media.(takes one parameter of username and no return type.)
#.......................................................................................................................
def like_a_post(username):
    media_id = get_users_post(username)                                                                                 # Getting the post for liking.
    if media_id is not None:
        req_method = 'post'
        trail_url = 'media/%s/likes' %(media_id)                                                                        # making content for post request.
        payload = {"access_token" : ACCESS_TOKEN}
        print (Fore.YELLOW + "Liking the post.")
        print (Style.RESET_ALL)
        info = fetch_data(req_method,trail_url,payload)                                                                 # Requesting for like.
        if info is not None:
            print (Fore.GREEN + "Like was successful!.")
            print (Style.RESET_ALL)
        else:
            print (Fore.RED + "Your like was unsuccessful. Try again!")
            print (Style.RESET_ALL)
#end of like_post method................................................................................................





#get comments will get the list of comments on given media id(one parameter username and no return type.)
#.......................................................................................................................
def get_comments(username):
    media_id = get_users_post(username)                                                                                 # getting the media for comments.
    if media_id is not None:
        req_method = 'get'
        trail_url = 'media/%s/comments?access_token=%s' % (media_id,ACCESS_TOKEN)                                       # Making url for comments request.
        print (Fore.YELLOW + "Accessing for comments: ")
        print (Style.RESET_ALL)
        info = fetch_data(req_method,trail_url)                                                                         # Fetching comments.
        if info is not None:
            if len(info['data']):                                                                                       # printing comments.
                for item in info['data']:
                    text = item['text']
                    text = text.encode('utf-8')
                    print "FROM: " + (Fore.BLUE +item['from']['full_name']) + Style.RESET_ALL + ". COMMENT: " + (Fore.GREEN + text)
                    print (Style.RESET_ALL)
                print (Fore.GREEN + "All comments printed successfully.")
                print (Style.RESET_ALL)
            else:
                print (Fore.RED + "No comments on this post.")                                                          # If no comments.
                print (Style.RESET_ALL)
        else:
            print (Fore.RED + "Unable to fetch comments. Try again.")
            print (Style.RESET_ALL)
#End of get_comments method.............................................................................................





#post_a_comment will post the comment on a media.(one parameter is username and no return type).
#.......................................................................................................................
def post_a_comment(username):
    media_id = get_users_post(username)                                                                                 # Getting post for comment.
    if media_id is not None:
        comment_text = take_input('string','your_comment:')                                                             # Asking user for comment.
        comment_text = comment_text.encode('utf-8')
        if comment_text is not None:
            req_method = 'post'
            trail_url = 'media/%s/comments' % (media_id)                                                                # Forming for post request.
            payload = {"access_token" : ACCESS_TOKEN, "text" : comment_text}
            print (Fore.YELLOW + "Making comment on post: ")
            print (Style.RESET_ALL)
            info = fetch_data(req_method,trail_url,payload)                                                             # Posting comment.
            if info is not None:
                print (Fore.GREEN + "Successfully added a new comment!.")                                               # printing Message.
                print (Style.RESET_ALL)
            else:
                print (Fore.RED + "Unable to add comment. Try again!")
                print (Style.RESET_ALL)
#End of post_a_comment..................................................................................................





#This will find and list all location near given coordinates.(no parameter and return selected location.)
#.......................................................................................................................
def location_finder1():
    print "Enter the location coordinates."                                                                             # Asking for latitude and longitude.
    lat = take_input('float','Enter latitude coordinate.')
    if lat is not None:
        lng = take_input('float','Enter longitude coordinate.')
        if lng is not None:
            req_method = 'get'
            trail_url = 'locations/search?lat=%s&lng=%s&access_token=%s' %(lat,lng,ACCESS_TOKEN)                        # Forming trail url for locations.
            print (Fore.YELLOW + "Requesting for locations: ")
            print (Style.RESET_ALL)
            info = fetch_data(req_method,trail_url)                                                                     # Fetching locations.
            if info is not None:
                if len(info['data']):
                    print (Fore.GREEN + "Locations Nearby: ")                                                           # Printing nearby location.
                    print (Style.RESET_ALL)
                    i = 1
                    for item in info['data']:
                        location = item['name']
                        location = location.encode('utf-8')
                        print "%d. " % i + location
                        i += 1
                    selection = take_input('number','Select one location.')                                             # Asking to select one location.
                    if selection is not None:
                        if 0 < selection <= len(info['data']):                                                          # Handling invalid cases.
                            selection = selection - 1
                            location_id = info['data'][selection]['id']
                            return location_id
                        else:
                            print (Fore.RED + "Please select from the given options.")
                            print (Style.RESET_ALL)
                else:
                    print (Fore.RED + "Sorry we can not found any popular location nearby.")
                    print (Style.RESET_ALL)
    return None
#End of location finder.................................................................................................





#This will find and list all location near given coordinates.()
#
#.......................................................................................................................
def location_finder():
    locations = []
    print "Enter the location coordinates."                                                                             # Asking for location coordinates.
    lat = take_input('float','Enter latitude coordinate.')
    if lat is not None:
        lng = take_input('float','Enter longitude coordinate.')
        if lng is not None:
            req_method = 'get'
            trail_url = 'locations/search?lat=%s&lng=%s&access_token=%s' %(lat,lng,ACCESS_TOKEN)
            print (Fore.YELLOW + "Requesting for locations: ")
            print (Style.RESET_ALL)
            info = fetch_data(req_method,trail_url)                                                                     # Collecting all the locations.
            if info is not None:
                if len(info['data']):                                                                                   # Iterating over all the locations.
                    print "Locations Nearby:"
                    for item in info['data']:
                        try:
                            location = item['name']
                            location = location.encode('utf-8')
                            print location
                        except:
                            pass
                        locations.append(item['id'])
                    return locations
                else:
                    print "Sorry we can not found any popular location nearby."
    return None
#End of location finder.................................................................................................





#natural_calmity will get image in particular location with natural_calamity(no parameter, return images)
#.......................................................................................................................
def natural_calamity1():
    location = location_finder1()                                                                                        # Asking for one location.
    images = []
    if location is not None:
        req_method = 'get'
        trail_url = 'locations/%s/media/recent?access_token=%s' % (location,ACCESS_TOKEN)                               # Forming url for getting images.
        images_data = fetch_data(req_method,trail_url)

        if images_data is not None:
            if len(images_data['data']):
                index = 0
                for image in images_data['data']:                                                                       # Iterating over all the images.
                    try:
                        text = image['caption']['text']
                        text = text.encode('utf-8')
                        text = text.upper()
                    except:
                        text = ''
                    for item1 in disasters:                                                                             # Searching for keyword.
                        if text.find(item1) != -1:
                            images.append(image['id'])
                            download_post(images_data,index)                                                            # Downloading post with natural calamity.
                    index += 1
                print (Fore.GREEN + "Images with Natural Calamity downloaded successfully.")
                print (Style.RESET_ALL)
                return images
            else:
                print (Fore.RED + "No images for this location")
                print (Style.RESET_ALL)
    return None
#End of natural_calamity method.........................................................................................




#
#.......................................................................................................................
def natural_calamity():
    req_method = 'get'
    locations = location_finder()
    images = []
    if locations is not None:

        for item in locations:                                                                                          # Collecting images for particular location.
            trail_url = 'locations/%s/media/recent?access_token=%s' % (item,ACCESS_TOKEN)
            print (Fore.YELLOW + "Searching post in this location.")
            print (Style.RESET_ALL)
            images_data = fetch_data(req_method,trail_url)

            if images_data is not None:
                if len(images_data['data']):
                    index = 0
                    for image in images_data['data']:                                                                   # Iterating over images.
                        try:
                            text = image['caption']['text']
                            text = text.encode('utf-8')
                            text = text.upper()
                        except:
                            text = ''
                        for item1 in disasters:                                                                         # Checking for disaster in every image caption.
                            if text.find(item1) != -1 and image['id'] not in images:
                                images.append(image['id'])
                                download_post(images_data, index)                                                       # Downloading image.
                                break
                        index += 1
    return images
#.......................................................................................................................





#Start of photobot application.
#.......................................................................................................................
print (Fore.GREEN + "Welcome to Instabot.")
print (Style.RESET_ALL)

photobot = True

while photobot:                                                                                                         # Printing application main menu and handling.
    print 'What to you want to do?'
    selection = take_input('number',' 0. To exit from photobot. \n 1. Print my information.\n 2. Print my user id.\n 3. Download my most recent post.\n 4. Show media recently liked by me.\n 5. Print user information. \n 6. Download user post. \n 7. Like a post. \n 8. Print comments on a post. \n 9. Post a comment. \n 10. Get post with natural calamity between coordinates. \n 11. Get post with natural calamity in specific location.')

    if selection is not None:
        if selection == 0:
            photobot = False
        elif selection == 1:
            self_info()
        elif selection == 2:
            print (Fore.GREEN + self_id())
            print (Style.RESET_ALL)
        elif selection == 3:
            get_own_post()
        elif selection == 4:
            get_recent_like()
        elif selection == 5:
            username = take_input('string', 'please enter the username: ')
            if username is not None:
                user_info(username)
        elif selection == 6:
            username = take_input('string', 'please enter the username: ')
            if username is not None:
                get_users_post(username)
        elif selection == 7:
            username = take_input('string', 'please enter the username: ')
            if username is not None:
                like_a_post(username)
        elif selection == 8:
            username = take_input('string', 'please enter the username: ')
            if username is not None:
                get_comments(username)
        elif selection == 9:
            username = take_input('string', 'please enter the username: ')
            if username is not None:
                post_a_comment(username)
        elif selection == 10:
            images = natural_calamity()
            if images is not None and len(images):
                print (Fore.GREEN + "These images may be of natural calamity, Images Ids:") ,images
                print (Style.RESET_ALL)
            if len(images) == 0:
                print(Fore.RED + "No image found for natural calamity.")
                print (Style.RESET_ALL)
        elif selection == 11:
            images = natural_calamity1()
            if images is not None and len(images):
                print "These images may be of natural calamity, Images Ids:" ,images
        else:
            print (Fore.RED + "Please choose form the given options.")
            print (Style.RESET_ALL)

#End of Photobot application............................................................................................