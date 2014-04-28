'''Copyright [2014] [Kristian Kissling]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

import urllib.request
import webbrowser
from socket import timeout

   ''' This little program is a hack and not optimised yet. 
   Webradio "Radio Nacional" uses changing IP addresses. This script checks if the current IP address is still valid. If it is not, it searches a range of given IPs for a working one. If successful, it writes the new IP in "ip.txt" and starts a browser, to switch the existing "Radio-Nacional"-URL to the new found IP. The backend it modifies, is running as a webserver on an local IP Radio Hardware and is using 192.168.2.100 as IP address. 
   '''
   
# Get current IP address from file
def catch_ip_adr():
    with open("ip.txt", "rt") as ip_file:
        ip_adr = ip_file.read()
        return ip_adr

# Check current IP address for availability. If not, try_next_ip ()
def conn_test():
	try:
		new_url = urllib.request.urlopen(str(catch_ip_adr()),timeout=2)
		new_server_status = new_url.getcode()
		print('Server is alive and kicking, everything shoud be fine. Good Bye!')
		quit()
	except urllib.error.HTTPError:
		pass
		print('Error: Current IP is not available. Trying other IP addresses.')
		try_next_ip()
	except urllib.error.URLError:
		pass
		print('Error: Current IP is not available. Trying other IP adresses.')
		try_next_ip()

# Read IP addresses from adrlist.txt and test each for availability with conn_test_new()
def try_next_ip():
	with open("adrlist.txt", "rt") as ip_list:
		all_ips = ip_list.readlines()
		for line in all_ips:
			conn_test_new(line)

# If IP address is available, call change_url()
def conn_test_new(line):
	try:
		new_url = urllib.request.urlopen(line,timeout=2)
		new_server_status = new_url.getcode()
		change_url(line)
	except urllib.error.HTTPError:
		pass
	except urllib.error.URLError:
		pass

# Put working IP address in ip.txt and open default browser with a working url, that modifies webradio backend
def change_url(line):
	print('Writing '+line+' in file ip.txt...')
	with open("ip.txt", "wt") as out_file:
		out_file.write(line)
		tab = 2
		# This opens a local server backend and modifies the address of a network radio.
		rnurl = "http://192.168.2.100/all/cgi-bin/same/op?modn_en=Radio+Nacional&1="+line+"%3F&radiotyp=1&tag=UB"
		webbrowser.open(rnurl,new=tab)
		print ('Starting Default Browser and finishing.')
		quit()

conn_test()
