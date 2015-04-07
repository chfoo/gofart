import argparse

import tornado.ioloop

from gofart.app import App


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--host', default='localhost',
                            help='listening hostname')
    arg_parser.add_argument('--port', default=8000, type=int,
                            help='listening port number')
    arg_parser.add_argument('--xheaders', action='store_true',
                            help='service is run behind a web server')

    arg_parser.add_argument('--debug', action='store_true',
                            help='run in debug mode')

    args = arg_parser.parse_args()

    app = App(debug=args.debug)
    app.listen(args.port, address=args.host, xheaders=args.xheaders)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
