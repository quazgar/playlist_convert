"""Module for parsing k3b files."""

from string import Template
import xml.dom.minidom
import sys
import zipfile

def parse(infile_name):
    """Parses the file with the given name."""

    k3b_file = zipfile.ZipFile(infile_name)
    xml_file = k3b_file.open("maindata.xml")

    plXML = xml.dom.minidom.parse(xml_file)
    track_list = plXML.getElementsByTagName("contents")[0]
    tracks = convertTrackList(track_list)
    plXML.unlink()
    return tracks

def convertTrackList(list):
    tracks = []
    iNumber = 0
    for track in list.getElementsByTagName("track"):
        iNumber += 1
        (interpret, title, duration) = parseTrack(track)
        tracks.append((iNumber, interpret, title, duration))

    #applyTracks(tracks)
    return tracks

def parseTrack(track):
    artist = getText(track, "artist")
    title = getText(track, "title")
    duration = getText(track, "index0")[0:-3]

    return (artist, title, duration)

def getText(track, name):
    elements = track.getElementsByTagName(name)
    if elements is not None and elements.item(0) is not None:
        k = elements.item(0).firstChild
        if k.nodeType == k.TEXT_NODE:
            return k.nodeValue

    return ""

def applyTracks(tracks):
    indices = ""
    artists = ""
    titles = ""
    times = ""
    newline = "&#x85;"
    for track in tracks:
        indices += str(track[0])
        artists += track[1]
        titles += track[2]
        times += track[3]

        if track is not tracks[-1]:
            indices += newline
            artists += newline
            titles += newline
            times += newline

    inFile = open('/home/daniel/local/share/playlists/playlist_template.svg',
                  'r')
    inString = inFile.read()

    # outString = inString % {'numbers': indices,
    #                         'artists': artists,
    #                         'titles': titles,
    #                         'times': times}
    outString = Template(inString) \
                .substitute({'numbers': indices,
                             'artists': artists,
                             'titles': titles,
                             'times': times})
    print outString

# def tracks2csv(tracks):
    
