# DigitalTattooTwitterMedia
Reposts the images / videos in the search results for the specified phrase.

## How To
- Installation of required libraries

```bash
pip install tweepy
pip install twitter
pip install configparser
```

- API settings
  - `touch setting.ini`
  - [docs](https://docs.python.org/ja/3/library/configparser.html)

- Create csv
  - `touch ${EnvName}_tweeted_movie.csv`
  - `touch ${EnvName}_tweeted.csv`
  - `touch ${EnvName}_user_id_tweeted.csv`

- Run

```bash
python rePostImeges.py -w '$SearchWord' -e '$EnvName'
python rePostVideos.py -w '$SearchWord' -e '$EnvName'
```
