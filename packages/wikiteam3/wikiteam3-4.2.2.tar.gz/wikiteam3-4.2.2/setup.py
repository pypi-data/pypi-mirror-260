# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikiteam3',
 'wikiteam3.dumpgenerator',
 'wikiteam3.dumpgenerator.api',
 'wikiteam3.dumpgenerator.cli',
 'wikiteam3.dumpgenerator.dump',
 'wikiteam3.dumpgenerator.dump.image',
 'wikiteam3.dumpgenerator.dump.misc',
 'wikiteam3.dumpgenerator.dump.page',
 'wikiteam3.dumpgenerator.dump.page.xmlexport',
 'wikiteam3.dumpgenerator.dump.page.xmlrev',
 'wikiteam3.dumpgenerator.dump.xmldump',
 'wikiteam3.dumpgenerator.log',
 'wikiteam3.uploader',
 'wikiteam3.utils',
 'wikiteam3.utils.login']

package_data = \
{'': ['*']}

install_requires = \
['file_read_backwards>=3.0.0,<4.0.0',
 'internetarchive>=3.5.0,<4.0.0',
 'lxml>=4.9.2,<5.0.0',
 'mwclient>=0.10.1,<0.11.0',
 'python-slugify>=8.0.1,<9.0.0',
 'requests>=2.31.0,<3.0.0']

entry_points = \
{'console_scripts': ['wikiteam3dumpgenerator = wikiteam3.dumpgenerator:main',
                     'wikiteam3uploader = wikiteam3.uploader:main']}

setup_kwargs = {
    'name': 'wikiteam3',
    'version': '4.2.2',
    'description': 'Tools for downloading and preserving MediaWikis. We archive MediaWikis, from Wikipedia to tiniest wikis.',
    'long_description': '# `wikiteam3`\n\n![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Farchive.org%2Fadvancedsearch.php%3Fq%3Dsubject%3Awikiteam3%26rows%3D1%26page%3D1%26output%3Djson&query=%24.response.numFound&label=WikiTeam3%20Dumps%40IA)\n[![PyPI version](https://badge.fury.io/py/wikiteam3.svg)](https://badge.fury.io/py/wikiteam3)\n\n<!-- !["MediaWikiArchive.png"](./MediaWikiArchive.png) -->\n<div align=center><img width = \'150\' height =\'150\' src ="./MediaWikiArchive.png"/></div>\n\n> Countless MediaWikis are still waiting to be archived.\n>\n> _Image by [@gledos](https://github.com/gledos/)_\n\n`wikiteam3` is a fork of `mediawiki-scraper`.\n\n<details>\n\n## Why we fork mediawiki-scraper\n\nOriginally, mediawiki-scraper was named wikiteam3, but wikiteam upstream (py2 version) suggested that the name should be changed to avoid confusion with the original wikiteam.  \nHalf a year later, we didn\'t see any py3 porting progress in the original wikiteam, and mediawiki-scraper lacks "code" reviewers.  \nSo, we decided to break that suggestion, fork and named it back to wikiteam3, put the code here, and release it to pypi wildly.\n\nEverything still under GPLv3 license.\n\n</details>\n\n## Installation/Upgrade\n\n```shell\npip install wikiteam3 --upgrade\n```\n\n## Dumpgenerator usage\n\n### Downloading a wiki with complete XML history and images\n\n```bash\nwikiteam3dumpgenerator http://wiki.domain.org --xml --images\n```\n\n>[!WARNING]\n>\n> `NTFS/Windows` users please note: When using `--images`, because NTFS does not allow characters such as `:*?"<>|` in filenames, some files may not be downloaded, please pay attention to the `XXXXX could not be created by OS` error in your `errors.log`.\n> We will not make special treatment for NTFS/EncFS "path too long/illegal filename", highly recommend you to use ext4/xfs/btrfs, etc.\n> <details>\n> - Introducing the "illegal filename rename" mechanism will bring complexity. WikiTeam(python2) had this before, but it caused more problems, so it was removed in WikiTeam3.\n> - It will cause confusion to the final user of wikidump (usually the Wiki site administrator).\n> - NTFS is not suitable for large-scale image dump with millions of files in a single directory.(Windows background service will occasionally scan the whole disk, we think there should be no users using WIN/NTFS to do large-scale MediaWiki archive)\n> - Using other file systems can solve all problems.\n> </details>\n\n### Manually specifying `api.php` and/or `index.php`\n\nIf the script can\'t find itself the `api.php` and/or `index.php` paths, then you can provide them:\n\n```bash\nwikiteam3dumpgenerator --api http://wiki.domain.org/w/api.php --xml --images\n```\n\n```bash\nwikiteam3dumpgenerator --api http://wiki.domain.org/w/api.php --index http://wiki.domain.org/w/index.php \\\n    --xml --images\n```\n\nIf you only want the XML histories, just use `--xml`. For only the images, just `--images`. For only the current version of every page, `--xml --curonly`.\n\n### Resuming an incomplete dump\n\n<details>\n\n```bash\nwikiteam3dumpgenerator \\\n    --api http://wiki.domain.org/w/api.php --xml --images --resume --path /path/to/incomplete-dump\n```\n\nIn the above example, `--path` is only necessary if the download path (wikidump dir) is not the default.\n\n>[!NOTE]\n>\n> en: When resuming an incomplete dump, the configuration in `config.json` will override the CLI parameters. (But not all CLI parameters will be ignored, check `config.json` for details)\n\n`wikiteam3dumpgenerator` will also ask you if you want to resume if it finds an incomplete dump in the path where it is downloading.\n\n</details>\n\n## Using `wikiteam3uploader`\n\n### Requirements\n\n> [!NOTE]\n>\n> Please make sure you have the following requirements before using `wikiteam3uploader`, and you don\'t need to install them if you don\'t wanna upload the dump to IA.\n\n- unbinded localhost port 62954 (for multiple processes compressing queue)\n- 3GB+ RAM (~2.56GB for commpressing)\n- 64-bit OS (required by 2G `wlog` size)\n\n- `7z` (binary)\n    > Debian/Ubuntu: install `p7zip-full`  \n\n    > [!NOTE]\n    >\n    > Windows: install <https://7-zip.org> and add `7z.exe` to PATH\n- `zstd` (binary)\n    > 1.5.5+ (recommended), v1.5.0-v1.5.4(DO NOT USE), 1.4.8 (minimum)  \n    > install from <https://github.com/facebook/zstd>  \n\n    > [!NOTE]\n    >\n    > Windows: add `zstd.exe` to PATH\n\n### Uploader usage\n\n> [!NOTE]\n>\n> Read `wikiteam3uploader --help` and do not forget `~/.wikiteam3_ia_keys.txt` before using `wikiteam3uploader`.\n\n```bash\nwikiteam3uploader {YOUR_WIKI_DUMP_PATH}\n```\n\n## Checking dump integrity\n\nTODO: xml2titles.py\n\nIf you want to check the XML dump integrity, type this into your command line to count title, page and revision XML tags:\n\n```bash\ngrep -E \'<title(.*?)>\' *.xml -c; grep -E \'<page(.*?)>\' *.xml -c; grep \\\n    "</page>" *.xml -c;grep -E \'<revision(.*?)>\' *.xml -c;grep "</revision>" *.xml -c\n```\n\nYou should see something similar to this (not the actual numbers) - the first three numbers should be the same and the last two should be the same as each other:\n\n```bash\n580\n580\n580\n5677\n5677\n```\n\nIf your first three numbers or your last two numbers are different, then, your XML dump is corrupt (it contains one or more unfinished ```</page>``` or ```</revision>```). This is not common in small wikis, but large or very large wikis may fail at this due to truncated XML pages while exporting and merging. The solution is to remove the XML dump and re-download, a bit boring, and it can fail again.\n\n## import wikidump to MediaWiki / wikidump data tips\n\n> [!IMPORTANT]\n>\n> In the article name, spaces and underscores are treated as equivalent and each is converted to the other in the appropriate context (underscore in URL and database keys, spaces in plain text). <https://www.mediawiki.org/wiki/Manual:Title.php#Article_name>\n\n> [!NOTE]\n>\n> `WikiTeam3` uses `zstd` to compress `.xml` and `.txt` files, and `7z` to pack images (media files).  \n> `zstd` is a very fast stream compression algorithm, you can use `zstd -d` to decompress `.zst` file/steam.\n\n## Contributors\n\n**WikiTeam** is the [Archive Team](http://www.archiveteam.org) [[GitHub](https://github.com/ArchiveTeam)] subcommittee on wikis.\nIt was founded and originally developed by [Emilio J. Rodríguez-Posada](https://github.com/emijrp), a Wikipedia veteran editor and amateur archivist. Thanks to people who have helped, especially to: [Federico Leva](https://github.com/nemobis), [Alex Buie](https://github.com/ab2525), [Scott Boyd](http://www.sdboyd56.com), [Hydriz](https://github.com/Hydriz), Platonides, Ian McEwen, [Mike Dupont](https://github.com/h4ck3rm1k3), [balr0g](https://github.com/balr0g) and [PiRSquared17](https://github.com/PiRSquared17).\n\n**Mediawiki-Scraper** The Python 3 initiative is currently being led by [Elsie Hupp](https://github.com/elsiehupp), with contributions from [Victor Gambier](https://github.com/vgambier), [Thomas Karcher](https://github.com/t-karcher), [Janet Cobb](https://github.com/randomnetcat), [yzqzss](https://github.com/yzqzss), [NyaMisty](https://github.com/NyaMisty) and [Rob Kam](https://github.com/robkam)\n\n**WikiTeam3** Every archivist who has uploaded a wikidump to the [Internet Archive](https://archive.org/search?query=subject%3Awikiteam3).\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'yzqzss',
    'maintainer_email': 'yzqzss@yandex.com',
    'url': 'https://github.com/saveweb/wikiteam3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
