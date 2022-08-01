#!/usr/bin/pythno3

import re
import sys
import exurl
import random
import requests
# from tqdm import tqdm
from termcolor import colored
from regex_useragents import list_of_regex, list_of_user_agents

header = '''

+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+-
|S|Q|L|i| |D|e|t|e|c|t|o|r|
+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+-
|Coded By > Eslam Akl @eslam3kll
|Blog > eslam3kl.medium.com 
+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+-

'''
print(colored(header, "white"))

file = sys.argv[1]
output_filename = "output_for_" + file
waybackurls = []
results = []
final_urls = []

# read the content from the file and put it into an array.
with open(file, 'r') as links: 
    for line in links:
        line = line.strip()
        waybackurls.append(line)


# function to send a request and match the regex 
def send_request(final_urls_array):
    # proxy setting
    proxies = {"http": "http://127.0.0.1:8080"}
    for line in final_urls_array:
        user_agent_random = random.choice(list_of_user_agents)
        headers = {"User-Agent": str(user_agent_random)}
        try:
            r = requests.get(line, headers=headers, verify=False, timeout=7) # add proxies=proxies if you need to turn it on
            content = r.text

            for pattern in list_of_regex:
                pattern = pattern.strip()
                if re.findall(pattern, content):
                    print(line + colored(" [" + pattern + "]", "red"))
                    output = line + " [" + pattern + "]"
                    results.append(output)
        except KeyboardInterrupt:
            exit()
        except Exception as error:
            pass

# function to replace the value of the parameters
def split_file(wayback_array, payload):
    splitting_urls = exurl.split_urls(wayback_array, payload)
    return splitting_urls


# calling splitting functions
payloads = ["'123", "''123", "\")123", "\"123", "[]123", "\"\"123", "'\"123", "\"'123", "\\123"]
for line in payloads:
    line = line.strip()
    splitted_urls = split_file(waybackurls, line)
    for line2 in splitted_urls:
        final_urls.append(line2)

send_request(final_urls)
'''
array_length = len(final_urls)
# start progress bar with calling execution functino
for i in tqdm(range(array_length), desc="\nLoading...", ascii=False, ncols=75):
    line = final_urls[i]
    send_request(line)
'''
f = open(output_filename, 'a+')
for line in results:
    line = line.strip()    
    f.write(line + "\n")
f.close()

print(colored("\nWe have finished\nCheck the output file: ", "green") + output_filename)

