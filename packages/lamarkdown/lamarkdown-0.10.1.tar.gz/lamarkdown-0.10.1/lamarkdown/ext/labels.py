'''
# List Label Extension

Assigns counter-based (or fixed) labels to headings and/or list items, either by embedding label
text directly in the HTML (for headings), or by employing CSS properties to render labels,
particularly for <ol> and <ul>.

'Label templates' specify what labelling system to use. They can be provided in two ways:

1. By adding the '-label' directive; e.g.:

    ## The Next Section {-label="[1] "}

    {-label="(a) "}
    1. Item A
    2. Item B
    3. Item C

2. By specifying the configuration options 'h_labels', 'ol_labels' and 'ul_labels', which then
   apply to the top-most heading, <ol> or <ul> elements, respectively. (By specifying 'h_level',
   the 'h_labels' template can instead apply to a specific heading level from 1 to 6.)


## Template syntax

Label templates can create complex labelling schemes, with minimal specification. The syntax is
defined as follows:

template := template_part ( ',' template_part )* [ ',' '*' ]
template_part := literal* [ [ ('X' | 'L' | 'H' [level] ) literal+ ] format_spec literal* ]

format_spec := any alphanumeric sequence (including '-', but not at the start or end position)

level := an integer from 1 to 6, inclusive
literal := ( unquoted_literal | quoted_literal )*
unquoted_literal := any single character _other than_ ',', quotation marks, alphanumeric
    characters, or '-' if surrounded by alphanumeric characters
quoted_literal := any sequence of characters surrounded by double or single quotes, and possibly
    including doubled-up quotes to represent literal quotation marks.

Thus, a template consists of one or more comma-separated parts, optionally ending in a '*'. The
first (mandatory) part applies directly to the current list or list element. Subsequent parts apply
to successive levels of child lists, _of the same fundamental type_ (nested lists for lists, and
sub-headings for headings). If present, the '*' causes the final template to apply indefinitely to
any more deeply-nested lists/headings. (If '*' is omitted, then any lists nested more deeply are
outside the scope of this template list.)

The `format_spec` refers to the core numbering system for a given list or list element. It can be:

* `1`, for arabic numerals;
* `a`/`A`, for lower/uppercase English alphabetic numbering;
* `i`/`I`, for lower/uppercase Roman numerals; or
* one of various terms accepted by the list-style-type CSS property; e.g., `lower-greek`,
    `armenian`, etc.

(This extension seeks to support _most_ numbering schemes available in CSS.)

For <ul> elements, there's generally no numbering system required, and `format_spec` can be
omitted, so that the entire template consists just of a literal `prefix`.

(This extension _does not_ directly support the CSS terms 'disc', 'circle', 'square', as these can
be directly represented with literal characters; e.g., '•', '◦', '▪'.)

If `X`, `L` or `H` is given, it refers to the label of the nearest _numbered_ ancestor element.
Specifically, `X` means _any_ such element (though, again, only those with numbering systems, so
generally not <ul> elements), `L` means a list element (almost certainly <ol>), `H` means any
heading element, and `H1`-`H6` mean the corresponding heading level. If such an ancestor element
exists, its core label (minus any prefix/suffix literals) will be inserted prior to the element's
own number, along with an delimiting literal.

If X, L or H is given, but no such element exists, then no ancestor label will be inserted, _and_
the delimiting literal will be omitted too.

Examples:

* -label="(X.1),*"
* -label="1.,(a),(i)"


# Also...

:no-label -- suppresses any label for the current element, and avoids updating the counter.

'''


# TODO:
##
# -label-resume -- continue the numbering from the previous list _at the same level_. (The
#   previous list may be a sibling element, or it may be an 'nth-cousin', sharing any common
#   ancestor element.)
#
#
# -label-skip -- skips 1 counter value if the attribute value is non-numeric. If the attr value is
#   an integer, advances the counter by that amount (_on top of_ the one increment that the counter
#   would normally advance anyway). If the attr value is '=' followed by an integer (or an
#   alphabetic count or roman numeral), then the counter value is set to that number.


from __future__ import annotations

import lamarkdown
from lamarkdown.ext.label_support.labellers import Labeller
from lamarkdown.ext.label_support.label_templates import (LabelTemplate, LabelTemplateParser,
                                                          LabelTemplateException)
from lamarkdown.ext.label_support.label_renderers import (LabelsRenderer, CssLabelsRenderer,
                                                          HtmlLabelsRenderer, add_css_class)
from lamarkdown.ext.label_support.ref_resolver import RefResolver
from lamarkdown.lib.progress import Progress
from lamarkdown.lib.directives import Directives

import markdown

import abc
from xml.etree.ElementTree import Element

NAME = 'la.labels'

LABEL_DIRECTIVE = 'label'
NO_LABEL_DIRECTIVE = 'no-label'


class LabelProcessor(abc.ABC):
    def init(self, directives: Directives):
        self.directives = directives
        self.reset()

    def reset(self):
        pass

    @abc.abstractmethod
    def test(self, element: Element) -> bool:
        ...

    @abc.abstractmethod
    def run(self, element: Element, control: 'LabelControl'):
        ...


class HeadingLabelProcessor(LabelProcessor):
    def reset(self):
        self._previous_h_level = -1

    def test(self, element: Element) -> bool:
        return element.tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    def run(self, element: Element, control: 'LabelControl'):

        if self.directives.pop_bool(NO_LABEL_DIRECTIVE, element, NAME):
            control.render_none(element.tag, None, element)
            control.resolve_refs(element)
            return

        cur_h_level = int(element.tag[1])

        # Maybe a labeller already exists (from a previous sibling heading)
        labeller = control.find(element.tag)

        if labeller is None:
            # If no labeller exists, first see if there's a '-label' directive
            template = self.directives.pop(LABEL_DIRECTIVE, element, NAME)

            # Failing that, see if a parent heading labeller specifies an inner template
            if template is None and (
                    outer_labeller := control.find(f'h{cur_h_level - 1}')) is not None:

                template = outer_labeller.template.inner_template

            # Failing that, maybe a configuration option is applicable
            if template is None:
                template = control.get_default_template('h', element.tag)

            if template is not None:
                labeller = control.new_labeller(element.tag, 'h', template)

        elif new_template := self.directives.pop(LABEL_DIRECTIVE, element, NAME):
            # A labeller does already exist, but a new template has been given
            labeller = control.replace_labeller(labeller, element.tag, 'h', new_template)

        if self._previous_h_level > cur_h_level:
            # Finishing (at least) one heading level, and continuing with a higher- level
            # heading.

            for i in range(self._previous_h_level, cur_h_level, -1):
                if (inner_labeller := control.find(f'h{i}')) is not None:
                    control.remove_labeller(inner_labeller)

        self._previous_h_level = cur_h_level

        if labeller is not None:
            control.render(labeller, None, element)

        control.resolve_refs(element)


class ListLabelProcesor(LabelProcessor):
    def test(self, element: Element) -> bool:
        return element.tag in {'ol', 'ul'}

    def run(self, element: Element, control: 'LabelControl'):
        template: str | LabelTemplate | None = self.directives.pop(LABEL_DIRECTIVE, element, NAME)

        outer_labeller = control.find(element.tag)
        if template is None and outer_labeller is not None:
            template = outer_labeller.template.inner_template

        if template is None and outer_labeller is None:
            template = control.get_default_template(element.tag)

        if template is None:
            control.resolve_refs(element)
            control.recurse(element)
            return

        labeller = control.new_labeller(element.tag, element.tag, template)
        control.resolve_refs(element)

        for li in element:
            # Lists generally contain just <li> elements, but it doesn't hurt to check.
            if li.tag == 'li':
                if self.directives.pop_bool(NO_LABEL_DIRECTIVE, li, NAME):
                    control.render_none(element.tag, element, li)

                else:
                    if new_template := self.directives.pop(LABEL_DIRECTIVE, li, NAME):
                        labeller = control.replace_labeller(labeller,
                                                            element.tag, element.tag, new_template)

                    control.render(labeller, element, li)

                control.resolve_refs(li)
                control.recurse(li)
                control.clear_dependents(labeller)

        control.remove_labeller(labeller)


class FigureLabelProcessor(LabelProcessor):
    def reset(self):
        self._first_child = True
        self._level = 0

    def test(self, element: Element) -> bool:
        return element.tag in {'figure', 'table'}

    def run(self, element: Element, control: 'LabelControl'):
        caption_tag = 'figcaption' if element.tag == 'figure' else 'caption'
        fig_caption = (
            element[0]       if element[0].tag == caption_tag
            else element[-1] if element[-1].tag == caption_tag
            else None
        )


        if element.tag == 'table':
            element_type = 'table'

            if self._level > 0 and fig_caption is None:
                # Nested <table> elements will only be labelled if they already have an explicit
                # caption. In particular, if we have <figure><table>...</table></figure>, the
                # outer <figure> element represents the container to be captioned/labelled,
                # and the inner <table> element is purely the subject of that.
                control.resolve_refs(element)
                control.recurse(element)
                return

        else:
            if cls := element.get('class'):
                css_classes = [c.lower() for c in cls.split()]
                css_type_guess = {
                    t
                    for t, words in [('figure',  ('figure', 'picture', 'image', 'diagram')),
                                     ('table',   ('table', 'tabular')),
                                     ('math',    ('math', 'equation', 'formula')),
                                     ('listing', ('listing', 'code'))]
                    if any(cls.startswith(word) or cls.endswith(word)
                           for cls in css_classes
                           for word in words)
                }
            else:
                css_type_guess = set()

            children = [e for e in element if e is not fig_caption]
            element_type = (
                css_type_guess.pop() if len(css_type_guess) == 1

                # Note: len(children) == 0 will happen in certain normal cases, where the document
                # tree merely contains _placeholder_ text that will later be turned into an image
                # (for instance). We're going to assume this means it's a figure.
                else 'figure'        if len(children) == 0

                else 'table'         if all(c.tag == 'table' for c in children)
                else 'math'          if all(c.tag == 'math'  for c in children)
                else 'listing'       if all(c.tag in ['code', 'pre'] for c in children)
                else 'figure'
            )

            add_css_class(element, f'la-{element_type}')


        if (self.directives.pop_bool(NO_LABEL_DIRECTIVE, element, NAME)
                or (fig_caption is not None
                    and self.directives.pop_bool(NO_LABEL_DIRECTIVE, fig_caption, NAME))):

            control.resolve_refs(element)
            if fig_caption is None:
                pass
            else:
                control.render_none(element_type, None, fig_caption)
                control.resolve_refs(fig_caption)

            control.recurse(element)
            return

        if fig_caption is None:
            fig_caption = Element(caption_tag)
            fig_caption.tail = element.text
            element.text = None
            element.insert(0, fig_caption)


        template1 = self.directives.pop(LABEL_DIRECTIVE, element, NAME)
        template2 = self.directives.pop(LABEL_DIRECTIVE, fig_caption, NAME)
        if template1 and template2:
            if template1 == template2:
                control.progress.warning(
                    NAME,
                    msg = (f'{self.directives.format(LABEL_DIRECTIVE, template1)} given twice '
                           f'for the same {element_type}'))
            else:
                t1_fmt = self.directives.format(LABEL_DIRECTIVE, template1)
                t2_fmt = self.directives.format(LABEL_DIRECTIVE, template2)
                control.progress.warning(
                    NAME,
                    msg = (f'Conflicting label templates, {t1_fmt} and {t2_fmt}, given for the '
                           f'same {element_type}'))

        template: str | LabelTemplate | None = template1 or template2

        maybe_labeller = control.find(element_type)
        labeller: Labeller
        if self._first_child or maybe_labeller is None:
            if template is None and maybe_labeller is not None:
                # There's an existing labeller, but it's for an outer level. Maybe it has an inner
                # specification...
                template = maybe_labeller.template.inner_template

            if template is None and self._level == 0:
                template = control.get_default_template(element_type)

            if template is None:
                control.resolve_refs(element)
                control.recurse(element)
                return

            labeller = control.new_labeller(element_type, element_type, template)

        elif template is not None:
            labeller = control.replace_labeller(maybe_labeller,
                                                element_type, element_type, template)

        else:
            labeller = maybe_labeller

        control.render(labeller, None, fig_caption)
        control.resolve_refs(element)
        control.resolve_refs(fig_caption)

        self._first_child = True
        self._level += 1
        control.recurse(element, exclude = {fig_caption})
        control.clear_dependents(labeller)
        self._first_child = False
        self._level -= 1


class LabelControl(markdown.treeprocessors.Treeprocessor):
    def __init__(self,
                 md,
                 label_processors: list[LabelProcessor],
                 default_templates: dict[str, str],
                 use_css_rendering: set[str],
                 parser: LabelTemplateParser,
                 ref_resolver: RefResolver,
                 html_renderer: HtmlLabelsRenderer,
                 css_renderer: CssLabelsRenderer | None,
                 directives: Directives,
                 progress: Progress):

        super().__init__(md)
        self._label_processors = label_processors
        self._default_templates = default_templates
        self._use_css_rendering = use_css_rendering
        self._parser = parser
        self._ref_resolver = ref_resolver
        self._html_renderer = html_renderer
        self._css_renderer = css_renderer
        self._directives = directives
        self._progress = progress


    def run(self, root: Element):
        'Starting point for all label processing, called by Python Markdown.'

        # Initialise state
        self._stack: list[Labeller] = []
        self._labellers: dict[tuple, Labeller] = {}
        self._next_id = 0
        self._renderers: dict[str, LabelsRenderer] = {}

        self._ref_resolver.find_refs(root)
        for label_proc in self._label_processors:
            label_proc.init(self._directives)

        self._apply_labellers(root)
        return root

    def _apply_labellers(self, element: Element):
        for label_proc in self._label_processors:
            if label_proc.test(element):
                label_proc.run(element, self)
                break
        else:
            self.resolve_refs(element)
            self.recurse(element)

    # The methods below form a kind of API used by individual label processors.

    def recurse(self, element: Element, exclude: set[Element] = set()):
        for child in element:
            if element not in exclude:
                self._apply_labellers(child)

    def clear_dependents(self, labeller: Labeller):
        for dependent_labeller in labeller.dependents:
            try:
                self._stack.remove(dependent_labeller)
            except ValueError:
                pass  # Doesn't matter if not in stack
            self.clear_dependents(dependent_labeller)
        labeller.dependents.clear()

    def remove_labeller(self, labeller: Labeller):
        self.clear_dependents(labeller)
        try:
            self._stack.remove(labeller)
        except ValueError:
            pass

    def find(self, element_type: str) -> Labeller | None:
        if element_type is None:
            return None
        for labeller in reversed(self._stack):
            if isinstance(labeller, Labeller) and labeller.element_type.startswith(element_type):
                return labeller
        return None

    def get_default_template(self, *element_types: str) -> str | None:
        for t in element_types:
            if template := self._default_templates.get(t):
                return template
        return None

    def _get_renderer(self, element_type: str):

        if self._css_renderer is None:
            return self._html_renderer

        renderer = self._renderers.get(element_type)
        if renderer is None:
            renderer = (
                self._css_renderer if any(element_type.startswith(t)
                                          for t in self._use_css_rendering)
                else self._html_renderer
            )
            self._renderers[element_type] = renderer

        return renderer

    def _make_labeller(self,
                       specific_element_type: str,
                       series_element_type: str,
                       template: str | LabelTemplate,
                       parent: Labeller | None = None,
                       count: int = 0) -> Labeller:

        try:
            _template: LabelTemplate = (
                self._parser.parse(template) if isinstance(template, str) else template)
        except LabelTemplateException as e:
            self._progress.error(NAME, exception = e)
            _template = self._parser.parse('1')

        _parent = (
            self.find(_template.parent_type)
            if parent is None and _template.parent_type is not None
            else parent)

        use_css = isinstance(self._get_renderer(specific_element_type), CssLabelsRenderer)

        # We cache labellers, reusing ones that share the same visual info and same parents. This
        # is done to optimise the output (fewer CSS declarations), _not_ processing time or memory
        # usage.

        key_list = [_template.counter_type, use_css, _template.prefix, _template.suffix]
        cur_parent = _parent
        while cur_parent is not None:
            key_list.append(cur_parent._template.counter_type)
            key_list.append(_template.separator)
            cur_parent = cur_parent.parent
        key = tuple(key_list)

        labeller = self._labellers.get(key)
        if labeller is None:
            if use_css:
                css_id = self._next_id
                self._next_id += 1
            else:
                css_id = None

            outer_labeller = self.find(series_element_type)
            labeller = Labeller(specific_element_type, _template, _parent, count, css_id)
            self._labellers[key] = labeller
            if outer_labeller is not None:
                outer_labeller.add_dependent(labeller)

        labeller.count = count

        assert parent is not labeller

        if _parent is not None:
            _parent.add_dependent(labeller)


        return labeller


    def new_labeller(self,
                     specific_element_type: str,
                     series_element_type: str,
                     template: str | LabelTemplate) -> Labeller:
        labeller = self._make_labeller(specific_element_type, series_element_type, template)
        self._stack.append(labeller)
        return labeller

    def replace_labeller(self,
                         old_labeller: Labeller,
                         specific_element_type: str,
                         series_element_type: str,
                         new_template: str | LabelTemplate):
        labeller = self._make_labeller(specific_element_type,
                                       series_element_type,
                                       new_template,
                                       parent = old_labeller.parent)
        self.clear_dependents(old_labeller)
        self._stack[self._stack.index(old_labeller)] = labeller
        return labeller

    def render(self, labeller: Labeller, container: Element | None, item: Element):
        labeller.count += 1
        self._get_renderer(labeller.element_type).render_labelled_element(labeller,
                                                                          container, item)

    def render_none(self, element_type: str, container: Element | None, item: Element):
        self._get_renderer(element_type).render_no_labelled_element(container, item)

    def resolve_refs(self, element: Element):
        self._ref_resolver.resolve_refs(element, self.find)

    @property
    def progress(self):
        return self._progress



_FN_DEFAULT = lambda: 0  # noqa: E731


class LabelsExtension(markdown.Extension):
    def __init__(self, **kwargs):
        p = None
        try:
            from lamarkdown.lib.build_params import BuildParams
            p = BuildParams.current
        except ModuleNotFoundError:
            pass  # Use default defaults

        default_progress = p.progress if p else Progress()

        self.config = {
            'directives': [
                p.directives if p else Directives(default_progress),
                'An object that retrieves directives from document elements.'
            ],

            'progress': [
                default_progress,
                'An object accepting progress messages.'
            ],

            'css_fn': [
                lamarkdown.css  # type: ignore
                if p else _FN_DEFAULT,
                'Callback function accepting CSS code via a string parameter. This enables CSS-'
                'based numbering (for <ol> elements). This may be "None", in which case list '
                'labels will be computed at compile-time and embedded in the HTML as plain text.'
            ],

            'label_processors': [
                [HeadingLabelProcessor(), ListLabelProcesor(), FigureLabelProcessor()],
                'The processors to be invoked to coordinate the labelling of elements.'
            ],

            'css_rendering': [
                {'ol', 'ul'}
            ],

            'labels': [
                {},
                'Default label template for each element type, to be applied at the outer-most '
                'level.'
            ],
        }
        super().__init__(**kwargs)


    def extendMarkdown(self, md):
        # Note: it may be wise to load the la.attr_prefix extension alongside this one, because it
        # provides a convenient way to apply directives. However, attr_prefix isn't loaded
        # automatically here, because this extension might still be useful without it.

        css_fn = self.getConfig('css_fn')
        control = LabelControl(
            md,
            label_processors = self.getConfig('label_processors'),
            default_templates = self.getConfig('labels'),
            use_css_rendering = self.getConfig('css_rendering'),
            parser = LabelTemplateParser(),
            ref_resolver = RefResolver(),
            html_renderer = HtmlLabelsRenderer(),
            css_renderer = None if css_fn is _FN_DEFAULT else CssLabelsRenderer(css_fn),
            directives = self.getConfig('directives'),
            progress = self.getConfig('progress'),
        )

        md.treeprocessors.register(control, 'la-labels-tree', 6)

        # Priority must be:
        # * Lower than the TreeProcessors of 'attr_list' (priority 8) and 'la.attr_prefix' (15),
        #   because they will supply the directives (as element attributes) that we consume here.
        #
        # * Higher than the TreeProcessor of 'toc' (priority 5), because heading elements must be
        #   labelled before the table-of-contents is built, or the labels will be omitted from the
        #   ToC.



def makeExtension(**kwargs):
    return LabelsExtension(**kwargs)
