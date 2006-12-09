
#
# gPodder (a media aggregator / podcast client)
# Copyright (C) 2005-2006 Thomas Perl <thp at perli.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA  02110-1301, USA.
#


#
#  liblocdbwriter.py -- rss output writer for your downloaded feeds
#  thomas perl <thp@perli.net>   20060109
#
#

import codecs

from datetime import datetime
from xml.sax import saxutils

import libgpodder

class writeLocalDB( object):
    ofile = None
    
    def __init__( self, filename, channel):
        self.ofile = codecs.open( filename, "w", 'iso-8859-1', 'replace')
        self.ofile.write( '<?xml version="1.0" encoding="ISO-8859-1"?>'+"\n")
        self.ofile.write( '<!-- '+_('local download database, generated by gPodder')+' -->'+"\n")
        self.ofile.write( '<rss version="2.0">'+"\n")
        self.ofile.write( '<channel>'+"\n")
        self.ofile.write( '<pubDate>' + datetime.now().ctime() + '</pubDate>'+"\n")
        
        self.ofile.write( '<title>'+saxutils.escape(channel.title)+'</title>'+"\n")
        self.ofile.write( '<description><![CDATA['+channel.description+']]></description>'+"\n")
        self.ofile.write( '<link>'+channel.link+'</link>'+"\n")
        self.ofile.write( '<language>'+channel.language+'</language>'+"\n")
        self.ofile.write( '<webMaster>'+channel.webMaster+'</webMaster>'+"\n")
        self.writeMetadata( channel)
        
        for item in channel:
            self.addItem( item)
            
        self.close()

    def writeMetadata( self, channel):
        self.ofile.write( '<gpodder:info')
        self.ofile.write( ' nosync="%s"' % (str(not channel.sync_to_devices).lower()))
        self.ofile.write( ' music="%s"' % (str(channel.is_music_channel).lower()))
        self.ofile.write( ' playlist="%s"' % (channel.device_playlist_name))
        self.ofile.write( '/>'+"\n")

    def writeEpisodeMetadata( self, episode):
        self.ofile.write( '<gpodder:info />'+"\n")

    def close( self):
        self.ofile.write( '</channel>'+"\n")
        self.ofile.write( '</rss>'+"\n")
        self.ofile.close()

    def addItem( self, item):
        self.ofile.write( '<item>'+"\n")
        self.ofile.write( '<title>'+saxutils.escape(item.title)+'</title>'+"\n")
        self.writeEpisodeMetadata( item)
        self.ofile.write( '<description><![CDATA['+item.description+']]></description>'+"\n")
        self.ofile.write( '<url>'+saxutils.escape(item.url)+'</url>'+"\n")
        self.ofile.write( '<link>'+saxutils.escape(item.link)+'</link>'+"\n")
        self.ofile.write( '<guid>'+saxutils.escape(item.link)+'</guid>'+"\n")
        self.ofile.write( '<pubDate>'+saxutils.escape(item.pubDate)+'</pubDate>'+"\n")
        self.ofile.write( '<mimeType>'+saxutils.escape(item.mimetype)+'</mimeType>' + "\n")
        self.ofile.write( '</item>'+"\n")


