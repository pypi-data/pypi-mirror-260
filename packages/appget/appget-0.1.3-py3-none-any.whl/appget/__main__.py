#!/usr/bin/env python3

import sys

from . import appget, log


def main():
    try:
        log.debug("这是debug信息")
        log.info("这是info信息")
        log.warning("这是warning信息")
        log.error("这是error信息")
        log.critical("这是critical信息")

        appget.install()
        return 0
    except Exception as err:
        log.error(err)
        return 1


if __name__ == "__main__":
    sys.exit(main())
