import os
import gzip
import collections

import argparse
import socket

from datetime import datetime
from urlparse import urlparse
from threading import Thread

import pygeoip
from pygeoip import GeoIP

from lxml import etree
from lxml.cssselect import CSSSelector

from jinja2 import Environment, FileSystemLoader
import codecs
import webbrowser

from flask import Flask, request


class logParser():
	chat = 0
	d = collections.Counter() #Keyword counter
	u = collections.Counter() #User counter
	t = collections.Counter() #Traffic counter
	p = collections.Counter() #Path counter
	e = collections.Counter() #Error counter
	r = collections.Counter() #Referrer counter
	c = collections.Counter() #Country counter
	files = []
	first = datetime.now()
	last = datetime.strptime("1000","%Y")
	

	def is_valid_ipv4_address(self, address):
		try:
			socket.inet_pton(socket.AF_INET, address)
		except AttributeError:  # no inet_pton here, sorry
			try:
				socket.inet_aton(address)
			except (socket.error, AttributeError):
				return False
			return address.count('.') == 3
		except (socket.error, AttributeError):  # not a valid address
			return False

		return True

	def is_valid_ipv6_address(self, address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
		except (socket.error, AttributeError):  # not a valid address
			return False
		return True
	
	def humanize(self, bytes):
		if bytes < 1024:
			return "%d B" % bytes
		elif bytes < 1024 ** 2:
			return "%.1f kB" % (bytes / 1024.0)
		elif bytes < 1024 ** 3:
			return "%.1f MB" % (bytes / 1024.0 ** 2)
		else:
			return "%.1f GB" % (bytes / 1024.0 ** 3)
			
	def parseLogs(self, file):
		#If the file is packed, then open it. Otherwise just open the file.
		if file.endswith(".gz"):
			fh = gzip.open(file)
		else:
			fh = open(file)
		keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
		 
		for line in fh:
			try:
				#Example line: 157.55.39.242 - - [20/Mar/2016:06:42:47 +0200] "GET /~jpoial/docs/api/index.html?java/awt/event/ContainerAdapter.html HTTP/1.1" 200 1417 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
				#Split line to extract data
				source, request, response, referrer, _, agent, _ = line.split("\"")
				method, path, protocol = request.split(" ")
				_, user, file = path.split("/",3)
				_, code, traffic = response.split(" ",2)
				ips, rfc, uid, timez, zone = source.split(" ",4)
				
				#Format date to make timeline
				stamped = datetime.strptime(timez,"[%d/%b/%Y:%H:%M:%S")
				if(self.first > stamped):
					self.first = stamped
				if(self.last < stamped):
					self.last = stamped
					
				#Check for referers
				_, netloc, refpath, _, _, _ = urlparse(referrer)
				if netloc == "":
					netloc = "direct"
				self.r[netloc] += 1
				
				#mark visited countrys
				if ips:
					if self.is_valid_ipv4_address(ips):
						self.c[self.gi.country_code_by_addr(ips).lower()] += 1
					if self.is_valid_ipv6_address(ips):
						self.c[self.gi6.country_code_by_addr(ips).lower()] += 1
				
				#mark what was requested
				self.p[path] += 1
				if (code[:1] == "5") or (code[:1]) == "4":
					self.e[path] += 1
					
				#mark requested users
				if user[:1] == "~":
					self.u[user] += 1
					self.t[user] += int(traffic)
				
				#mark keyword counter
				for keyword in keywords:
					if keyword in agent:
						self.d[keyword] += 1
						break
			except ValueError:
				pass

	def parseDirectory(self, dirs):
		for filename in os.listdir(dirs):	
			if os.path.isdir(os.path.join(dirs, filename)):
				if self.chat:
					print "..Checking directory:", filename
				self.parseDirectory(os.path.join(dirs, filename))
				continue
			if not filename.startswith("access.log"):
				if self.chat:
					print "..Skipping unknown file:", filename
				continue
				
			mode, inode, device, nlink, uid, gid, size, atime, mtime, ctime = os.stat(os.path.join(dirs, filename))
			self.files.append((os.path.join(dirs, filename), datetime.fromtimestamp(mtime), size)) # Append 3-tuple to list
			
			if filename.endswith(".gz"):
				if self.chat:
					print "..Checking compressed file:", filename
				self.parseLogs(os.path.join(dirs, filename))
				continue
			if self.chat:
				print "\nGoing to process:", filename
			
			self.parseLogs(os.path.join(dirs, filename))
	
	def displaySummary(self):
		print "============================================="
		
		print "Total lines with requested keywords:", sum(self.d.values())
		for keyword, hits in self.d.most_common():
			print "%s => %d (%.02f%%)" % (keyword, hits, hits * 100 / sum(self.d.values()))
			
		print "\nTop 5 requested URLs (total: %d):" % (sum(self.p.values()))
		for path, hits in self.p.most_common(5):
			print "%s => %d (%.02f%%)" % (path, hits, hits * 100 / sum(self.p.values()))
		
		print "\nTop 5 requested users and their traffic (total: %d):" % (sum(self.u.values()))
		for user, hits in self.u.most_common(5):
			print "%s => %d (%.02f%%) => %s" % (user, hits, hits * 100 / sum(self.u.values()), self.humanize(self.t[user]))
		
		print "\nTop 5 faulty URLs (total: %d):" % (sum(self.e.values()))
		for path, hits in self.e.most_common(5):
			print "%s => %d (%.02f%%)" % (path, hits, hits * 100 / sum(self.e.values()))
			
		print "\nTop 5 referers (total: %d):" % (sum(self.r.values()))
		for host, hits in self.r.most_common(5):
			print "%s => %d (%.02f%%)" % (host, hits, hits * 100 / sum(self.r.values()))
			
		maxHits = max(self.c.values())
		startColor = 240 	#Blue
		endColor = 360 		#Red
		colRange = endColor - startColor
		
		print "\nTop 10 countrys (Max: %d):" % maxHits
		
		for country, hits in self.c.most_common(10):
			pros = hits * 100 / maxHits
			color = ((colRange/100)*pros)+startColor
			print "%s => %d (%.02f%%)" % (country, hits, pros)
			
		print "=============================================\n\n"
		
		
	def analyzeFiles(self): 
		print "Analyze files"
		print "============================================="
		
		self.files.sort(key = lambda(filename, dt, size):dt)
		for filename, dt, size in self.files:
			print filename, dt, self.humanize(size)
		 
		print "============================================="
		print "Newest file is:", self.files[-1][0]
		print "Oldest file is:", self.files[0][0]
		print "============================================="
		print "Newest entry is:", self.last
		print "Oldest entry is:", self.first
		
		
	def paintWorld(self): 
		document =  etree.parse(open(str(self.template)+'world.svg'))
		
		print "\n============================================="
		print "Painting World"
		
		startColor = 240 	#Blue
		endColor = 360 		#Red
		startLight = 95 	#Light
		endLight = 25 		#Dark
		colRange = endColor - startColor
		lightRange = startLight - endLight
		maxHits = max(self.c.values());
		
		for country, hits in self.c.most_common():
			if country:
				sel = CSSSelector("#" + str(country))
				
				pros = hits * 100 / maxHits
				color = ((colRange/100)*pros)+startColor
				lightness = startLight-((lightRange*pros)/100)
				for j in sel(document):
					j.set("style", "fill: hsl(" + str(color) + ", 100%, " + str(lightness) + "%)")
					
					# Remove styling from children
					for i in j.iterfind("{http://www.w3.org/2000/svg}path"):
						i.attrib.pop("class", "")
		 
		with open(str(self.build)+"highlighted.svg", "w") as fh:
			fh.write(etree.tostring(document))

		#url = "file://" + os.path.realpath(str(self.build)+"output.html") + " &"
		#os.system("start \"\" "+str(url))
		

		
#Command build
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder',  help="Path to log files", default="logs/")
parser.add_argument('-t', '--template',  help="Path to template folder", default="templates/")
parser.add_argument('-b', '--build',  help="Path to build folder", default="build/")
parser.add_argument('-v', '--verbose', help="Increase verbosity", action="store_true")
args = parser.parse_args()

#create logParser
logParser = logParser()

#Set up geoip 
logParser.gi = GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
logParser.gi6 = GeoIP("GeoIPv6.dat", pygeoip.MEMORY_CACHE)

#Set some settings
logParser.template = args.template
logParser.build = args.build
if args.verbose: logParser.chat = 1;


#Scan for log files
logParser.parseDirectory(args.folder)
		
#Display whats found and analyze stuffs
logParser.displaySummary()
logParser.analyzeFiles()
logParser.paintWorld()

#Create Flask
app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome to the not-so-good Apache 2 log parser!"

@app.route("/report/")
def report():
	env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),trim_blocks=True)
	user_bytes = sorted(logParser.items(), key = lambda item:item[1], reverse=True)

	with codecs.open(str(args.build)+"output.html", "w", encoding="utf-8") as fh:
		fh.write(env.get_template(str(args.template)+"report.html").render(locals()))

	return env.get_template(str(self.build)+"output.html")


if __name__ == '__main__':
	app.run(debug=True)
	
