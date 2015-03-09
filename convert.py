#!/usr/bin/env python
import codecs
import os
import sys

from bs4 import BeautifulSoup


FIELDS = ['title', 'metaTitle', 'fullTitle', 'shortTitle', 'metaDescription',
          'shortDescription', 'fullDescription', 'description']

def main(directory):
    for filename in [f for f in os.listdir(directory) if f.lower().endswith('.xml')]:
        template = u"""
            <html><head><title></title><body>
            <h1>title</h1>
            <p>{title}</p>
            <h1>metaTitle</h1>
            <p>{metaTitle}</p>
            <h1>fullTitle</h1>
            <p>{fullTitle}</p>
            <h1>shortTitle</h1>
            <p>{shortTitle}</p>
            <h1>metaDescription</h1>
            <p>{metaDescription}</p>
            <h1>shortDescription</h1>
            <p>{shortDescription}</p>
            <h1>fullDescription</h1>
            <p>{fullDescription}</p>
            <h1>description</h1>
            <p>{description}</p>
            </body></html>
        """
        with open(os.path.join(directory, filename), 'r') as f:
            xml = f.read()
        soup = BeautifulSoup(xml)
        for field in FIELDS:
            try:
                text = unicode(soup.find(field).contents[0])
            except (AttributeError, IndexError):
                text = ''
            if text.endswith(']]>'):
                text = text[:-3]
            template = template.replace('{%s}' % field, text)
        output_file = os.path.join(directory, filename.lower().replace('.xml', '.html'))
        with codecs.open(output_file, 'w', 'utf8') as f:
            f.write(template.encode('ascii', 'xmlcharrefreplace'))
    print 'Done!'


if __name__ == '__main__':
    if not os.path.isdir(sys.argv[-1]):
        print 'Usage: '
        print '%s <path to directory containing XMLs>' % os.path.basename(__file__)
        sys.exit(-1)
    main(sys.argv[-1])
