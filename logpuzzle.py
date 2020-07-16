import os
import re
import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve
import argparse

def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    puzzle_urls = []
    with open(filename, 'r') as log_file:
        log_list = log_file.read().split('\n')
        log_list = list(filter(lambda x: '/puzzle/' in x, log_list))
        for url in log_list:
            url_result = re.findall(r'GET (\S+) HTTP', url)
            puzzle_urls.append(url_result[0])
    url_list = create_urls(puzzle_urls)
    url_list = list(set(url_list))
    sorted_urls = sorted(url_list, key=return_last_word)
    def extract_host_name(url):
        """returns the host name from a given url"""
    host = re.findall(r'GET (\S+) HTTP', url)
    return sorted_urls

def create_urls(urls):
    front = 'http://code.google.com'
    url_return = [front + url for url in urls]
    return url_return

def return_last_word(url):
    return re.findall(r'-(....).jpg', url)

def add_prefixes(filename, host_list):
    """adds server prefixes to the urls in host_list"""
    server_name = "https://" + re.findall(r'\S+\_(\S+)', filename)[0]
    completed_url_list = [server_name + host for host in host_list]
    return completed_url_list

def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print('dir made')
    index_html = '<html><body>'
    for index, url in enumerate(img_urls):
        image_name = 'img' + str(index)
        print('Retrieving {}'.format(url))
        urlretrieve(url, dest_dir + '/' + image_name)
        index_html += '<img src={}></img>'.format(image_name)
    index_html += '</body></html>'
    with open(dest_dir + '/index.html', 'w') as w_index:
        w_index.write(index_html)

def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')
    return parser

def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    img_urls = read_urls(parsed_args.logfile)
    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))
        
if __name__ == '__main__':
    main(sys.argv[1:])