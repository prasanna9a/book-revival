import tempfile
import unittest
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET
from revive import write_epub


class PackagingTests(unittest.TestCase):
    def test_unicode_navigation_and_xml_escaping(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'sample.epub'
            write_epub(output, 'కథ & <book>', 'te', [
                {'text': 'చందమామ & <నమూనా>\n\nSecond paragraph'},
                {'text': ''},
            ], 'abc123')
            with zipfile.ZipFile(output) as z:
                self.assertEqual(z.namelist()[0], 'mimetype')
                self.assertEqual(z.getinfo('mimetype').compress_type, zipfile.ZIP_STORED)
                self.assertEqual(z.read('mimetype'), b'application/epub+zip')
                for name in z.namelist():
                    if name.endswith(('.xml', '.opf', '.xhtml')):
                        ET.fromstring(z.read(name))
                first = z.read('EPUB/p1.xhtml').decode()
                self.assertIn('చందమామ &amp; &lt;నమూనా&gt;', first)
                self.assertIn('Unreviewed draft', first)
                self.assertIn('Text extraction unavailable', z.read('EPUB/p2.xhtml').decode())
                nav = ET.fromstring(z.read('EPUB/nav.xhtml'))
                for link in nav.findall('.//{http://www.w3.org/1999/xhtml}a'):
                    target, anchor = link.attrib['href'].split('#')
                    root = ET.fromstring(z.read('EPUB/' + target))
                    self.assertTrue(any(e.get('id') == anchor for e in root.iter()))

    def test_empty_book_rejected(self):
        with self.assertRaises(ValueError):
            write_epub('unused.epub', 'Empty', 'te', [], 'hash')


if __name__ == '__main__':
    unittest.main()
