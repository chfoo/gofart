import codecs
import os
import random

from tornado.web import URLSpec as U
import tornado.web


class App(tornado.web.Application):
    def __init__(self, debug=False):
        handlers = [
            U(r'/', IndexHandler, name='index'),
            U(r'/(http|https|uggc|uggcf)/(.+)', FartHandler),
        ]
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        static_path = os.path.join(os.path.dirname(__file__), 'static')

        super().__init__(
            handlers,
            template_path=template_path,
            static_path=static_path,
            debug=debug,
            xsrf_cookies=True,
            cookie_secret=os.urandom(16),
        )

    def fartenize_url(self, text, host_scheme, hostname, rot13=False):
        if len(text) > 1024:
            raise ValueError('Too long')

        if text.startswith('//'):
            text = 'https:{}'.format(text)
        elif text and '://' not in text:
            text = 'https://{}'.format(text)

        scheme, sep, link = text.partition('://')

        if not sep:
            raise ValueError('No separator')

        scheme = scheme.lower()

        if scheme not in ('http', 'https'):
            raise ValueError('Bad scheme')

        if '\n' in link or '\r' in link:
            raise ValueError('Newline found')

        return '{}://{}/{}/{}'.format(
            host_scheme, hostname,
            codecs.encode(scheme, 'rot_13') if rot13 else scheme,
            codecs.encode(link, 'rot_13') if rot13 else link
        )


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        link = self.get_argument('link', '')
        rot13 = self.get_argument('rot13', False) == 'yes'

        try:
            fartlink = self.application.fartenize_url(
                link,
                self.request.protocol, self.request.host,
                rot13=rot13
            )
        except ValueError:
            self.render('index.html', error=True, link=link, rot13=rot13)
        else:
            self.render('index.html', fartlink=fartlink, link=link, rot13=rot13)


class FartHandler(BaseHandler):
    def get(self, scheme, link):
        if '\n' in link or '\r' in link:
            raise tornado.web.HTTPError(400)

        if scheme in ('uggc', 'uggcf'):
            scheme = codecs.encode(scheme, 'rot_13')
            link = codecs.encode(link, 'rot_13')

        dest_link = '{}://{}'.format(scheme, link)
        rand = random.Random(dest_link)
        name = rand.choice((
          '97979__oldedgar__raspberry',
          '117606__mefrancis13__squeaky-fart',
          '185226__efpstudio__funny-fart',
        ))
        fart_ogg = '{}.ogg'.format(name)
        fart_mp3 = '{}.mp3'.format(name)

        self.render('fart.html', dest_link=dest_link,
                    fart_ogg=fart_ogg, fart_mp3=fart_mp3)
