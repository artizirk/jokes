#!/usr/bin/env python3

import base64
import os
from datetime import datetime

jokes_dir = "."

html = """<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>The best IRC jokes in the Internet</title>
        <meta name="description" content="The best IRC jokes in the Internet">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
        <link rel="icon" type="image/x-icon" href="favicon.ico" />
        <style>{style}</style>
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
        <div id="header">
        <h1>The best IRC jokes in the Internet</h1>
        </div>
        <hr>
        {posts}
        <hr>
        <footer>
            <small><a href="https://github.com/artizirk/jokes">Source code</a></small>
        </footer>
    </body>
</html>"""

style="""body {
    max-width: 50em;
    left: 50%;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1em;
    padding-right: 1em;
}
h2>small {
    font-size: initial;
    font-weight: normal;
}
pre {
    white-space: pre-wrap;
}
footer a {
    color: black;
}"""

post_template ="""<div id="{title}">
    <a name="#{title}"><h2>{title} <small>({tag} - {mtime})</small></h2></a>
    <p>
        <pre>{post}</pre>
    </p>
</div>"""
favicon = ("AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAA"
    "AAAAAAEAAAAAAAAAD/hAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABEREQAAAA"
    "ABEREREAAAAAEQAAEQAAAAARAAARAAAAAAAAABEAAAAAAAAAEQAAAAAAAAARAAAAAAAAABEAA"
    "AAAAAAAEQAAAAAAAAARAAAAAAAAABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

def mtime_to_human(mtime):
    return datetime.fromtimestamp(mtime)


def application(env, start_response):
    if env["PATH_INFO"] == "/favicon.ico":
        start_response('200 OK', [('Content-Type', 'image/x-icon')])
        return [base64.b64decode(favicon)]

    if env["PATH_INFO"] == "/style.css":
        start_response('200 OK', [('Content-Type', 'text/css')])
        return [style.encode()]

    # if user wants anything else then show them 404
    if env["PATH_INFO"] != "/":
        start_response('404 ERROR', [('Content-Type', 'text/html')])
        message = '<h1>Error 404 <small>Page not found</small></h1><a href="/">Go back home</a><br></br>'
        return [html.format(posts=message, style=style).encode()]

    posts = []
    files = []
    dirs = os.listdir(jokes_dir)
    for d in dirs:
        # ignore normal files in dir
        if not os.path.isdir(os.path.join(jokes_dir, d)):
            continue
        # ignore hidden dirs
        if d.startswith("."):
            continue
        # add legit jokes to the list
        for f in os.listdir(os.path.join(jokes_dir, d)):
            mtime = os.stat(os.path.join(jokes_dir, d, f)).st_mtime
            files.append((d, f, mtime))

    # sort jokes by last modification time
    files.sort(key=lambda x: x[2], reverse=True)

    for joke in files:
        f = open(os.path.join(jokes_dir, joke[0], joke[1]), "rb")
        p = post_template.format(title=joke[1],
                                tag=joke[0],
                                mtime=mtime_to_human(joke[2]),
                                post=f.read().decode().replace("<", "&lt;").replace(">", "&gt;"))
        f.close()
        posts.append(p)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html.format(posts=''.join(posts), style=style).encode()]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8080, application)
    print("Serving on http://localhost:8080/")
    httpd.serve_forever()
