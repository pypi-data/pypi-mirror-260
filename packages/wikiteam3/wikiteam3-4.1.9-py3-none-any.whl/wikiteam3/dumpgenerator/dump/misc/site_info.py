import json
import os

import requests

from wikiteam3.dumpgenerator.cli import Delay
from wikiteam3.dumpgenerator.api import get_JSON
from wikiteam3.dumpgenerator.config import Config


def save_siteinfo(config: Config, session: requests.Session):
    """Save a file with site info"""

    assert config.api

    if os.path.exists("%s/siteinfo.json" % (config.path)):
        print("siteinfo.json exists, do not overwrite")
        return
    
    print("Downloading site info as siteinfo.json")

    # MediaWiki 1.13+
    r = session.get(
        url=config.api,
        params={
            "action": "query",
            "meta": "siteinfo",
            "siprop": "general|namespaces|statistics|dbrepllag|interwikimap|namespacealiases|specialpagealiases|usergroups|extensions|skins|magicwords|fileextensions|rightsinfo",
            "sinumberingroup": 1,
            "format": "json",
        },
        timeout=10,
    )
    # MediaWiki 1.11-1.12
    if not "query" in get_JSON(r):
        r = session.get(
            url=config.api,
            params={
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general|namespaces|statistics|dbrepllag|interwikimap",
                "format": "json",
            },
            timeout=10,
        )
    # MediaWiki 1.8-1.10
    if not "query" in get_JSON(r):
        r = session.get(
            url=config.api,
            params={
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general|namespaces",
                "format": "json",
            },
            timeout=10,
        )
    result = get_JSON(r)
    Delay(config=config)
    with open(
        "%s/siteinfo.json" % (config.path), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
