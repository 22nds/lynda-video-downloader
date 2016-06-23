import os
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup, SoupStrainer
import youtube_dl

# TODO: Add your Lynda.com LOGIN between quotes.
USERNAME = ''
PASSWORD = ''

# TODO: Remove the two examples and course URLs.
COURSES = [
    'https://www.lynda.com/HTML-5-tutorials/HTML5-Managing-Browser-History/84811-2.html',
    'https://www.lynda.com/HTML-5-tutorials/HTML5-Video-and-Audio-in-Depth/80781-2.html'
]

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


def parse_url(url):
    """ Extract the short URL for link checking and
    Course title for creation of video folder.
    """

    try:
        # REGEX pattern for URL and Course name
        pattern = re.compile(r'(http[s]?://?[^/\s]+/[^/\s]+/)(.*)/(.*)')

        # Get SHORTENED URL for youtube_dl
        url_part = pattern.search(url).group(1)

        # Get the COURSE NAME for new folder
        title = pattern.search(url).group(2)

        return (pattern, url_part, title)
    except:
        print('Could not parse the course URL.')


def read_html(url):
    """Return the HTML of the course page."""

    try:
        page = urlopen(url).read()
        return page
    except:
        print('Could not open the page to get HTML.')


def get_videos(page, url_part, pattern):
    """Get all links, check if they are linked to the course and
    download the videos.
    """

    # Lynda.com login and video filename options
    options = {
        'username': USERNAME,
        'password': PASSWORD,
        'outtmpl': u'%(id)s-%(title)s.%(ext)s'
    }

    # Pattern - only links with valid links in the URL
    tds = SoupStrainer('a', {'href': re.compile(pattern)})

    # Parse html and get the links. Add them to set to save only uniques.
    for link in BeautifulSoup(page, "html.parser", parse_only=tds):
        if url_part in link['href']:
            l = link['href']
            try:
                with youtube_dl.YoutubeDL(options) as ydl:
                    ydl.download([l])
            except:
                print('Could not download the video: {}.'.format(link['href']))
                print('Check your username, password and course URL.')
                continue


def main():
    """Process the list of courses."""

    for url in COURSES:
        try:
            pattern, url_part, title = parse_url(url)
            move_to_course_directory(title)
            page = read_html(url)
            get_videos(page, url_part, pattern)
        except:
            print('Something went wrong.')

    print('DONE.')


if __name__ == '__main__':
    main()
