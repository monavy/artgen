#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, LCI Technology Group, LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
#  Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#  Neither the name of LCI Technology Group, LLC nor the names of its
#  contributors may be used to endorse or promote products derived from this
#  software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import web
import cgi

import markov


def error(msg):
    return '{{"error":"{0}"}}'.format(msg)


def notfound():
    return web.notfound(render.notfound())


web.config.debug = False
# Setup routing
urls = (
    '/', 'Index',
    '/article', 'Article'
)

# Configure the site template
render = web.template.render('/var/www/artgen/templates/', base='layout')
# render = web.template.render('templates', base='layout')

# Setup Markov Generator
m = markov.Markov()
m.load_from_file('/home/ubuntu/artgen/source_text.txt')
# m.load_from_file('source_text.txt')


class Index:
    def GET(self):
        return render.home(None)


class Article:
    def GET(self):
        return render.home(None)

    def POST(self):
        title = web.input()['title']
        author = web.input()['author']

        # Validate Input
        errors = []
        if title == '':
            errors.append('Title can not be empty')

        if author == '':
            errors.append('Author can not be empty')

        if errors != []:
            return render.home(','.join(errors))

        article = '<h1>' + cgi.escape(title.upper(), True) + '</h1>\n'
        article += '<h2>Written By: ' + cgi.escape(author, True) + '</h2>\n'
        for i in range(10):
            article += '<p>'
            article += cgi.escape(m.generate_paragraph(5, 8), True) + '</p>'

        return article


app = web.application(urls, locals())
app.notfound = notfound

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
