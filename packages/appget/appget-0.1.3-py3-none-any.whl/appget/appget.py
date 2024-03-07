import os

from . import log

BIN_HOME = '/usr/local/bin'
APP_HOME = '/usr/local/app'
APPGET_HOME = '/usr/local/app/appget'


def install():
    try:
        statinfo = os.stat(APPGET_HOME)
    except FileNotFoundError:
        try:
            # xattr -d com.apple.provenance ./appget
            os.makedirs(APPGET_HOME)
            statinfo = os.stat(APPGET_HOME)
            log.info(f'created directory: {APPGET_HOME}')
        except PermissionError as err:
            raise Exception(err.__str__())
    except Exception:
        raise

    print(statinfo)


def uninstall():
    pass


def update():
    pass


def upgrade():
    pass


def list_():
    pass


def info():
    pass


def search():
    pass
