# MusicValidator

Application that provides a series of functions to inspect tag information from media files and validate their presence and correctness.

## Features

-   Define libraries by familiar name
-   Pulls all tags from supported media files
-   Stored in a SQLite DB for fast retrieval

# Requirements

- Python 3+
- MusicManagerMicro
- MusicCheckerMicro

# Usage

```python
from music_validator_micro.music_validator import MusicValidator as MV
library_name = "MY_MEDIA"
mv = MV(library_name)
report = mv.execute()
# Provides an object of tag properties and the file path that is
# missing them
'''
{
    'TALB':[
        '/media/music/pop/hit_me_baby.mp3'
    ]
    'TIT2':[
        '/media/music/pop/final_countdown.mp3'
    ]
}
'''
```

# Caching

You can safely remove the cache databases in `$HOME/$XDG_CACHE/MusicValidatorMicro/<library_name>`

# Testing

Run pytest in root directory passing in tests directory. Sample audio files are also contained within tests path

# Build

```python
python -m build
python -m twine upload dist/*
```
