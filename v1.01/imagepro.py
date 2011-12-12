import os
import string
import msg
path =os.getenv('HOME')+"/Pictures"
path = os.path.abspath(path)+'/'
dirs = os.listdir(path)
dirs.sort()

class image:
	count=0
	extentions=['.jpg','.png','.jpeg']
	start=None

def close(outfile):
	if image.count==0:
		os.remove(outfile)
		print ('No jpg image on that dir(or u said \'not to add\')')
	else:
		print ('\n added'+str(image.count)+'image(s) \noutput file:'+outfile+'\n')
		print ('load file by \n')
		print ('GNOME 3:\" GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri \'file://'+outfile+'\' \"\n')
		print ('GNOME 2:\" gconftool -s \'/desktop/gnome/background/picture_filename\' \''+outfile+'\' -t string \"\n ')
 
#finding is-image file
def isimage(i):
	for ext in image.extentions:
		if i.find(ext) == -1:
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
			image.count=0
			close()
			raise IOError('refusenik user')
		print (complaint)

def add(i):
	if image.count==0:
		image.count=image.count+1
		f.write(s1+i+s2+i+s3)
		image.start=i
	else:
		s0='\n<to>'+path+i+'</to> \n</transition>'
		f.write(s0+s1+i+s2+i+s3)
		image.count=image.count+1

def askadd(i):
	if args.action==False :
		add(i)
	elif ask_ok('Add '+i+' ?:'):
		add(i)

		

