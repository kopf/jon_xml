#!/usr/bin/env python
import codecs
import os
import sys

from bs4 import BeautifulSoup


FIELDS = ['title', 'metatitle', 'fulltitle', 'shorttitle', 'metadescription',
          'shortdescription', 'fulldescription', 'description']

def main(directory):
    for filename in [f for f in os.listdir(directory) if f.lower().endswith('.xml')]:
        template = u"""<html><head><title></title><body>"""
        with open(os.path.join(directory, filename), 'r') as f:
            xml = f.read()
        soup = BeautifulSoup(xml)
        for field in FIELDS:
            text = u''
            xml = soup.find(field)
            if xml:
                for tag in xml.contents:
                    try:
                        text += unicode(tag)
                    except (AttributeError, IndexError):
                        pass
            if text.endswith(']]>'):
                text = text[:-3]
            template += u'<h1>{field}</h1><p>{text}</p>'.format(
                field=field, text=text)
        template += u'</body></html>'
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
