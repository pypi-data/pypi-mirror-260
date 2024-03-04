# RSSPod-dl

Python-based CLI tool for downloading and managing podcast episodes from RSS feeds.

### Install Package

```shell
pip install RSSPod-dl
```

## Description

This program is a multi-threaded podcast downloader. It can download a single podcast or multiple podcasts from a list. The metadata of the original podcast episodes is maintained in the downloaded MP3 files.

---

## Usage

To run the program, use the following command:

```shell
rsspod <command> [<args>]
```

**Where:** 
- `<command>` is either `download` for a single podcast or `download_all` for multiple podcasts 
- `<args>` are the arguments for the command. For `download`, provide the **URL** of the podcast. For `download_all`, provide the **path** to the file containing the list of podcasts.

> for more information and features, use the `--help` flag with the command
    ```shell
    rsspod --help
    ``` 

### Download a Single Podcast
To download a single podcast, use the **download** command and provide the URL of the podcast:

```shell
rsspod download https://example.com/podcast.rss
```

### Download Multiple Podcasts

To download multiple podcasts, use the **download_all** command and provide the path to the file containing the list of podcasts:

```shell
rsspod download_all /path/to/podcast_list.txt
```

if no file is provided, the program will look for a file named `podcast_list.txt` in the current directory.

All podcasts in the file will be downloaded

### Adding Podcasts to the List
The file should contain the name of the podcast followed by a colon and then the URL of the podcast. Lines starting with # are treated as comments and those podcasts will not be downloaded. Here's an example of the file structure:

```txt
Podcast Name:Podcast RSS Feed URL
```

Here's an example:

```txt
Lost Terminal:https://www.spreaker.com/show/4488937/episodes/feed
```

In this example, "Lost Terminal" is the name of the podcast and "https://www.spreaker.com/show/4488937/episodes/feed" is the RSS feed URL of the podcast.

If you want to add a comment or note to yourself in the file, start the line with a `#`. The program will ignore these lines when downloading podcasts. For example:


```txt
# This is my favorite podcast
Modem Prometheus:https://www.spreaker.com/show/5184621/episodes/feed
```
Or you can use it to disable a podcast from being downloaded. For example:

```txt
# This is my favorite podcast
Lost Terminal:https://www.spreaker.com/show/4488937/episodes/feed

# Modem Prometheus:https://www.spreaker.com/show/5184621/episodes/feed
```

Once you have prepared your list, save the file. When running the `download_all` command, provide the path to this file:

```shell
rsspod download_all /path/to/podcast_list.txt
```

If no file is provided, the program will look for a file named `podcast_list.txt` in the current directory.

```txt
#Lost Terminal:https://www.spreaker.com/show/4488937/episodes/feed
Modem Prometheus:https://www.spreaker.com/show/5184621/episodes/feed
```

In this example, the "Lost Terminal" podcast will not be downloaded because its line starts with #. Each non-comment line represents a separate podcast with its corresponding RSS feed URL. The program will download all episodes from each provided podcast URL.

>Credits to [Tris](https://github.com/0atman) for the best SCI-FI podcast out there [Lost Terminal](https://lostterminal.com/).

---

### Dependencies
This program uses the following Python packages:

- `requests`: Used for making HTTP requests to download the podcast episodes.
- `bs4` (BeautifulSoup): Used for parsing the XML of the RSS feeds.
- `eyed3`: Used for handling ID3 tags in the downloaded MP3 files.
- `os` and `argparse`: Used for file operations and command line argument parsing, respectively.
- `alive_progress`: Used for displaying a progress bar while the podcasts are being downloaded.
- `io`: Used for handling byte streams.
- `time`: Used for time-related tasks.
- `socket`: Used for low-level networking interface.
- `re`: Used for regular expression operations.

You can install these packages using pip:
```shell
pip install requests bs4 eyed3 alive_progress
```

Note: `os`, `argparse`, `io`, `time`, `socket`, and re are part of the Python standard library, so you don't need to install them separately.

---

### Build Yourself (Optional)
If you want to build this project yourself, follow these steps

1. clone the repository

```shell
git clone https://github.com/yourusername/RSSPod_dl.git
```

2. Install the package

```shell
cd RSSPod_dl
pip install .
```
---

## License
This program is released under the MIT License. See the `LICENSE` file for more details.

---

## About

This project was born out of a personal need. As a podcast listener, I wanted a simple way to download my favorite podcasts from various sources and sync them to my iPod. This tool allows me to do just that - it downloads multiple podcasts and organizes them in a single directory, making it easy to transfer and listen to them on my device.

This is one of my first projects and I'm still learning, so feel free to correct me or suggest improvements, raise issues or contribute to the project!