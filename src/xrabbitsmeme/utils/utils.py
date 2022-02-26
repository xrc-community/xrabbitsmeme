from .. import config


def generate_image_url(filepath: str):
    if not filepath.startswith('/'):
        filepath = '/' + filepath
    domain = config.DOMAIN
    return f'{domain}{filepath}'
