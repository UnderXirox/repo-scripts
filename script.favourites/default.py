import os, sys
import xbmc, xbmcgui, xbmcaddon
from xml.dom.minidom import parseString

__addon__ = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')

def log(txt):
    message = 'script.favourites: %s' % txt
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)
    
class Main:
    def __init__( self ):
        self.WINDOW = xbmcgui.Window( 10000 )
        self._clear_properties()
        self._read_file()
        self._parse_String()
        self._fetch_favourites()
        self.doc.unlink()

    def _clear_properties( self ):
        for count in range( 20 ):
            # clear Property
            self.WINDOW.clearProperty( "favourite.%d.path" % ( count + 1, ) )
            self.WINDOW.clearProperty( "favourite.%d.name" % ( count + 1, ) )
            self.WINDOW.clearProperty( "favourite.%d.thumb" % ( count + 1, ) )

    def _read_file( self ):
        # Set path
        self.fav_dir = xbmc.translatePath( 'special://profile/favourites.xml' )
        # Check to see if file exists
        if (os.path.isfile( self.fav_dir ) == False):
            self.favourites_xml = '<favourites><favourite name="Can Not Find favourites.xml">-</favourite></favourites>'
        else:
            # read file
            self.fav = open( self.fav_dir , 'r')
            self.favourites_xml = self.fav.read()
            self.fav.close()

    def _parse_String( self ):
        self.doc = parseString( self.favourites_xml )
        self.favourites = self.doc.documentElement.getElementsByTagName ( 'favourite' )

    def _fetch_favourites( self ):
        # Go through each favourites
        count = 0
        for self.doc in self.favourites:
            self.fav_path = self.doc.childNodes [ 0 ].nodeValue
            # add return 
            if 'RunScript' not in self.fav_path: 
                self.fav_path = self.fav_path.rstrip(')')
                self.fav_path = self.fav_path + ',return)'
            if (sys.argv[ 1 ] == 'playlists=play'):
                if 'playlists/music' in self.fav_path: self.fav_path = self.fav_path.replace( 'ActivateWindow(10502,', 'PlayMedia(' )
                if 'playlists/video' in self.fav_path: self.fav_path = self.fav_path.replace( 'ActivateWindow(10025,', 'PlayMedia(' )
            # set properties
            self.WINDOW.setProperty( "favourite.%d.path" % ( count + 1, ) , self.fav_path )
            self.WINDOW.setProperty( "favourite.%d.name" % ( count + 1, ) , self.doc.attributes [ 'name' ].nodeValue )
            try: self.WINDOW.setProperty( "favourite.%d.thumb" % ( count + 1, ) , self.doc.attributes [ 'thumb' ].nodeValue )
            except: pass
            count = count+1

if ( __name__ == "__main__" ):
        log('script version %s started' % __addonversion__)
        Main()
log('script stopped')
