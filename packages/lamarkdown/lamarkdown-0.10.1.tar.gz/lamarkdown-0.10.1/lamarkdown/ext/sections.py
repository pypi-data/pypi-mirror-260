'''
# Sections Extension

Divides up a document into <section> elements, based on '---' dividers. This is useful for
producing RevealJS slide shows, for instance, where <section> elements are rendered as slides.

The '---' dividers would otherwise be captured and rendered as <hr/> elements, but this extension
overrides this. You can still use '----', etc. to get an <hr/> element. You can also configure this
extension to use an alternate divider string.

If a divider has an attached attribute list, those attributes are given to the subsequent <section>
element. If a divider appears before any other content, then it *won't* create an empty first
<section> before it, and can instead serve to attribute the first <section> below.
'''

from . import util

import markdown

import copy
import re
from xml.etree import ElementTree

_SEPARATOR_ATTR = 'la-sections-b25e560abe34c46aff67f5681e21a6a84eb10012'


class SectionBlockProcessor(markdown.blockprocessors.BlockProcessor):
    """
    Find section separators. We could just do this in the TreeProcessor stage, except that
    Python Markdown's HRProcessor would find all '---' sequences first and replace them with
    '<hr/>'.
    """

    def __init__(self, md_parser, separator):
        super().__init__(md_parser)
        self._regex = re.compile(fr'(?x)^[ ]*{re.escape(separator)}([ ]*\n)?({util.ATTR})?\s*$')

    def test(self, parent, block):
        self._match = self._regex.fullmatch(block)
        return self._match

    def run(self, parent, blocks):
        blocks.pop(0)  # We don't actually need the block, but we have to discard it.
        elem = ElementTree.SubElement(parent, 'div', {_SEPARATOR_ATTR: '1'})
        util.set_attributes(elem, self._match)


class SectionTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(self, md):
        super().__init__(md)

    def run(self, root):
        sections_found = False
        first = True
        new_root = ElementTree.Element('div')
        section = ElementTree.Element('section')
        section.text = '\n'
        section.tail = '\n'

        for element in root:
            if element.tag == 'div' and element.get(_SEPARATOR_ATTR) == '1':
                sections_found = True
                if not first:
                    # Allow for a 'separator' right at the start, which serves purely to specify
                    # attributes, and doesn't create a blank first section.
                    new_root.append(section)

                section = ElementTree.Element('section')
                section.text = '\n'
                section.tail = '\n'
                section.attrib = {k: v for k, v in element.attrib.items() if k != _SEPARATOR_ATTR}

            else:
                section.append(copy.deepcopy(element))

            first = False

        new_root.append(section)
        return new_root if sections_found else root



class SectionsExtension(markdown.Extension):
    def __init__(self, **kwargs):
        self.config = {
            'separator': [
                '---',
                'Sections will be divided by this string (which must be its own top-level block).'
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        block_proc = SectionBlockProcessor(md.parser, self.getConfig('separator'))
        tree_proc = SectionTreeProcessor(md)

        # Block processor priority must be >50, to override HRProcessor.
        md.parser.blockprocessors.register(block_proc, 'la-sections-block', 60)
        md.treeprocessors.register(tree_proc, 'la-sections-tree', 30)



def makeExtension(**kwargs):
    return SectionsExtension(**kwargs)
