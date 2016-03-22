import os
import gzip
import collections
import argparse
from datetime import datetime

class logParser():
	chat = 0
	d = collections.Counter()
	u = collections.Counter()
	t = collections.Counter()
	p = collections.Counter()
	e = collections.Counter()
	files = []
	first = datetime.now()
	last = datetime.strptime("1000","%Y")
	
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
		if file.endswith(".gz"):
			fh = gzip.open(file)
		else:
			fh = open(file)
		keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
		 
		for line in fh:
			try:
				#157.55.39.242 - - [20/Mar/2016:06:42:47 +0200] "GET /~jpoial/docs/api/index.html?java/awt/event/ContainerAdapter.html HTTP/1.1" 200 1417 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
				source, request, response, referrer, _, agent, _ = line.split("\"")
				method, path, protocol = request.split(" ")
				_, user, file = path.split("/",3)
				_, code, traffic = response.split(" ",2)
				time, rfc, uid, timez, zone = source.split(" ",4)
				
				stamped = datetime.strptime(timez,"[%d/%b/%Y:%H:%M:%S")
				if(self.first > stamped):
					self.first = stamped
				if(self.last < stamped):
					self.last = stamped
					
				#print "referrer: ", referrer
					
				self.p[path] += 1
				
				if (code[:1] == "5") or (code[:1]) == "4":
					self.e[path] += 1
					
				if user[:1] == "~":
					self.u[user] += 1
					self.t[user] += int(traffic)
				
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
		
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder',  help="Path to log files", default="logs/")
parser.add_argument('-v', '--verbose', help="Increase verbosity", action="store_true")
args = parser.parse_args()

logParser = logParser()
if args.verbose: logParser.chat = 1;
logParser.parseDirectory(args.folder)
		
logParser.displaySummary()
logParser.analyzeFiles()

