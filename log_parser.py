# python log_parser.py -f skip/ -v       <-- TEST
# python log_parser.py -f logs/ -v       <-- TRUE

import os
import gzip
import collections
import argparse
from datetime import datetime

class logParser():
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
			
	def parseLogs(self, file, zip = 0):
		if zip: 
			fh = gzip.open(file)
		else:
			fh = open(file)
		keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
		 
		for line in fh:
			try:
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
					
				print "referrer: ", referrer
					
					
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

	def parseDirectory(self, dirs, chat):
		for filename in os.listdir(dirs):	
			if os.path.isdir(os.path.join(dirs, filename)):
				if chat:
					print "..Checking directory:", filename
				self.parseDirectory(os.path.join(dirs, filename), chat)
				continue
			if not filename.startswith("access.log"):
				if chat:
					print "..Skipping unknown file:", filename
				continue
				
			mode, inode, device, nlink, uid, gid, size, atime, mtime, ctime = os.stat(os.path.join(dirs, filename))
			self.files.append((os.path.join(dirs, filename), datetime.fromtimestamp(mtime), size)) # Append 3-tuple to list
			
			if filename.endswith(".gz"):
				if chat:
					print "..Checking compressed file:", filename
				self.parseLogs(os.path.join(dirs, filename),1)
				continue
			if chat:
				print "\nGoing to process:", filename
			
			self.parseLogs(os.path.join(dirs, filename))
	
	def displaySummary(self):
		total = sum(self.d.values())
		print "=============================================\nTotal lines with requested keywords:", total
		for keyword, hits in sorted(self.d.items(), key = lambda (keyword,hits):-hits):
			print "%s => %d (%.02f%%)" % (keyword, hits, hits * 100 / total)
			
		print "\nTop 5 requested URLs:"
		i = 0
		for path, hits in sorted(self.p.items(), key = lambda (path,hits):-hits):
			print "%s => %d (%.02f%%)" % (path, hits, hits * 100 / total)
			i += 1
			if i >= 5:
				break
				
		print "\nTop 5 requested users and their traffic:"
		i = 0
		for user, hits in sorted(self.u.items(), key = lambda (user,hits):-hits):
			print "%s => %d (%.02f%%) => %s" % (user, hits, hits * 100 / total, self.humanize(self.t[user]))
			i += 1
			if i >= 5:
				break
		
		print "\nTop 5 faulty URLs:"
		i = 0
		for path, hits in sorted(self.e.items(), key = lambda (path,hits):-hits):
			print "%s => %d (%.02f%%)" % (path, hits, hits * 100 / total)
			i += 1
			if i >= 5:
				break
		print "=============================================\n\n"
		
		
	def analyzeFiles(self): 
		print "Analyze files"
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
logParser.parseDirectory(args.folder, args.verbose)
		
logParser.displaySummary()
logParser.analyzeFiles()

