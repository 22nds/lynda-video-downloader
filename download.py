import os
import re
from urllib.request import urlopen

import youtube_dl

# SETTINGS
# Lynda.com LOGIN details
USERNAME = 'your-username'
PASSWORD = 'your-password'

# Download subtitles of the videos
SUBTITLES = True

# Location of the list of course URLs
LINKS = 'links.txt'

HOME_DIR = os.getcwd()

def move_to_course_directory(title):
    """Check if current directory is home directory. If not, change to it.
    Make a course directory and move to it.
    If course directory already exists, just move to it.
    If everything fails break the program.
    """

    # Move to home directory if we are somewhere else (e.g. course subdir)
    if os.getcwd() != HOME_DIR:
        os.chdir(HOME_DIR)

    try:
        # Make a directory with course name
        os.mkdir(title)
        os.chdir(title)
    except FileExistsError:
        # Position yourself in course directory
        os.chdir(title)
    except:
        print('Could not create subdirectory for the course: {}'.format(title))


def get_title(url):
    """ Get course title for creation of the video folder.
    """
    try:
        # REGEX pattern for URL and Course name
        pattern = re.compile(r'(http[s]?://?[^/\s]+/[^/\s]+/)(.*)/(.*)')

        # Get the COURSE NAME for new folder
        title = pattern.search(url).group(2)
        return (title)
    except:
        print('Could not parse the course URL.')

def get_videos(url):
    """Download all videos in the course.
    """

    # Lynda.com login and video filename options
    options = {
        'username': USERNAME,
        'password': PASSWORD,
        'outtmpl': u'%(playlist_index)s-%(title)s.%(ext)s',
	'writesubtitles': SUBTITLES,
        'allsubtitles': SUBTITLES
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
    except:
        print('Could not download the video in course: {}'.format(url))


def main():
    """Process the list of courses.
    """

    for url in open(LINKS):
        try:
            print(url)
            title = get_title(url)
            print(title)
            move_to_course_directory(title)
            get_videos(url)
        except:
            print('Something went wrong.')

    print('DONE.')


if __name__ == '__main__':
    main()
