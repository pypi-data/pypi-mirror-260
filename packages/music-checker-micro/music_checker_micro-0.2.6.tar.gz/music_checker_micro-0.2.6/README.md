# MusicChecker

Application that provides a series of functions to retrieve tag information from media files.

## Features

-   Define libraries by familiar name
-   Pulls all tags from supported media files
-   Stored in a SQLite DB for fast retrieval

# Requirements

Python 3+

# Usage

```python
from music_checker_micro.music_checker import MusicChecker as MC
library = "my_library"
mc = MC(library)
result = mc.execute()
```

# Supported Formats

-   MP3
-   ~~FLAC~~

# Caching

Cached data is stored in the standard XDG directory

```txt
$HOME/$XDG_CACHE/MusicCheckerMicro/<library_name>
```

Usually /home/username/.cache/MusicChecker

# Testing

Run pytest in root directory passing in tests directory. Sample audio files are also contained within tests path

# TODO

-   dynamic placement of cache dir
-   update on mtime

# Build

```python
python -m build
python -m twine upload dist/*
```
