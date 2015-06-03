tvrename
========

Renames TV shows with filenames matching common Scene formats.

This tool is for educational purposes only, the author does not condone or
encourage downloading or otherwise sharing of the files it can rename.

Formats
-------

`tvrename` understands the following filename formats:
* awesome.show.215.hdtv-grp.mp4
* Awesome.Show.S02E15.HDTV.x264-grp.mp4

Variations on the above may work; if in doubt, `--confirm`!

Usage
-----

```
$ tvrename.py --help
usage: tvrename.py [-h] [-n] [-c] files [files ...]

positional arguments:
  files

optional arguments:
  -h, --help     show this help message and exit
  -n, --dry-run  just print what would be done
  -c, --confirm  confirm before doing
```

### Modes of operation

`tvrename` works in two ways:
* **Rename** – if given a single file it will rename it into SxxExx format in the
  same directory, e.g. awesome.show.211.hdtv-grp.mp4 -> S02E11.mp4
* **Move** – if given one or more files & a directory, `tvrename` will look for a
  directory with the show name and move it into place, e.g.
  awesome.show.211.hdtv-grp.mp4 -> Awesome Show/S02/S02E11.mp4

`tvrename` will *not* create directories, or overwrite files.

If multiple possible directories exist, it will prompt you:

```
tvrename.py awesome.show.211.hdtv-grp.mp4 ../TV/
Couldn't determine desination for awesome.show.215.hdtv-grp.mp4.
Candidates are:
[1] ../TV/Awesome Show
[2] ../TV/Awesome Show (2015)
Choice? [1-2/Q]
```

### Options

* `-n` / `--dry-run` – Prints what it would have done, for example:
  ```
  tvrename.py -n awesome.show.211.hdtv-grp.mp4
  (Not) Moving awesome.show.211.hdtv-grp.mp4 to S02E11.mp4
  ```
* `-c` / `--confirm` – Asks before doing anything, for example:
  ```
  tvrename.py -c awesome.show.211.hdtv-grp.mp4
  Moving awesome.show.211.hdtv-grp.mp4 to S02E11.mp4
  OK? [Y/n/q]
  ```

License
-------

[tvrename][repo] is free software, available under the [MIT license][license].

[repo]: https://github.com/ElliottH/tvrename
[license]: https://github.com/ElliottH/tvrename/blob/master/LICENSE
