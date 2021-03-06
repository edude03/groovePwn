#!/usr/bin/python

import os, shutil, ID3, errno

def organiseMP3(tempFileName):
	try:
		tags = ID3.ID3(tempFileName)
		
		fileName = "%s.mp3"%(tags["TITLE"],)
		try:
			songDir = os.path.join(tags["ARTIST"], tags["ALBUM"])
		except KeyError:
			songDir = tags["ARTIST"]
		
		# Make a folder for the track and move it there
		try:
			os.makedirs(songDir)
		except OSError, e:
			if e.errno != errno.EEXIST:
				# Not a "file exists" error: propogate on
				raise e
		target = os.path.join(songDir, fileName)
		
		shutil.move(tempFileName, target)
		
		print "Pwn't an MP3 to: %s"%(target,)
	except ID3.InvalidTagError:
		# Delete the tempoary file
		print "Tag data missing but still stored."
		shutil.move(tempFileName, "./")
	except KeyError:
		# Some very important tag data is missing: can't do anything
		print "Tag data missing but still stored."
		shutil.move(tempFileName, "./")
	except Exception, e:
		print "Some unknown encoding/identification error occurred: Temp stored.", e
		shutil.move(tempFileName, "./")
