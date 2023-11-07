#!/usr/bin/env python3

import argparse
import logging
import os
import urllib.request
from pathlib import Path


def main(args):
    z, x, y = map(int, args.tile.split("/"))
    logging.info(f"Downloading children of {z}/{x}/{y} to zoom {args.zoom}")
    downloadChildren(z, x, y, args.url, args.destination, args.zoom, args.force)


def downloadChildren(z, x, y, url, destination, maxZoom, force=False):
    downloadTile(z, x, y, url, destination, force)
    if z < maxZoom:
        downloadChildren(z + 1, x * 2, y * 2, url, destination, maxZoom, force)
        downloadChildren(z + 1, x * 2 + 1, y * 2, url, destination, maxZoom, force)
        downloadChildren(z + 1, x * 2, y * 2 + 1, url, destination, maxZoom, force)
        downloadChildren(z + 1, x * 2 + 1, y * 2 + 1, url, destination, maxZoom, force)


def downloadTile(z, x, y, url, destination, force=False):
    tile = Path(destination) / str(z) / str(x)
    tile.mkdir(parents=True, exist_ok=True)
    tile = tile / f"{y}.png"
    if not force and tile.exists():
        logging.info(f"Skipping {tile}")
        return
    logging.info(f"Downloading {tile}")
    urllib.request.urlretrieve(url.format(z=z, x=x, y=y), tile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "tile", help="Tile to download example: 7/22/49", metavar="tile"
    )
    parser.add_argument(
        "url",
        help="url template, example: http://example.com/{z}/{x}/{y}.png",
        metavar="URL",
    )
    parser.add_argument("destination", help="destination directory", metavar="DEST")
    parser.add_argument("-f", "--force", help="force download", action="store_true")
    parser.add_argument("-z", "--zoom", help="zoom level", type=int, default=14)

    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    main(args)
