#!/usr/bin/env python3
"""Read-only intrinsic validator for the knowledge-base content contract."""
import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import date
from pathlib import Path

SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
SECTIONS = ('hook-eli5', 'big-picture', 'mechanics', 'trade-offs', 'pitfalls', 'mastery')
CHECKERS = {}
CURRENT_PROFILE = 'constitution-1.2'
PRESENTATIONS = ('disclosure-v1', 'sources-only-v1')
INTERVIEW_TITLE = 'Tricky & Most-Asked Interview Scenarios'
INTERVIEW_START = '<!-- kb-interview-scenarios:start -->'
INTERVIEW_END = '<!-- kb-interview-scenarios:end -->'
ANSWER_PARTS = {
    'scenario': 'The Scenario & Constraint',
    'decision': 'The Direct Answer & Architectural Decision',
    'trade-offs': 'Key Trade-Offs & Follow-Up Traps',
}


class ValidationError(ValueError):
    """A catalog or content artifact violates a named contract rule."""


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result: raise ValidationError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValidationError(f'{path}: {exc}') from exc


def _nodes(manifest):
    if not isinstance(manifest, dict) or type(manifest.get('schemaVersion')) is not int or manifest['schemaVersion'] != 1:
        raise ValidationError('schemaVersion must be integer 1')
    roots = manifest.get('roots')
    if not isinstance(roots, list) or not roots: raise ValidationError('roots must be a nonempty array')
    return roots


def index_manifest(manifest, root, baseline=None):
    old_ids = set()
    if baseline is not None:
        def collect(nodes):
            for node in nodes:
                if isinstance(node, dict):
                    identity = node.get('id')
                    if not isinstance(identity, str): raise ValidationError('Baseline node id must be a string')
                    old_ids.add(identity)
                    if isinstance(node.get('children'), list): collect(node['children'])
        collect(_nodes(baseline))
    index, ids = {}, set()
    root = Path(root).resolve()
    content_root = (root / 'topics').resolve()
    # The configured content root itself must also remain within the checkout.
    if not content_root.is_relative_to(root): raise ValidationError('Content root escapes repository')
    def visit(nodes, ancestors, is_root=False):
        slugs = set()
        for node in nodes:
            if not isinstance(node, dict): raise ValidationError('Each node must be an object')
            identity, kind, title, slug = (node.get(k) for k in ('id','kind','title','slug'))
            if not isinstance(identity, str) or not identity or re.search(r'\s', identity):
                raise ValidationError('Node id must be a nonempty opaque string without whitespace')
            if identity in ids: raise ValidationError(f'Duplicate node ID: {identity}')
            ids.add(identity)
            if identity not in old_ids:
                try:
                    parsed = uuid.UUID(identity)
                    if parsed.version != 4 or str(parsed) != identity: raise ValueError()
                except (ValueError, AttributeError): raise ValidationError(f'New node needs canonical lowercase UUIDv4: {identity}')
            if kind not in ('hub','topic') or (is_root and kind != 'hub'):
                raise ValidationError('kind must be hub/topic and every root must be a hub')
            if not isinstance(title, str) or not title.strip(): raise ValidationError('Node title must not be blank')
            if not isinstance(slug, str) or not SLUG.fullmatch(slug): raise ValidationError(f'Invalid kebab-case slug: {slug!r}')
            if slug in slugs: raise ValidationError(f'Duplicate sibling slug: {slug}')
            slugs.add(slug)
            chain = ancestors + [node]
            route = '/' + '/'.join(n['slug'] for n in chain)
            relative = 'topics' + route + ('/_overview.html' if kind == 'hub' else '.html')
            path = (root / relative).resolve()
            if not path.is_relative_to(content_root): raise ValidationError(f'Derived path escapes content root: {relative}')
            index[route] = dict(node=node, route=route, relative_path=relative, path=path, ancestors=chain)
            if kind == 'hub':
                children = node.get('children')
                if not isinstance(children, list) or not children: raise ValidationError(f'Hub needs nonempty children: {route}')
                visit(children, chain)
            elif 'children' in node: raise ValidationError(f'Topic must not have children: {route}')
    visit(_nodes(manifest), [], True)
    return index


def validate_expectation(index, expected):
    base = '/' + expected['root']['slug']
    parent = base + '/' + expected['parent']['slug']
    wanted = [(base, expected['root']['title'], 'hub'), (parent, expected['parent']['title'], 'hub')]
    for group in expected['groups']:
        route = parent + '/' + group['slug']
        wanted.append((route, group['title'], 'hub'))
        for topic in group['topics']:
            wanted.append((route + '/' + topic['slug'], topic['title'], 'topic'))
        if route in index:
            actual = [n['slug'] for n in index[route]['node'].get('children', [])]
            required = [t['slug'] for t in group['topics']]
            if [s for s in actual if s in required] != required:
                raise ValidationError(f'Wrong requested topic order: {route}')
    for route, title, kind in wanted:
        item = index.get(route)
        if not item or item['node']['title'] != title or item['node']['kind'] != kind:
            raise ValidationError(f'Missing/misplaced/wrong-label requested node: {route} ({title})')
    group_slugs = [g['slug'] for g in expected['groups']]
    actual = [n['slug'] for n in index[parent]['node']['children']]
    if [s for s in actual if s in group_slugs] != group_slugs:
        raise ValidationError('Wrong requested category order')
    return {'topics': sum(len(g['topics']) for g in expected['groups']), 'hubs': 2 + len(expected['groups'])}


from html.parser import HTMLParser
from dataclasses import dataclass, field


@dataclass
class Element:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def all(self, tag=None, **attrs):
        result = []
        for child in self.children:
            if isinstance(child, Element):
                if (tag is None or child.tag == tag) and all(child.attrs.get(k) == v for k,v in attrs.items()): result.append(child)
                result.extend(child.all(tag, **attrs))
        return result

    def text(self):
        return ' '.join(child.text() if isinstance(child, Element) else child for child in self.children).strip()

    def has_class(self, name): return name in self.attrs.get('class','').split()


class ArticleParser(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element('document'); self.stack = [self.root]; self.errors = []

    def handle_decl(self, decl): self.errors.append('Document declarations are forbidden in partials')

    def handle_starttag(self, tag, attrs):
        if len({k for k,v in attrs}) != len(attrs): self.errors.append(f'Duplicate attributes on {tag}')
        el = Element(tag, dict(attrs)); self.stack[-1].children.append(el)
        if tag not in self.VOID: self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID: self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if len(self.stack) < 2 or self.stack[-1].tag != tag:
            self.errors.append(f'Unbalanced closing tag: {tag}')
        else: self.stack.pop()

    def handle_data(self, text): self.stack[-1].children.append(text)

    def finish(self):
        self.close()
        if len(self.stack) != 1: self.errors.append('Unclosed HTML elements')



def check_links(article, index):
    from urllib.parse import urlsplit, parse_qsl
    errors = []
    for anchor in article.all('a'):
        href = anchor.attrs.get('href', '')
        if not anchor.text().strip(): errors.append('Link needs accessible text')
        if href.startswith('#/'):
            parsed = urlsplit(href[1:])
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
            target = index.get(parsed.path)
            if not target or parsed.fragment or parsed.netloc or parsed.scheme:
                errors.append(f'Unknown content route: {href}'); continue
            if len(pairs)>1 or any(k!='section' or v not in SECTIONS for k,v in pairs):
                errors.append(f'Invalid section query: {href}')
            if pairs and target['node']['kind']!='topic': errors.append('Only topics have lesson sections')
        else:
            parsed = urlsplit(href)
            if parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password:
                errors.append(f'Invalid source/content link: {href}')
    return errors


def strip_interview_block(source):
    if source.count(INTERVIEW_START) != 1 or source.count(INTERVIEW_END) != 1:
        raise ValidationError('Expected exactly one complete interview marker pair')
    start = source.index(INTERVIEW_START)
    end = source.index(INTERVIEW_END) + len(INTERVIEW_END)
    if end <= start: raise ValidationError('Interview markers are reversed')
    return source[:start] + source[end:]


def repository_path(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '://' in value:
        raise ValidationError('Expected a repository-relative evidence path')
    path = (Path(root).resolve() / value).resolve()
    if not path.is_relative_to(Path(root).resolve()): raise ValidationError('Path escapes repository')
    return path


def parsed_article(source):
    parser = ArticleParser(); parser.feed(source); parser.finish()
    return parser


def article_inventory(source):
    parser = parsed_article(source)
    cards = [e for e in parser.root.all('details') if e.has_class('kb-question')]
    return {
        'foundationalKeys': [e.attrs.get('data-recall-id') for e in cards if e.attrs.get('data-recall-kind', 'foundational') == 'foundational'],
        'interviewKeys': [e.attrs.get('data-recall-id') for e in cards if e.attrs.get('data-recall-kind') == 'interview'],
        'diagrams': sum(e.has_class('mermaid') for e in parser.root.all('pre')),
    }


def check_interviews(article, mastery, source, topic_id, *, research_presentation='disclosure-v1'):
    errors = []
    # Preservation markers belong to the backfill migration, not to new lessons.
    marked = INTERVIEW_START in source or INTERVIEW_END in source
    if marked:
        try: strip_interview_block(source)
        except ValidationError as exc: errors.append(str(exc))
    groups = [e for e in article.all() if 'data-interview-scenarios' in e.attrs]
    if len(groups) != 1:
        return errors + ['Expected exactly one interview subsection']
    group = groups[0]
    if group.tag != 'section' or not any(c is group for c in mastery.children):
        errors.append('Interview subsection must be a direct nested mastery section')
    heading_id = f'node-{topic_id}-interview-scenarios'
    headings = group.all('h3')
    if (len(headings) != 1 or headings[0].text() != INTERVIEW_TITLE or
            headings[0].attrs.get('id') != heading_id or group.attrs.get('aria-labelledby') != heading_id):
        errors.append('Expected exact interview heading, stable ID and accessible label')
    # The markers must delimit the new section itself, not an arbitrary unrelated span.
    if marked and not errors:
        span = source[source.index(INTERVIEW_START)+len(INTERVIEW_START):source.index(INTERVIEW_END)]
        fragment = parsed_article(span)
        top = [e for e in fragment.root.children if isinstance(e, Element)]
        if (fragment.errors or len(top) != 1 or top[0].tag != 'section' or
                'data-interview-scenarios' not in top[0].attrs or
                any(isinstance(e,str) and e.strip() for e in fragment.root.children)):
            errors.append('Marker span must contain only the complete interview subsection')
    group_cards = [e for e in group.all('details') if e.has_class('kb-question')]
    all_cards = [e for e in article.all('details') if e.has_class('kb-question')]
    foundational = []
    for card in all_cards:
        inside = any(e is card for e in group_cards)
        role = card.attrs.get('data-recall-kind', 'foundational')
        if role not in ('foundational', 'interview'): errors.append('Unknown recall role')
        if inside != (role == 'interview'): errors.append('Recall role/subsection placement mismatch')
        if not any(e is card for e in mastery.all('details')): errors.append('Recall card outside mastery')
        if any(e.has_class('kb-question') for e in card.all('details')): errors.append('Nested recall disclosure is forbidden')
        if role == 'foundational': foundational.append(card)
    if not 3 <= len(foundational) <= 5: errors.append('Expected three to five foundational recall items')
    if not 5 <= len(group_cards) <= 7: errors.append('Expected five to seven interview recall items')
    for card in group_cards:
        if not any(e is card for e in group.children): errors.append('Interview cards must be direct subsection children')
        key = card.attrs.get('data-recall-id', '')
        if not key.startswith('interview-') or not SLUG.fullmatch(key) or key == 'interview-':
            errors.append('Interview key needs a stable interview- kebab-case identity')
        if card.attrs.get('data-scenario-basis') not in ('adapted-production', 'reported-recurring', 'knowledge-based'):
            errors.append('Invalid scenario research basis')
        parts = [e for e in card.children if isinstance(e, Element) and 'data-scenario-part' in e.attrs]
        if [e.attrs['data-scenario-part'] for e in parts] != list(ANSWER_PARTS):
            errors.append('Expected exactly three ordered answer parts'); continue
        if len([e for e in card.all() if 'data-scenario-part' in e.attrs]) != 3:
            errors.append('Answer parts cannot be nested or duplicated')
        for part, label in zip(parts, ANSWER_PARTS.values()):
            paragraphs = [e for e in part.children if isinstance(e, Element) and e.tag == 'p']
            strong = [e for e in paragraphs[0].children if isinstance(e, Element) and e.tag == 'strong'] if paragraphs else []
            if part.tag != 'div' or len(strong) != 1 or strong[0].text() != label:
                errors.append('Missing exact visible constitutional answer label')
            if len(paragraphs) < 2 or not any(p.text() for p in paragraphs[1:]):
                errors.append('Answer part lacks explanatory prose after label')
    notes = [e for e in group.all() if 'data-interview-research' in e.attrs]
    if len(notes) != 1 or not notes[0].text() or not notes[0].all('a'):
        errors.append('Expected one visible research note with named source links')
    elif 'hidden' in notes[0].attrs or notes[0].attrs.get('aria-hidden') == 'true':
        errors.append('Research note must remain visible')
    elif any(any(e is notes[0] for e in c.all()) for c in group_cards):
        errors.append('Research note must be visible outside closed question cards')
    if research_presentation == 'sources-only-v1' and len(notes) == 1:
        note = notes[0]
        children = [e for e in note.children if isinstance(e, Element)]
        if (note.tag != 'aside' or not children or children[0].tag != 'h4' or children[0].text() != 'Sources'
                or len(note.all('h4')) != 1 or note.all('p')
                or any(e.tag not in ('ul','ol') for e in children[1:])
                or any(isinstance(e,str) and e.strip() for e in note.children)):
            errors.append('Current source group needs Sources heading and references without intro prose')
        for parent in [article] + article.all():
            if any(e is note for e in parent.all()) and (parent.tag == 'details' or 'hidden' in parent.attrs or parent.attrs.get('aria-hidden') == 'true'):
                errors.append('Sources cannot be inside hidden or collapsible content')
    elif research_presentation == 'disclosure-v1' and len(notes) == 1:
        if not notes[0].all('p'): errors.append('Historical research disclosure paragraph is required')
    elif research_presentation not in PRESENTATIONS:
        errors.append('Unknown research presentation')
    return errors


def check_article(item, source, index, *, recall_profile=CURRENT_PROFILE, research_presentation='disclosure-v1'):
    parser = ArticleParser(); parser.feed(source); parser.finish()
    errors = list(parser.errors)
    top = [c for c in parser.root.children if isinstance(c, Element)]
    if len(top) != 1 or top[0].tag != 'article': return errors + ['Exactly one root article is required']
    if any(isinstance(c,str) and c.strip() for c in parser.root.children): errors.append('Text outside root article')
    article = top[0]; node = item['node']; kind = node['kind']
    if research_presentation == 'sources-only-v1' and 'Continue by comparing the related decisions:' in article.text():
        errors.append('Related-topic filler preamble is forbidden')
    if article.attrs.get('data-node-id') != node['id']: errors.append('Article identity does not match manifest')
    if not article.has_class('kb-topic' if kind == 'topic' else 'kb-hub'): errors.append('Wrong article role class')
    headings = article.all('h1')
    if len(headings) != 1 or headings[0].text() != node['title']: errors.append('Expected one h1 with exact manifest title')
    if re.search(r'\bTODO\b|\bTBD\b|add explanation here|coming soon|lorem ipsum', source, re.I): errors.append('Unfinished content marker')
    elements = [article] + article.all()
    ids = set()
    for el in elements:
        if el.tag in {'html','head','body','script','style','link','iframe','object','embed','base','meta','form'}:
            errors.append(f'Forbidden element: {el.tag}')
        if any(k.lower().startswith('on') or k in ('style','srcdoc') for k in el.attrs): errors.append(f'Executable/inline style attribute on {el.tag}')
        identity = el.attrs.get('id')
        if identity:
            if identity in ids: errors.append(f'Duplicate DOM id: {identity}')
            ids.add(identity)
    for pre in article.all('pre'):
        if pre.has_class('mermaid') and not pre.text().strip(): errors.append('Empty Mermaid diagram')
    if kind == 'topic':
        sections = [c for c in article.children if isinstance(c,Element) and c.tag=='section']
        if [s.attrs.get('data-section') for s in sections] != list(SECTIONS):
            return errors + ['Missing or reordered six lesson modules']
        by_key = dict(zip(SECTIONS, sections))
        for key, section in by_key.items():
            if section.attrs.get('id') != f'node-{node["id"]}-{key}': errors.append(f'Wrong stable section id: {key}')
            if not section.all('h2') or not section.all('p'): errors.append(f'Module lacks heading or explanatory prose: {key}')
        if not any(el.has_class('mermaid') for el in by_key['big-picture'].all('pre')): errors.append('Big picture needs Mermaid diagram')
        mechanics = by_key['mechanics'].all('details')
        if not mechanics: errors.append('Mechanics needs native details')
        for detail in mechanics:
            summaries = [c for c in detail.children if isinstance(c,Element) and c.tag=='summary']
            answer = ' '.join(c.text() if isinstance(c,Element) else c for c in detail.children if c not in summaries).strip()
            if len(summaries)!=1 or not summaries[0].text() or not answer: errors.append('Empty mechanics step')
        tables = by_key['trade-offs'].all('table')
        if not tables or not any(len(t.all('th'))>=2 and len(t.all('tr'))>=2 for t in tables): errors.append('Missing structured decision table')
        pitfalls = by_key['pitfalls'].text()
        for label in ('Symptom','Root Cause','Fix/Prevention'):
            if label not in pitfalls: errors.append(f'Pitfalls missing {label}')
        mastery = by_key['mastery']
        if 'Summarize this in your own words' not in mastery.text(): errors.append('Missing Feynman prompt')
        questions = [el for el in mastery.all('details') if el.has_class('kb-question')]
        if recall_profile == CURRENT_PROFILE:
            errors.extend(check_interviews(article, mastery, source, node['id'], research_presentation=research_presentation))
        elif recall_profile == 'legacy-1.1':
            if not 3 <= len(questions) <= 5: errors.append('Expected three to five recall items')
        else: errors.append('Unknown recall profile')
        recall_ids = set()
        for question in questions:
            key = question.attrs.get('data-recall-id','')
            if not SLUG.fullmatch(key) or key in recall_ids: errors.append('Invalid/duplicate stable recall key')
            recall_ids.add(key)
            if 'open' in question.attrs or 'name' in question.attrs: errors.append('Recall must start closed without an exclusive group name')
            summaries = [c for c in question.children if isinstance(c,Element) and c.tag=='summary']
            answer = ' '.join(c.text() if isinstance(c,Element) else c for c in question.children if c not in summaries).strip()
            if len(summaries)!=1 or not summaries[0].text() or not answer: errors.append('Recall question/answer is empty')
        if not any(a.attrs.get('href','').startswith('https://') for a in article.all('a')): errors.append('Lesson needs primary-source reference links')
    if kind == 'hub':
        paragraphs = article.all('p')
        if len(paragraphs) < 2 or any(not p.text().strip() for p in paragraphs):
            errors.append('Hub needs complete introduction and reading guidance')
        if len(article.all('h2')) < 2: errors.append('Hub needs roadmap and reading guidance headings')
        if not any(el.has_class('mermaid') for el in article.all('pre')): errors.append('Hub needs Mermaid roadmap')
        lists = [el for el in article.all() if 'data-child-links' in el.attrs]
        if len(lists) != 1:
            errors.append('Hub needs one immediate-child link list')
        else:
            links = [(a.attrs.get('href'),a.text()) for a in lists[0].all('a')]
            expected = [('#'+item['route']+'/'+child['slug'],child['title']) for child in node['children']]
            if links != expected: errors.append('Hub child links must exactly match ordered immediate manifest children')
    errors.extend(check_links(article,index))
    return errors


CHECKERS['topic'] = check_article
CHECKERS['hub'] = check_article


def check_history(index, baseline, root):
    old_index = index_manifest(baseline, root, baseline=baseline)
    previous = {item['node']['id']: item['node'] for item in old_index.values()}
    current = {item['node']['id']: item['node'] for item in index.values()}
    errors = []
    core = {'id','kind','title','slug','children'}
    for identity, old in previous.items():
        new = current.get(identity)
        if new is None:
            errors.append(f'Previous node ID was dropped or replaced: {identity}'); continue
        if new['kind'] != old['kind']: errors.append(f'Node kind changed for ID: {identity}')
        for key, value in old.items():
            if key not in core and (key not in new or new[key] != value):
                errors.append(f'Existing optional metadata changed/lost for {identity}: {key}')
    return errors


def sha256(data): return hashlib.sha256(data).hexdigest()


def research_record(path):
    """A readable Markdown record carries one explicit, machine-checkable JSON map."""
    text = Path(path).read_text(encoding='utf-8')
    blocks = re.findall(r'```json\s*\n(.*?)\n```', text, re.S)
    if len(blocks) != 1: raise ValidationError('Research record needs exactly one JSON evidence map')
    try: value = json.loads(blocks[0])
    except json.JSONDecodeError as exc: raise ValidationError(f'Malformed research map: {exc}') from exc
    if not isinstance(value,dict): raise ValidationError('Research map must be an object')
    return value


EDITORIAL_CRITERIA = {'concept-specificity','distinctness','production-prompt','direct-answer',
                      'decision-costs','follow-up','evidence','full-delivery'}


def iso_date(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): return False
    try: date.fromisoformat(value); return True
    except ValueError: return False


def https_url(value):
    from urllib.parse import urlsplit
    if not isinstance(value,str): return False
    try:
        u=urlsplit(value)
        return u.scheme=='https' and bool(u.hostname) and not u.username and not u.password
    except ValueError: return False


def check_research(record, source, item, *, constitution_versions=('1.2.0',), research_presentation='disclosure-v1'):
    """Check evidence shape and claim/basis consistency, not source credibility or prose quality."""
    errors=[]
    if research_presentation not in PRESENTATIONS: errors.append('Unknown research presentation')
    if record.get('state') not in ('draft','reviewed'): errors.append('Research state must be draft or reviewed')
    if record.get('constitutionVersion') not in constitution_versions: errors.append('Research constitution version mismatch')
    if record.get('title')!=item['node']['title']: errors.append('Research exact concept title mismatch')
    if not iso_date(record.get('researchedOn')): errors.append('Research requires actual ISO date')
    searches=record.get('searches')
    if not isinstance(searches,list) or not searches: errors.append('Missing actual search records'); searches=[]
    for search in searches:
        if not isinstance(search,dict) or not all(isinstance(search.get(k),str) and search[k].strip() for k in ['query','result']) or not iso_date(search.get('date')):
            errors.append('Search needs actual query/date/result or failure')
    searches=[s for s in searches if isinstance(s,dict)]
    sources=record.get('sources')
    if not isinstance(sources,list) or not sources: errors.append('Missing primary sources'); sources=[]
    if any(not isinstance(s,dict) for s in sources):errors.append('Invalid source record')
    sources=[s for s in sources if isinstance(s,dict)]
    by_id={}
    for entry in sources:
        if not isinstance(entry,dict): errors.append('Invalid source record'); continue
        key=entry.get('id')
        if not isinstance(key,str) or not key: errors.append('Source IDs must be unique and nonempty'); continue
        if key in by_id: errors.append('Source IDs must be unique and nonempty')
        by_id[key]=entry
        if not https_url(entry.get('url')) or not entry.get('title') or not entry.get('supportRationale'):
            errors.append('Source needs named HTTPS URL and support rationale')
        roles=entry.get('roles')
        if not isinstance(roles,list) or not roles or any(not isinstance(role,str) or role not in {'technical-primary','interview-evidence'} for role in roles):
            errors.append('Invalid source role')
        if not iso_date(entry.get('checkedOn')) and not entry.get('limitation'):
            errors.append('Source requires actual check date or explicit limitation')
    parser=parsed_article(source)
    cards=[e for e in parser.root.all('details') if e.attrs.get('data-recall-kind')=='interview']
    rows=record.get('scenarios')
    if not isinstance(rows,list) or not 5<=len(rows)<=7 or any(not isinstance(row,dict) for row in rows):
        errors.append('Research needs five to seven scenario mappings');rows=[]
    if [r.get('key') for r in rows] != [c.attrs.get('data-recall-id') for c in cards]:
        errors.append('Research keys must exactly match allocated lesson keys and order')
    for row,card in zip(rows,cards):
        if not all(row.get(k) for k in ['theme','assumptions','limitations']): errors.append('Scenario mapping lacks theme or assumptions/limitations')
        for field_name in ['selectionSources','technicalSources']:
            refs=row.get(field_name)
            if not isinstance(refs,list) or not refs or any(ref not in by_id for ref in refs):
                errors.append('Scenario has unresolved source mapping')
        technical=[by_id[x] for x in row.get('technicalSources',[]) if x in by_id]
        if not any('technical-primary' in s.get('roles',[]) and iso_date(s.get('checkedOn')) for s in technical):
            errors.append('Technical answer needs checked primary-source support')
        basis=row.get('basis');claim=row.get('supportedInterviewClaim')
        if basis!=card.attrs.get('data-scenario-basis'): errors.append('Research/HTML basis mismatch')
        if basis=='reported-recurring':
            evidence=[by_id[x] for x in row.get('selectionSources',[]) if x in by_id]
            if not claim or claim=='none' or not any('interview-evidence' in s.get('roles',[]) for s in evidence):
                errors.append('Reported recurrence needs explicit interview evidence and supported claim')
        elif basis in ('adapted-production','knowledge-based'):
            if claim!='none': errors.append('Adapted/knowledge-based card cannot assert interview frequency')
            if basis=='knowledge-based' and not any(re.search(r'fail|unavailable',s.get('result',''),re.I) for s in searches):
                errors.append('Knowledge fallback requires actual failed/unavailable search evidence')
        else: errors.append('Unknown research classification')
        editorial=row.get('editorial',{})
        if not isinstance(editorial,dict) or set(editorial)!=EDITORIAL_CRITERIA:
            errors.append('Every scenario needs all eight editorial dispositions'); continue
        for finding in editorial.values():
            if (not isinstance(finding,dict) or finding.get('status') not in ('pass','fail') or
                    not isinstance(finding.get('rationale'),str) or not finding['rationale'].strip()):
                errors.append('Editorial disposition needs explicit status and finding')
            elif record.get('state')=='reviewed' and finding['status']!='pass':
                errors.append('Reviewed research cannot retain failing editorial dispositions')
    notes=[e for e in parser.root.all() if 'data-interview-research' in e.attrs]
    if len(notes)==1:
        ps=notes[0].all('p');public=ps[0].text() if ps else ''
        if research_presentation == 'disclosure-v1' and record.get('publicDisclosure')!=public: errors.append('Exact public disclosure differs from research record')
        urls=[a.attrs.get('href') for a in notes[0].all('a')]
        if record.get('sourceNoteUrls')!=urls or set(urls)!={s.get('url') for s in sources}:
            errors.append('Public source links do not match final source record')
        if research_presentation == 'disclosure-v1' and any(r.get('basis')=='adapted-production' for r in rows) and not ('adapt' in public.lower() and 'not independently verified' in public.lower()):
            errors.append('Adapted scenarios require visible frequency limitation')
        if research_presentation == 'disclosure-v1' and 'search was unavailable' in public.lower() and any('success' in s.get('result','').lower() for s in searches):
            errors.append('Public unavailable-search claim contradicts successful research')
    return errors


def migration_inputs(root, expected):
    fields = ['preservationBaseline','scenarioResearchDirectory','completionRecord','deliveryRecord']
    paths = {name:repository_path(root,expected.get(name)) for name in fields}
    for name,path in paths.items():
        if not (path.is_dir() if name == 'scenarioResearchDirectory' else path.is_file()):
            raise ValidationError(f'Missing migration evidence: {name}')
    audit = load_json(paths['preservationBaseline'])
    if audit.get('schemaVersion') != 1 or len(audit.get('lessons',[])) != 15 or len(audit.get('hubs',[])) != 6:
        raise ValidationError('Invalid frozen migration inventory')
    completion = load_json(paths['completionRecord'])
    digest = sha256(paths['preservationBaseline'].read_bytes())
    if completion.get('schemaVersion') != 1 or completion.get('baselineSha256') != digest:
        raise ValidationError('Completion record does not reference frozen baseline digest')
    lessons = completion.get('lessons',[])
    if len(lessons) != 15 or {e.get('topicId') for e in lessons} != {e['id'] for e in audit['lessons']}:
        raise ValidationError('Completion record must identify exactly the 15 immutable topics')
    for record in [audit['manifest'], *audit['hubs']]:
        if sha256(repository_path(root,record['path']).read_bytes()) != record['sha256']:
            raise ValidationError(f'Protected manifest/hub changed: {record["path"]}')
    actual_runtime={relative:sha256(repository_path(root,relative).read_bytes()) for relative in audit['runtimeFiles']}
    changed={relative for relative,digest in audit['runtimeFiles'].items() if actual_runtime[relative]!=digest}
    if changed:
        reference=expected.get('runtimeCompatibilityRecord')
        if not reference:raise ValidationError('Runtime changes require an explicit reviewed compatibility record')
        path=repository_path(root,reference);fix=load_json(path)
        if (not isinstance(fix,dict) or fix.get('schemaVersion')!=1 or fix.get('status')!='reviewed' or
                fix.get('baselineSha256')!=digest or not fix.get('rationale') or not https_url(fix.get('reference'))):
            raise ValidationError('Invalid runtime compatibility review')
        files=fix.get('files',[])
        if not isinstance(files,list) or any(not isinstance(x,dict) for x in files):raise ValidationError('Invalid runtime exception file list')
        permitted={x.get('path'):x for x in files}
        if len(permitted)!=len(files) or set(permitted)!=changed:
            raise ValidationError('Runtime exception must cover exactly the observed changed files')
        for relative in changed:
            item=permitted[relative]
            if item.get('beforeSha256')!=audit['runtimeFiles'][relative] or item.get('afterSha256')!=actual_runtime[relative] or not item.get('reason'):
                raise ValidationError('Unexpected runtime bytes or unreviewed compatibility change: '+relative)
        if all(e.get('status')=='pass' for e in lessons):
            if fix.get('regressionStatus')!='pass':raise ValidationError('Runtime fix lacks completed regression acceptance')
            references=fix.get('regressionEvidence',[])
            if not references:raise ValidationError('Runtime fix requires regression evidence')
            for ref in references:
                evidence=load_json(repository_path(root,ref))
                if evidence.get('status',evidence.get('result'))!='pass' or any(evidence.get('runtimeFileHashes',{}).get(name)!=actual_runtime[name] for name in changed):
                    raise ValidationError('Runtime regression evidence is failing or stale')
        paths['runtimeCompatibilityRecord']=path
    return audit, completion, paths


def check_migration_lesson(item, source, audit, completion, paths, root):
    errors = []
    frozen = next((x for x in audit['lessons'] if x['path']==item['relative_path']),None)
    if not frozen: return ['Lesson is outside fixed migration inventory']
    node=item['node']
    if (node['id'],node['title'],item['route'],node['kind']) != (frozen['id'],frozen['title'],frozen['route'],'topic'):
        errors.append('Original lesson identity/path/route changed')
    original=None
    try:
        original=strip_interview_block(source)
        if sha256(original.encode('utf-8')) != frozen['sourceSha256']:
            errors.append('Protected original source changed outside interview marker span')
    except ValidationError as exc: errors.append(str(exc))
    if original is not None:
        # Additional diagnostics accompany the stronger complete-source comparison.
        for section in frozen.get('sections',[]):
            pattern=r'<section\b[^>]*\bdata-section="'+re.escape(section['key'])+r'"[^>]*>.*?</section>'
            match=re.search(pattern,original,re.S)
            if not match or sha256(match[0].encode('utf-8'))!=section['sha256']:
                errors.append('Protected section bytes changed: '+section['key'])
        for card in frozen['foundationalRecall']:
            if 'htmlSha256' not in card: continue
            match=re.search(r'<details\b[^>]*\bdata-recall-id="'+re.escape(card['key'])+r'"[^>]*>.*?</details>',original,re.S)
            if not match or sha256(match[0].encode('utf-8'))!=card['htmlSha256']:
                errors.append('Protected foundational answer changed: '+card['key'])
        if 'diagramSourcesSha256' in frozen:
            import html
            diagrams=[sha256(html.unescape(m).encode('utf-8')) for m in re.findall(r'<pre\b[^>]*\bclass="mermaid"[^>]*>(.*?)</pre>',original,re.S)]
            if diagrams!=frozen['diagramSourcesSha256']:errors.append('Original diagram source inventory changed')
    inventory=article_inventory(source)
    old_keys=[x['key'] for x in frozen['foundationalRecall']]
    if inventory['foundationalKeys'] != old_keys: errors.append('Original foundational key order changed')
    research=paths['scenarioResearchDirectory']/(Path(frozen['path']).stem+'.md')
    record={}
    try:
        record=research_record(research)
        if record.get('topicId') != node['id'] or record.get('path') != frozen['path']:
            errors.append('Research topic identity mismatch')
        if [x.get('key') for x in record.get('scenarios',[])] != inventory['interviewKeys']:
            errors.append('Research scenario key mapping mismatch')
        # Minimal synthetic helper fixtures lack the migration record version; production maps must include it.
        if 'constitutionVersion' in record or root.joinpath('manifest.json').is_file():
            errors.extend(check_research(record,source,item))
    except (OSError,ValidationError,KeyError,TypeError) as exc:
        errors.append(f'Research evidence: {exc}')
    entry=next(x for x in completion['lessons'] if x['topicId']==node['id'])
    if entry.get('path') != frozen['path'] or entry.get('foundationalKeys') != old_keys:
        errors.append('Completion original identity/key mismatch')
    # An author writes only its local report; consolidation assigns shared new keys later.
    if entry.get('interviewKeys') and entry['interviewKeys'] != inventory['interviewKeys']:
        errors.append('Allocated scenario identities changed from completion inventory')
    gates=entry.get('checks',{})
    if set(gates) != {'preservation','structure','editorial','browser','print'}:
        errors.append('Completion requires all five gates')
    elif any(g.get('status') not in ('pending','pass','fail') for g in gates.values()):
        errors.append('Invalid completion disposition')
    elif entry.get('status') == 'pass' and any(g['status']!='pass' for g in gates.values()):
        errors.append('Overall pass requires all five passing gates')
    if entry.get('status') not in ('pending','pass','fail'): errors.append('Invalid overall lesson disposition')
    if entry.get('status')=='pass':
        if entry.get('sourceSha256')!=sha256(source.encode('utf-8')):
            errors.append('Passing completion record has stale source digest')
        if entry.get('interviewKeys')!=inventory['interviewKeys']: errors.append('Passing completion must allocate every scenario key')
        if record.get('state')!='reviewed': errors.append('Passing completion requires reviewed research')
        for name,gate in gates.items():
            references=gate.get('evidence')
            if not isinstance(references,list) or not references: errors.append('Passing gate needs evidence references'); continue
            for relative in references:
                try:
                    path=repository_path(root,relative)
                    evidence=load_json(path)
                    if evidence.get('status',evidence.get('result'))!='pass':
                        errors.append(f'{name} evidence is not passing')
                    own=evidence if evidence.get('topicId')==node['id'] else next((e for e in evidence.get('lessons',[]) if e.get('topicId')==node['id']),{})
                    if own.get('sourceSha256')!=sha256(source.encode('utf-8')):
                        errors.append(f'{name} evidence is missing current per-lesson source proof')
                    if name=='print' and {x.get('theme') for x in own.get('outputs',[])}!={'light','dark'}:
                        errors.append('Print evidence must include both themes for this lesson')
                except (OSError,ValidationError,TypeError,AttributeError): errors.append(f'Invalid {name} evidence path or shape')
    return errors


def validate(root, expected, baseline=None, *, lesson=None):
    root = Path(root).resolve()
    report = dict(profile=expected.get('profile','custom'), phase='intrinsic', result='fail', counts={}, checks=[], integrationStatus='pending', scope='lesson' if lesson else 'batch', recallProfile=CURRENT_PROFILE, lessons=[])
    if lesson: report['selectedLesson']=lesson
    def check(name, status, artifact, message):
        report['checks'].append(dict(name=name, status=status, artifact=str(artifact), message=message))
    presentation = expected.get('researchPresentation', 'disclosure-v1')
    report['researchPresentation'] = presentation
    try:
        if presentation not in PRESENTATIONS or (expected.get('profile') == 'topic-publishing' and expected.get('researchPresentation') != 'sources-only-v1'):
            raise ValidationError('Current publishing requires explicit sources-only-v1 research presentation')
        if expected.get('recallProfile',CURRENT_PROFILE) != CURRENT_PROFILE:
            raise ValidationError('Production validation cannot waive the current recall profile')
        manifest = load_json(root / 'manifest.json')
        index = index_manifest(manifest, root, baseline)
        counts = (validate_expectation(index, expected) if 'groups' in expected else
                  {kind+'s':sum(i['node']['kind']==kind for i in index.values()) for kind in ('topic','hub')})
        report['counts'] = dict(totalNodes=len(index), batch=counts)
        check('catalog', 'pass', 'manifest.json', 'Shape, identities, derived targets and requested membership verified')
    except ValidationError as exc:
        check('catalog', 'fail', 'manifest.json', str(exc)); return report
    migration = expected.get('profile') == 'backend-architecture' or 'preservationBaseline' in expected
    audit = completion = paths = None
    try:
        if migration:
            if expected.get('recallProfile') != CURRENT_PROFILE: raise ValidationError('Current batch must explicitly record recallProfile')
            audit, completion, paths = migration_inputs(root, expected)
            if 'runtimeCompatibilityRecord' in paths:
                report['runtimeCompatibility']=load_json(paths['runtimeCompatibilityRecord'])
            check('preservation-inputs','pass',expected['preservationBaseline'],'Frozen catalog/hubs and evidence identities verified; runtime hashes match baseline or the explicit compatibility review')
        if lesson:
            selected=repository_path(root,lesson)
            if selected != root/lesson or (migration and lesson not in {x['path'] for x in audit['lessons']}):
                raise ValidationError('Scoped target must be one exact in-scope baseline lesson path')
    except (ValidationError,OSError,KeyError,TypeError) as exc:
        check('migration-inputs','fail',lesson or 'evidence',str(exc)); return report
    selected_items=[item for item in index.values() if not lesson or item['relative_path']==lesson]
    if lesson and len(selected_items)!=1:
        check('scope','fail',lesson,'Scoped lesson is not present in catalog'); return report
    for item in selected_items:
        relative = item['relative_path']
        if not item['path'].is_file():
            check('content', 'fail', relative, 'Required partial is missing'); continue
        checker = CHECKERS.get(item['node']['kind'])
        if checker is None:
            check('content-contract', 'pending', relative, 'Required content checks are not yet available'); continue
        try:
            # Preserve CRLF and every other original byte for exact migration hashes.
            source = item['path'].read_bytes().decode('utf-8')
        except (OSError, UnicodeError) as exc:
            check('content', 'fail', relative, f'Unreadable partial: {exc}'); continue
        errors = checker(item, source, index, research_presentation=presentation)
        if item['node']['kind']=='topic':
            inventory=article_inventory(source)
            inventory.update(topicId=item['node']['id'],path=relative,sourceSha256=sha256(source.encode('utf-8')))
            inventory['acceptance']={name:'pending' for name in ['editorial','browser','print']}
            if completion:
                entry=next((x for x in completion['lessons'] if x['topicId']==item['node']['id']),{})
                inventory['acceptance']={name:entry.get('checks',{}).get(name,{}).get('status','pending') for name in ['editorial','browser','print']}
            report['lessons'].append(inventory)
            if audit: errors.extend(check_migration_lesson(item,source,audit,completion,paths,root))
            elif expected.get('researchDirectory'):
                relative_record = expected.get('researchRecords',{}).get(item['node']['id'],
                    expected['researchDirectory']+'/'+item['node']['id']+'.json')
                try:
                    path = repository_path(root, relative_record)
                    record = research_record(path) if path.suffix == '.md' else load_json(path)
                    if record.get('topicId') != item['node']['id'] or record.get('path') != relative:
                        errors.append('Research identity/path differs from manifest')
                    if record.get('state') != 'reviewed': errors.append('Publishing requires reviewed research')
                    errors.extend(check_research(record,source,item,constitution_versions=('1.2.0','1.3.0','2.0.0'),research_presentation=presentation))
                except (OSError,ValidationError,TypeError,AttributeError) as exc:
                    errors.append(f'Invalid/missing research record {relative_record}: {exc}')
        report['counts'].setdefault('diagrams',0)
        report['counts']['diagrams'] += article_inventory(source)['diagrams']
        check('content', 'fail' if errors else 'pass', relative, '; '.join(errors) if errors else 'Content contract and references verified')
    known_files = {item['path'] for item in index.values()}
    orphan_files = [str(path.relative_to(root)) for path in (root / 'topics').rglob('*.html') if path.resolve() not in known_files]
    check('files', 'fail' if orphan_files else 'pass', 'topics/', 'Unregistered HTML partials: '+', '.join(orphan_files) if orphan_files else 'No unregistered HTML partials')
    if baseline is None:
        check('history', 'pending', 'manifest.json', 'No prior catalog supplied; initial-node format was checked')
    else:
        try:
            history_errors = check_history(index, baseline, root)
        except ValidationError as exc:
            history_errors = [str(exc)]
        check('history', 'fail' if history_errors else 'pass', 'manifest.json', '; '.join(history_errors) if history_errors else 'Previous IDs, kinds and optional metadata preserved')
    record = expected.get('deliveryRecord')
    if record:
        path = (root / record).resolve()
        valid_record = path.is_relative_to(root) and path.is_file()
        if valid_record:
            valid_record = bool(path.read_text(encoding='utf-8').strip())
        check('bundle', 'pass' if valid_record else 'fail', record, 'Delivery record exists; content paths were individually checked' if valid_record else 'Required delivery record is missing/empty or escapes repository')
    required = [c for c in report['checks'] if c['name'] != 'history' or baseline is not None]
    report['result'] = 'pass' if all(c['status'] == 'pass' for c in required) else 'fail'
    report['counts']['foundationalRecall']=sum(len(x['foundationalKeys']) for x in report['lessons'])
    report['counts']['interviewRecall']=sum(len(x['interviewKeys']) for x in report['lessons'])
    report['counts']['recallQuestions']=report['counts']['foundationalRecall']+report['counts']['interviewRecall']
    if completion and not lesson and all(x['status']=='pass' for x in completion['lessons']):
        report['integrationStatus']='pass'
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path('.'))
    parser.add_argument('--expect', type=Path)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--lesson', help='Exact repository-relative catalog partial path (authoring check)')
    args = parser.parse_args(argv)
    try:
        expected = load_json(args.expect or args.repo_root / 'tests/content/publishing.json')
        baseline = load_json(args.baseline) if args.baseline else None
        report = validate(args.repo_root, expected, baseline, lesson=args.lesson)
    except (OSError, UnicodeError) as exc:
        print(f'Unreadable input: {exc}', file=sys.stderr); return 2
    except (ValidationError, KeyError, TypeError) as exc:
        report = dict(profile='unknown', phase='intrinsic', result='fail', counts={}, integrationStatus='pending',
                      checks=[dict(name='input',status='fail',artifact='input',message=str(exc))])
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['result'] == 'pass' else 1


if __name__ == '__main__': sys.exit(main())
