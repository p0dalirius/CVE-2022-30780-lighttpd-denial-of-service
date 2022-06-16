# CVE-2022-30780 - lighttpd remote denial of service

<p align="center">
   CVE-2022-30780 - lighttpd remote denial of service
   <br>
   <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/CVE-2022-30780-lighttpd-denial-of-service">
   <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
   <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
   <br>
   <br>
</p>

## Summary

An unauthenticated attacker can send an HTTP request with an URL overflowing the maximum URL length, resulting in a denial of service.

### Vulnerable versions

The following versions of lighttpd are vulnerable:

| Software | Version                                                                                       | Vulnerable                |
|----------|-----------------------------------------------------------------------------------------------|---------------------------|
| Lighttpd | [1.4.58](https://api.github.com/repos/lighttpd/lighttpd1.4/zipball/refs/tags/lighttpd-1.4.58) | [Yes :white_check_mark:](./tests/1.4.58/) |
| Lighttpd | [1.4.57](https://api.github.com/repos/lighttpd/lighttpd1.4/zipball/refs/tags/lighttpd-1.4.57) | [Yes :white_check_mark:](./tests/1.4.57/) |
| Lighttpd | [1.4.56](https://api.github.com/repos/lighttpd/lighttpd1.4/zipball/refs/tags/lighttpd-1.4.56) | [Yes :white_check_mark:](./tests/1.4.56/) |

## Usage

```
$ ./CVE-2022-30780-lighttpd-denial-of-service.py -h
usage: CVE-2022-30780-lighttpd-denial-of-service.py [-h] [-v] -u URL [-k] [-t THREADS]

CVE-2022-30780-lighttpd-denial-of-service

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose mode
  -u URL, --url URL     URL to connect to.
  -k, --insecure        Allow insecure server connections when using SSL (default: False)
  -t THREADS, --threads THREADS
                        Number of threads (default: 20)
```

## Demonstration

https://user-images.githubusercontent.com/79218792/169104678-62d1c35e-252d-4174-8a1d-3af7e4462ff2.mp4

## References
 - https://github.com/lighttpd/lighttpd1.4
 - https://podalirius.net/en/cves/2022-30780/
 - https://redmine.lighttpd.net/issues/3059
