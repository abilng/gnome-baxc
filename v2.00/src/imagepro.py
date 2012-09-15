import os
import string
from xml.dom.minidom import Document
import datetime

extentions=['.jpg','.png','.jpeg']

#finding is-image file
def isimage(filename):
	for ext in extentions:
		if filename.find(ext) == -1:
			pass
		else:
			return True
	return False

def ask_ok(prompt):
	retries=2
	complaint='Yes or no, please!'
	while True:
		ok = str(input(prompt))
		if ok in ('y', 'ye', 'yes','Y'):
			return True
		elif ok in ('n', 'no', 'nop','N', 'nope'):
			return False
		retries = retries - 1
		if retries < 0:
			raise IOError('refusenik user')
		print (complaint)

aboutmsg="""
	<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n
	<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n
	p, li { white-space: pre-wrap; }\n
	</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n
	<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Gnome-BAXC</span></p>\n
	<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600;\"></p>\n
	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"baxc50.png\" />Version 1.01</p>\n
	<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n
	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Gnome-BAXC </span><span style=\" font-size:11pt;\">(Gnome -</span><span style=\" font-size:11pt; font-weight:600;\">Ba</span><span style=\" font-size:11pt;\">ckground </span><span style=\" font-size:11pt; font-weight:600;\">X</span><span style=\" font-size:11pt;\">ML </span><span style=\" font-size:11pt; font-weight:600;\">C</span><span style=\" font-size:11pt;\">reator) generates xml code for background slide show of gnome.</span></p>\n
	<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"></p>\n
	<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"></p></body></html>
	"""

def finalmsg(outfile,count):
	msg = '\n Added '+str(count)+'image(s).\nOutput file:'+outfile+'\n'
	return msg



class xmlCreator():
	def __init__(self):
		self.images=list()

	def load(self,outfile):
		g3cmd='GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri \'file://'+str(outfile)+'\' 2>/dev/null'
		g2cmd='gconftool -s \'/desktop/gnome/background/picture_filename\' \''+str(outfile)+'\' -t string 2>/dev/null'
		print ("GNOME 3: "+ g3cmd)
		print ("GNOME 2: "+ g2cmd)
		if os.system(g3cmd) == 0:
			pass
		else:
			os.system(g2cmd)

	def close(self,outfile):
		if len(self.images) == 0:
			os.remove(outfile)
		else:
			self.load(outfile)

	def addimage(self,image):
			self.images.append(image)

	def getimagecount(self):
		return len(self.images)

	def getimages(self,directory,askprompt = False):
		path = os.path.abspath(directory)+'/'
		dirs = os.listdir(path)
		dirs.sort()
		for i in dirs:
			if isimage(i):
				if askprompt==False :
					self.images.append((path + i))
				elif ask_ok('Add '+i+' ?:'):
					image.append((path + i))
		return self.images

	def create_xml(self, display_time, transition_time = 5):
		xmldoc = Document()
		background = xmldoc.createElement('background')
		xmldoc.appendChild(background)

		starttime = xmldoc.createElement('starttime')
		sTime = datetime.datetime.now()
		year = xmldoc.createElement('year')
		year.appendChild(xmldoc.createTextNode('%s' % sTime.year))
		starttime.appendChild(year)
		month = xmldoc.createElement('month')
		month.appendChild(xmldoc.createTextNode('%s' % sTime.month))
		starttime.appendChild(month)
		day = xmldoc.createElement('day')
		day.appendChild(xmldoc.createTextNode('%s' % sTime.day))
		starttime.appendChild(day)
		hour = xmldoc.createElement('hour')
		hour.appendChild(xmldoc.createTextNode('%s' % sTime.hour))
		starttime.appendChild(hour)
		minute = xmldoc.createElement('minute')
		minute.appendChild(xmldoc.createTextNode('%s' % sTime.minute))
		starttime.appendChild(minute)
		second = xmldoc.createElement('second')
		second.appendChild(xmldoc.createTextNode('%s' % sTime.second))
		starttime.appendChild(second)
		background.appendChild(starttime)

		for i in range(len(self.images)):
			currentImage = self.images[i]
			try:
				next = self.images[i + 1]
			except IndexError:
				next = self.images[0]

			static = xmldoc.createElement('static')

			duration = xmldoc.createElement('duration')
			duration.appendChild(xmldoc.createTextNode("%s.0" % display_time))
			static.appendChild(duration)

			file = xmldoc.createElement('file')
			file.appendChild(xmldoc.createTextNode(currentImage))
			static.appendChild(file)

			background.appendChild(static)

			transition = xmldoc.createElement('transition')

			duration = xmldoc.createElement('duration')
			duration.appendChild(xmldoc.createTextNode("%s.0" % transition_time))
			transition.appendChild(duration)

			transitionFrom = xmldoc.createElement('from')
			transitionFrom.appendChild(xmldoc.createTextNode(currentImage))
			transition.appendChild(transitionFrom)

			transitionTo = xmldoc.createElement('transitionTo')
			transitionTo.appendChild(xmldoc.createTextNode(next))
			transition.appendChild(transitionTo)

			background.appendChild(transition)

		return xmldoc.toxml()

