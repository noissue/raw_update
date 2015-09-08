#   script.rawrestore, NO Issue's XBMC Update Tool
#   Copyright (C) 2015  Adam Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib, urllib2, re, time
import xbmcgui,xbmcplugin
import os
import zipfile

homePath = xbmc.translatePath('special://home')
addonPath = os.path.join(os.path.join(homePath, 'addons'),'script.rawupdate')
mediaPath = os.path.join(addonPath, 'media')
addonName = "Raw Update"

def mainMenu():
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addItem('Update','url', 1, os.path.join(mediaPath, "update.png"))

def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok


#######################################################################
#						Parses Choice
#######################################################################
      
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
							
	return param  
	
#######################################################################
#						Perform Update
####################################################################### 

def runUpdate():
	progress = xbmcgui.DialogProgress()
	progress.create('Progress', 'Performing Update')
	
	progress.update( 0, "", "Downloading Update File", "")	
	
	zipPath = os.path.join(addonPath, 'backup.zip')
	try:
		urllib.urlretrieve("http://158.69.223.146/root/update_script_public/raw/master/backup.zip", zipPath)
	except:
		xbmcgui.Dialog().ok(addonName, "There was an issue downloading backup file,", "please check your internet connection and try again later.", " ")
		progress.close()
		return
	
	progress.update( 33, "", "Opening Update File", "")	
		
	try:
		zf = zipfile.ZipFile(zipPath, 'r')
	except RuntimeError:
		xbmcgui.Dialog().ok(addonName, "There was an issue opening backup file,", "this may be worth noting to the developers.", " ")
		progress.close()
		return
	
	progress.update( 40, "", "Applying Update File", "")		
		
	#Python 2.6+ provides transversal attack protection but download from trusted sources only
	try:
		zf.extractall(homePath)
	except:
		xbmcgui.Dialog().ok(addonName, "There was an issue applying backup file,", "this may be worth noting to the developers.", " ")
		progress.close()
		return
		
	progress.update( 90, "", "Cleaning up", "")
		
	zf.close()
	os.remove(zipPath)
	
	progress.update( 100, "", "Done", "")
	
	xbmc.sleep( 100 )
	progress.close()
	

#######################################################################
#						START MAIN
#######################################################################              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        mainMenu()
       
elif mode==1:
		runUpdate()



xbmcplugin.endOfDirectory(int(sys.argv[1]))
