### magnetpy-python3
very simple and half-assed magnet url parser written in python2, now converted to python3.

This is a forked version of the repo [original](https://github.com/jeffjose/magnetpy). 
The changes include:
- Refactored the code to Python3 
- Renamed the default shortcut method to `parse_magnet`.

Short example (the following magnet link is an example only, it is in no way meant to be distributed.)
```
>>> u = parse_magnet('magnet:?xt=urn:btih:618d44538721e80dfd5657161816158de0d8dcae&dn=Star+Wars%3A+Empire+at+War+-+Gold+Pack+%28GOG%29&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969')
>>> u
<magnetpy.magnet_url.MagnetUrl object at 0x7feeea194b70>
>>> u.data
{'tr': ['udp://tracker.leechers-paradise.org:6969', 'udp://zer0day.ch:1337', 'udp://tracker.coppersurfer.tk:6969', 'udp://public.popcorn-tracker.org:6969'], 'dn': 'Star Wars: Empire at War - Gold Pack (GOG)', 'xt': 'urn:btih:618d44538721e80dfd5657161816158de0d8dcae'}
>>> u.files
[{'hash': '618d44538721e80dfd5657161816158de0d8dcae', 'hash_type': 'btih', 'data_size': None, 'display_name': 'Star Wars: Empire at War - Gold Pack (GOG)'}]
```


