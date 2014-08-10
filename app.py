#!/usr/bin/env python3

import base64
import os

html = """
<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>The best IRC jokes in the Internet</title>
        <meta name="description" content="The best IRC jokes in the Internet">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
        <link rel="icon" type="image/x-icon" href="favicon.ico" />
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body style="">
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->

        <br>
        <h1>The best IRC jokes in the Internet</h1>

        <hr>
        {posts}
        <hr>
        <small><a href="#" style="color:black;">Source code</a></small>,  <small>now press F5</small>
    </body>
</html>
"""

style="""
/*i cant style*/
body {
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
"""

post_template ="""
<h2>{title} <small>({tag})</small></h2>
<p><pre>
{post}
</pre></p>
"""

favicon = 'AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAD/hAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABEREQAAAAABEREREAAAAAEQAAEQAAAAARAAARAAAAAAAAABEAAAAAAAAAEQAAAAAAAAARAAAAAAAAABEAAAAAAAAAEQAAAAAAAAARAAAAAAAAABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


def application(env, start_response):
    if env["PATH_INFO"] == "/favicon.ico":
        start_response('200 OK', [('Content-Type', 'image/x-icon')])
        return [base64.b64decode(favicon)]

    if env["PATH_INFO"] == "/style.css":
        start_response('200 OK', [('Content-Type', 'text/css')])
        return [style.encode()]

    start_response('200 OK', [('Content-Type', 'text/html')])
    posts = []
    files = []
    dirs = os.listdir("jokes")
    for d in dirs:
        for f in os.listdir("jokes/"+d):
            files.append((d, f))

    for joke in files:
        f = open("jokes/{}/{}".format(joke[0], joke[1]), "rb")
        p = post_template.format(title=joke[1], tag=joke[0], post=f.read().decode())
        f.close()
        posts.append(p)
    return [html.format(posts=''.join(posts)).encode()]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 8080, application)
    print("Serving on http://localhost:8080/")
    httpd.serve_forever()
