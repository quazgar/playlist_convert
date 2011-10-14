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
    for trackList in plXML.getElementsByTagName("contents"):
        convertTrackList(trackList)
    plXML.unlink()

def convertTrackList(list):
    tracks = []
    iNumber = 0
    for track in list.getElementsByTagName("track"):
        iNumber += 1
        (interpret, title, duration) = parseTrack(track)
        tracks.append((iNumber, interpret, title, duration))

    applyTracks(tracks)

def parseTrack(track):
    creator = getText(track, "creator")
    title = getText(track, "title")
    duration = getDuration(track)

    return (creator, title, duration)

def getText(track, name):
    elements = track.getElementsByTagName(name)
    if elements is not None and elements.item(0) is not None:
        k = elements.item(0).firstChild
        if k.nodeType == k.TEXT_NODE:
            return k.nodeValue

    return ""

def getDuration(track):
    duration = getText(track, "duration")
    if duration == "" :
        return duration

    seconds = int(duration) / 1000
    minutes = seconds / 60
    seconds = seconds - minutes*60
    return ("%d:%02d" % (minutes, seconds))

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
