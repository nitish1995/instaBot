import requests                                                                                                         # Library for web requests.
import urllib                                                                                                           # Library used for downloading posts.
from colorama import init                                                                                               # For colored output on console.
from colorama import Fore, Style
# -*- coding: utf-8 -*

init()
BASE_URL = "https://api.instagram.com/v1/"                                                                              # Base url for instagram api endpoints, this will be same trough out application.





#take_input will take and handle different type of inputs.(Two parameter of string type and return input data.)
#.......................................................................................................................
def take_input(input_type,message):
    if input_type == 'Y':                                                                                               # If want to take input in yes or no.
        input_data = raw_input(message).replace(" ","")
        input_data = input_data.upper()                                                                                 # Handling invalid cases.
        if len(input_data):
            if input_data == 'Y' or input_data == 'YES':
                return 'Y'
            elif input_data == 'N' or input_data == 'NO':
                return 'N'
            else:
                print (Fore.RED + "Please enter (Y/N).")
                print(Style.RESET_ALL)
        else:
            print (Fore.RED + "Please don't leave it blank.")
            print (Style.RESET_ALL)
#....................................................................
    elif input_type == 'number':                                                                                        # If want to take a integer.
        input_data = raw_input(message).replace(" ","")
        if len(input_data):                                                                                             # Handling invalid cases.
            try:
                input_data = int(input_data)
                return input_data
            except:
                print (Fore.RED + "Please enter a number.")
                print (Style.RESET_ALL)
        else:
            print (Fore.RED + "Please don't leave it blank.")
            print (Style.RESET_ALL)
#....................................................................
    elif input_type == 'float':                                                                                         # If want to take a float.
        input_data = raw_input(message).replace(" ","")
        if len(input_data):                                                                                             # Handling invalid cases.
            try:
                input_data = float(input_data)
                return input_data
            except:
                print (Fore.RED + "Please enter a number.")
                print (Style.RESET_ALL)
        else:
            print (Fore.RED + "Please don't leave it blank.")
            print (Style.RESET_ALL)
#...................................................................
    elif input_type == 'string':                                                                                        # If want to take a string.
        input_data = raw_input(message).strip()
        if len(input_data):                                                                                             # Handling invalid cases.
            return input_data
        else:
            print (Fore.RED + "Please don't leave it blank.")
            print (Style.RESET_ALL)

    return None
#End of take_input method...............................................................................................





#fetch_data method will fetch get and post requests.(More than two parameter ,and a json return type).
#.......................................................................................................................
def fetch_data(req_method,trail_url,*extras):
    request_url = BASE_URL + trail_url                                                                                  # Making completer url.
    print "%s" % request_url
#......................................................................................
    if req_method == 'get':                                                                                             # To handle cases with get request.
        try:                                                                                                            # Handling invalid cases.
            info = requests.get(request_url).json()
            if info['meta']['code'] == 200:
                return info
            else:
                print (Fore.RED + "Status code other than 200 received.")
                print (Style.RESET_ALL)
        except:
            print (Fore.RED + "Invalid response or check your internet connection.")
            print (Style.RESET_ALL)
#......................................................................................
    elif req_method == 'post':                                                                                          # To handle cases with post requests.
        try:                                                                                                            # Handling invalid cases.
            info = requests.post(request_url,extras[0]).json()
            if info['meta']['code'] == 200:
                return info
            else:
                print (Fore.RED + "Status code other than 200 received.")
                print (Style.RESET_ALL)
        except:
            print (Fore.RED + "invalid response or check your internet connection.")
            print (Style.RESET_ALL)

    return None
#end of fetch_data method...............................................................................................





#download_post will download the given post(two parameter json structure, index od post and return id of post)
#.......................................................................................................................
def download_post(post_details,index):
    if len(post_details['data']):
        if post_details['data'][index]['type'] == 'image':                                                              # Checking for image.
            url = post_details['data'][index]['images']['standard_resolution']['url']
            name = post_details['data'][index]['id'] + '.jpeg'

        elif post_details['data'][index]['type'] == 'video':                                                            # Checking for videos.
            url = post_details['data'][index]['videos']['standard_resolution']['url']
            name = post_details['data'][index]['id'] + '.mp4'

        print "Downloading post."
        try:
            urllib.urlretrieve(url, name)                                                                               # Downloading post.
            print (Fore.GREEN + "Downloaded successfully")
            print (Style.RESET_ALL)
        except:
            print (Fore.RED + "Can not download this post. Try again!")
            print (Style.RESET_ALL)

        return post_details['data'][index]['id']                                                                        # Return post id.

    else:
        print (Fore.RED + "No post found. Try again!")
        print (Style.RESET_ALL)

    return None
#End of download_post method............................................................................................
