# DigitalTattooTwitterMedia
Reposts the images / videos in the search results for the specified phrase.

## How To
- Installation of required libraries

```bash
pip install tweepy==3.1.0
pip install twitter
pip install python-twitter
pip install configparser
pip install selenium
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

- selenium install

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
install python3-selenium
apt update
apt -f install -y
which google-chrome
apt install unzip
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip
unzip IPAexfont00401.zip -d ~/.fonts/
fc-cache -fv
```

- API settings
  - `touch setting.ini`
  - `touch setting.ini
  - [docs](https://docs.python.org/ja/3/library/configparser.html)

- Create csv
  - rePostImeges.py
    - `touch ${EnvName}_tweeted.csv`
    - `touch ${EnvName}_user_id_tweeted.csv`
  - rePostVideos.py
    - `touch ${EnvName}_tweeted_movie.csv`
    - `touch ${EnvName}_user_id_tweeted_movie`
  - fanService.py
    - `touch ${EnvName}_faned.csv`
  - delTweetUserSearchQuoteService.py
    - `touch ${EnvName}_del_tweeted_fans.csv`
  - replyAndQTService.py
    - `touch ${EnvName}_quotedIds.csv`



- Run

```bash
python rePostImeges.py -w '$SearchWord' -e '$EnvName'
python rePostVideos.py -w '$SearchWord' -e '$EnvName'
python fanService.py -w '$SearchWord' -e '$EnvName'
python delTweetUserSearchQuoteService.py -e '$EnvName'
python replyAndQTService.py -e '$EnvName'
```
