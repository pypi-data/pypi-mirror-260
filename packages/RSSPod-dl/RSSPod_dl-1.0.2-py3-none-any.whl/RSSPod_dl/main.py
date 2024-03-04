import requests
from bs4 import BeautifulSoup
import eyed3
from io import BytesIO
import os, argparse, time, socket
from alive_progress import alive_bar # Progress bar
import re

def collect_args():
  # Create the top-level parser
    parser = argparse.ArgumentParser(prog='podcast_downloader')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create the parser for the "download" command
    parser_download = subparsers.add_parser('download', help='download a single podcast')
    parser_download.add_argument('url', type=str, help='The URL of the podcast to download')
    parser_download.add_argument('--overwrite', action='store_true', help='Overwrite the output file if it already exists.')
    parser_download.add_argument('--output', type=str, default=os.getcwd(), help='The output directory for the downloaded podcasts.')

    # Create the parser for the "download_all" command
    parser_download_all = subparsers.add_parser('download_all', help='download multiple podcasts')
    parser_download_all.add_argument('--file', type=str, default='podlist.txt', help='A file containing URLs of podcasts to download. If no file is provided, "podlist.txt" in the current directory will be used.')
    parser_download_all.add_argument('--overwrite', action='store_true', help='Overwrite the output file if it already exists.')
    parser_download_all.add_argument('--output', type=str, default=os.getcwd(), help='The output directory for the downloaded podcasts.')

    # Parse and return the arguments
    args = parser.parse_args()

    # check output path is valid
    if os.path.isfile(args.output):
        raise ValueError('Output path is a file, please provide a valid directory path')
    
    os.makedirs(args.output, exist_ok=True)

    # check if the file exists
    if args.command == 'download_all' and not os.path.isfile(args.file):
        raise ValueError('File not found')

    return args

def clean_string(s):
    '''
    Remove non-ASCII characters from a string.
    '''
    return re.sub(r'[^\x00-\x7F]+', ' ', s) # thanks to https://stackoverflow.com/a/20078869/119527

def check_connection():
    host = 'www.google.com'  # Highly available website
    port = 80  # HTTP port
    try:
        sock = socket.create_connection((host, port), timeout=5)
        sock.close()
        return True
    except socket.error as ex:
        return False


def get_podcast_episods_number(url):
    '''
    Get the number of episodes of a podcast from its RSS feed.
    input: url (str) - URL of the podcast RSS feed
    output: (int) - The number of episodes of the podcast
    '''
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')

    # Find all item tags in the document (each item tag represents a podcast episode)
    items = soup.find_all('item')

    return len(items)


def get_podcast_name(url):
    '''
    Get the name of the podcast from its RSS feed.
    input: url (str) - URL of the podcast RSS feed
    output: (str) - The name of the podcast
    '''
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')

    # Get the podcast name
    podcast_name = soup.channel.title.text

    return podcast_name


def get_podcast_dict(file):
    '''
    Get the list of podcasts from a file.
    input: file (str) - Path to the file containing the list of podcasts
    output: (dict) - Dict of podcasts in the format {name: url}

    File format:
        name1:url1
        name2:url2
        #name3:url3 (skip line)
        ...
    '''
    dict_output = {}
    with open(file, 'r') as f:
        for line in f:
            if line[0] != '#':  # skip line if starts with #
                # Split the line into a name and a URL
                split_line = line[1:].strip('\n').split(':')
                name = split_line[0]
                url = ':'.join(split_line[1:])
        
                dict_output[name] = url
    
    return dict_output


def download_podcast(name, url, download_path, ovveride, dict_episod_summary, bar):
    '''
    Downloads and tags all the episodes of a podcast from its RSS feed.
    input: url (str) - URL of the podcast RSS feed
    input: download_path (str) - Path to the directory where the episodes will be downloaded
    '''

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')

    # Get the podcast name
    podcast_name = soup.channel.title.text

    # Find all item tags in the document (each item tag represents a podcast episode)
    items = soup.find_all('item')

    # Loop through each item
    for item in items:
    
        # Find the URL of the mp3 file
        mp3_url = item.find('enclosure')['url']
        # Send a GET request to the mp3 URL
        mp3_response = requests.get(mp3_url)
        # Get the episode title
        episode_title = item.find('title').text
        
        # Create a directory for the podcast
        podcast_dir = os.path.join(download_path, podcast_name)
        os.makedirs(podcast_dir, exist_ok=True)

        # Check if the file already exists 
        if ovveride or not os.path.exists(os.path.join(podcast_dir, f'{episode_title}.mp3')):

            # Get Metadata
            episode_link = item.find('link').text
            episode_published_date = item.find('pubDate').text
            episode_description = item.find('description').text if item.find('description') else None
            episode_author = item.find('itunes:author').text if item.find('itunes:author') else None
            episode_duration = item.find('itunes:duration').text if item.find('itunes:duration') else None
            episode_image = item.find('itunes:image')['href'] if item.find('itunes:image') else None
            episode_category = item.find('itunes:category')['text'] if item.find('itunes:category') else None
            
            # Save the mp3 file to the directory
            with open(os.path.join(podcast_dir, f'{episode_title}.mp3'), 'wb') as file:
                file.write(mp3_response.content)

            # Load the MP3 file
            audiofile = eyed3.load(os.path.join(podcast_dir, f'{episode_title}.mp3'))

            if audiofile.tag is None:
                # If not, create a new ID3 tag
                audiofile.initTag()
            
            # Set the metadata
            audiofile.tag.artist = clean_string(episode_author) if episode_author else None
            audiofile.tag.album = clean_string(podcast_name) if podcast_name else None
            audiofile.tag.title = clean_string(episode_title)  if episode_title else None
            audiofile.tag.comments.set("description", episode_description) if episode_description else None

            # Download the image
            image_response = requests.get(episode_image)

            # Set the image as album art
            audiofile.tag.images.set(3, image_response.content, "image/jpeg") #3 means Cover (front) image

            # Set the ID3 version to v2.3
            audiofile.tag.version = (2, 3, 0) # v2.3 is the version supported by the package eyed3

            # Save the metadata
            audiofile.tag.save()

            # Add the episode to the summary
            if podcast_name not in dict_episod_summary:
                dict_episod_summary[podcast_name] = [episode_title]
            else:
                dict_episod_summary[podcast_name].append(episode_title)
        
        bar() # update alive bar


def main():

    if not check_connection():
        print('Network is unreachable')
        return

    start_time = time.time()
    summary_dict = {} # {podcast_name: [ep1, ep2, ...], ...}
    args = collect_args()

    if args.command == 'download':
        name = get_podcast_name(args.url)
        total_episodes = get_podcast_episods_number(args.url)

        with alive_bar(total_episodes, title="Downloading...", spinner_length=4, receipt=False, elapsed=False, stats=None) as bar:
            download_podcast(name ,args.url, args.output, args.overwrite, summary_dict , bar)
    
    elif args.command == 'download_all':
        podcasts = get_podcast_dict(args.file)
        total_episodes = sum(get_podcast_episods_number(url) for url in podcasts.values())

    with alive_bar(total_episodes, title="Downloading..." ,spinner_length=4, receipt=False, elapsed=False, stats=None) as bar:
        for name, url in podcasts.items():
            download_podcast(name, url, args.output, args.overwrite, summary_dict, bar)
    
    # print summary
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(round(total_time % 60))
    episods_count = sum(len(episods) for episods in summary_dict.values())

    print('\nSummary:\n')

    for name, episods in summary_dict.items():
        print(f'Podcast: {name}\nNew Episodes: {len(episods)}')
        if len(episods) <= 5:
            for episode in episods:
                print(f' - {episode}')
        
    print(f'\nTotal New Episodes Downloaded: {episods_count}')
    print(f'Total Time: {minutes} minutes and {seconds} seconds\n')

if __name__ == "__main__":
    main()