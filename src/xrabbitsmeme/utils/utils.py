from starlette.requests import Request


def generate_image_url(request: Request, filepath: str):
    if not filepath.startswith('/'):
        filepath = '/' + filepath
    domain = f'{request.url.scheme}://{request.url.hostname}:{request.url.port}'
    return f'{domain}{filepath}'
