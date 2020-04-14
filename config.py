import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    csp = {
        'default-src': [
            '\'self\'',
            'www.google-analytics.com'
        ],
        'script-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net',
            'www.googletagmanager.com',
            'www.google-analytics.com',
            'cdnjs.cloudflare.com'
        ],
        'img-src': [
            '\'self\' data:',
            'www.googletagmanager.com',
            'www.google-analytics.com'
        ],
        'script-src-elem': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
            'www.googletagmanager.com',
            'www.google-analytics.com',

        ],
        'style-src': [
            'use.fontawesome.com',
            '\'self\''],
        'style-src-elem': [
            '\'self\'',
            'use.fontawesome.com'],
        'font-src': '*'

    }
