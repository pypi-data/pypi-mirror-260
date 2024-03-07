import colorlog

log_format = '%(log_color)s%(message)s'

log_colors = {
    'DEBUG': 'white',
    # 'INFO': 'light_white',  # 默认的白色更柔和，light_white太刺眼
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(fmt=log_format, log_colors=log_colors, ))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(colorlog.DEBUG)


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)


if __name__ == '__main__':
    logger.debug("这是debug信息")
    logger.info("这是info信息")
    logger.warning("这是warning信息")
    logger.error("这是error信息")
    logger.critical("这是critical信息")
