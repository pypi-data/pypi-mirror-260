import os
import typing
import uuid
import xml.etree.ElementTree as etree
import datetime
import re


class ValidationException(Exception):
    def __init__(self, message: str):
        self.message = message


class Context:
    def __init__(self, base_path: str = '.', default_time: int = 5):
        self.base_path = base_path
        self.default_time = default_time


class Package:
    def __init__(
            self, name: str, difficulty: int, uid: str = None, date: str = None,
            language: str = None, restriction: str = None, publisher: str = None,
            logo_path: str = None, rounds: list = None):
        self.id = uid or str(uuid.uuid4())
        self.name = name
        self.language = language
        self.difficulty = int(difficulty)
        self.date = date or datetime.date.today().strftime('%d.%m.%Y')
        self.authors = []
        self.logo_path = logo_path
        self.sources = []
        self.comments = None
        self.rounds = rounds or []
        self.restriction = restriction
        self.publisher = publisher

    @property
    def logo_name(self):
        return os.path.basename(self.logo_path)

    @classmethod
    def from_xml(cls, root_node, context: Context = None):
        m = re.match(r'{(.+)}(\w+)', root_node.tag)
        if not m or m.group(2) != 'package':
            raise ValueError(f'Root node is "{m.group(2)}", expected "package".')
        ns = {'x': m.group(1)}
        # Parse root node attributes
        logo = root_node.get('logo')
        logo_path = None
        if logo:
            logo_path = resolve_path('image', logo[1:], context)
        p = cls(
            root_node.get('name'),
            uid=root_node.get('id'),
            difficulty=root_node.get('difficulty'),
            date=root_node.get('date'),
            language=root_node.get('language'),
            publisher=root_node.get('publisher'),
            restriction=root_node.get('restriction'),
            logo_path=logo_path
        )
        # Parse info
        info = root_node.find('x:info', ns)
        if info is not None:
            a = info.find('x:authors', ns)
            if a is not None:
                p.authors = [n.text for n in a]
            s = info.find('x:sources', ns)
            if s is not None:
                p.sources = [n.text for n in s]
            c = info.find('x:comments', ns)
            if c is not None:
                p.comments = c.text
        # Parse rounds
        rs = root_node.find('x:rounds', ns)
        for r in rs:
            p.rounds.append(Round.from_xml(r, ns, context=context))
        return p

    @classmethod
    def from_yaml(cls, root, context: Context = None):
        logo = root.get('logo')
        logo_path = None
        if logo:
            logo_path = resolve_path('image', logo, context)
        p = cls(
            root['name'],
            uid=root.get('id'),
            difficulty=root['difficulty'],
            date=root.get('date'),
            language=root.get('language'),
            restriction=root.get('restriction'),
            publisher=root.get('publisher'),
            logo_path=logo_path,
        )
        a = root.get('authors')
        if not a:
            raise ValidationException('Package should have "authors" with at least one name')
        if isinstance(a, list):
            p.authors = a
        else:
            p.authors = [str(a)]
        s = root.get('sources')
        if s:
            if isinstance(s, list):
                p.sources = s
            else:
                p.sources = [str(s)]
        p.comments = root.get('comments')
        for k, v in root.items():
            if k.startswith('round'):
                p.rounds.append(Round.from_yaml(v, context=context))
        if not p.rounds:
            raise ValidationException('Package does not have a single round')
        return p

    def to_xml(self, context: Context = None):
        """Returns <package><info></info></package> root node."""
        package = etree.Element('package', {
            'xmlms': 'http://vladimirkhil.com/ygpackage3.0.xsd',
            'name': self.name,
            'version': '4',
            'difficulty': str(self.difficulty),
            'id': self.id,
            'date': self.date,
            'generator': 'si_convert',
        })
        if self.language:
            package.set('language', self.language)
        if self.publisher:
            package.set('published', self.publisher)
        if self.restriction:
            package.set('restriction', self.restriction)
        if self.logo_path:
            logo = f'@{self.logo_name}'
            package.set('logo', logo)
        info = etree.SubElement(package, 'info')
        if self.authors:
            authors = etree.SubElement(info, 'authors')
            for a in self.authors:
                etree.SubElement(authors, 'author').text = a
        if self.sources:
            sources = etree.SubElement(info, 'sources')
            for a in self.sources:
                etree.SubElement(sources, 'source').text = a
        if self.comments:
            c = etree.SubElement(info, 'comments')
            c.text = self.comments
        rounds = etree.SubElement(package, 'rounds')
        for r in self.rounds:
            rounds.append(r.to_xml(context=context))
        return package

    def to_yaml(self, context: Context = None) -> dict:
        res = {
            'name': self.name,
            'id': self.id,
            'difficulty': self.difficulty,
            'date': self.date,
        }
        if self.language:
            res['language'] = self.language
        if self.publisher:
            res['publisher'] = self.publisher
        if self.restriction:
            res['restriction'] = self.restriction
        if self.authors:
            res['authors'] = self.authors
        if self.sources:
            res['sources'] = self.sources
        if self.comments:
            res['comments'] = self.comments
        if self.logo_path:
            res['logo'] = self.logo_name
        for i, r in enumerate(self.rounds):
            res[f'round{i+1}'] = r.to_yaml(context=context)
        return res


class Round:
    def __init__(self, name: str, is_final: bool = False, themes: list = None):
        self.name = name
        self.is_final = is_final
        self.themes = themes or []
        self.prices = None

    @classmethod
    def from_xml(cls, node, ns: dict, context: Context = None):
        r = cls(node.get('name'))
        if node.get('type') == 'final':
            r.is_final = True
        for theme in node.find('x:themes', ns):
            t = Theme(theme.get('name'))
            for q in theme.find('x:questions', ns):
                t.questions.append(Question.from_xml(q, t, ns, context=context))
            if not r.is_final:
                prices = [q.value for q in t.questions]
                if r.prices is None:
                    r.prices = prices
                elif r.prices != prices:
                    raise ValidationException(f'Cannot parse rounds with different prices for themes: "{r.name}"')
            r.themes.append(t)
        return r

    @classmethod
    def from_yaml(cls, node: dict, context: Context = None):
        if 'name' not in node:
            raise ValidationException('One of the rounds does not have a name')
        r = cls(node['name'])
        if node.get('final'):
            r.is_final = True
        r.prices = node.get('prices')
        for tnode in node.get('themes', []):
            if 'name' not in tnode:
                raise ValidationException(f'One of the themes in round "{r.name}" does not have a name')
            t = Theme(tnode['name'])
            for v in tnode['questions']:
                q = Question.from_yaml(v, t, context=context)
                t.questions.append(q)
            if not t.questions:
                raise ValidationException(f'Theme "{t.name}" in round "{r.name}" does not have a single question')
            if r.prices and len(t.questions) != len(r.prices):
                raise ValidationException(f'Expected {len(r.prices)} questions for theme "{t.name}", round "{r.name}"')
            r.themes.append(t)
        if not r.themes:
            raise ValidationException(f'Round "{r.name}" does not have a single theme')
        return r

    def to_xml(self, context: Context = None):
        r = etree.Element('round', {'name': self.name})
        if self.is_final:
            r.set('type', 'final')
        ts = etree.SubElement(r, 'themes')
        for t in self.themes:
            tn = etree.SubElement(ts, 'theme', {'name': t.name})
            qs = etree.SubElement(tn, 'questions')
            for i, q in enumerate(t.questions):
                if self.is_final:
                    price = 0
                elif self.prices and i < len(self.prices):
                    price = self.prices[i]
                else:
                    price = q.value or 100
                qs.append(q.to_xml(price, context=context))
        return r

    def to_yaml(self, context: Context = None):
        r = {'name': self.name, 'themes': []}
        if self.prices:
            r['prices'] = self.prices
        if self.is_final:
            r['final'] = True
        for t in self.themes:
            r['themes'].append({
                'name': t.name,
                'questions': [q.to_yaml(context=context) for q in t.questions]
            })
        return r


class Theme:
    def __init__(self, name: str, questions: list = None):
        self.name = name
        self.questions = questions or []


DIRNAMES = {
    'image': 'Images',
    'voice': 'Audio',
    'video': 'Video',
}


class QAtom:
    def __init__(self, typ: str, time: typing.Optional[int], value: str, path: str = None):
        self.type = typ
        self.time = time
        self.value = value
        self.path = path

    @property
    def dirname(self) -> str:
        return DIRNAMES.get(self.type)


class Question:
    def __init__(self, value=None, typ: str = None, scenario: list = None):
        self.type = typ
        self.value = value
        self.scenario = scenario or []
        self.right = []
        self.wrong = []
        self.cost = None
        self.theme = None
        self.comments = None
        self.to_self = False
        self.knows = None

    @classmethod
    def from_xml(cls, node, theme: Theme, ns: dict, context: Context = None):
        q = cls(value=int(node.get('price')))
        typ = node.find('x:type', ns)
        if typ is not None:
            q.type = typ.get('name')
            params = {}
            for p in typ.findall('x:param', ns):
                params[p.get('name')] = p.text.strip()
            if q.type in ('cat', 'bagcat'):
                m = re.match(r'\[(\d+);(\d+)\]/?(\d+)?', params['cost'])
                if m:
                    cnt = 2 if not m.group(3) else 3
                    q.cost = [int(m.group(i)) for i in range(1, cnt+1)]
                else:
                    q.cost = int(params['cost'])
                q.theme = params.get('theme') or theme.name
                if q.type == 'bagcat':
                    q.to_self = params.get('self') == 'true'
                    q.knows = params.get('knows') or 'before'
        sc = node.find('x:scenario', ns)
        for atom in sc.findall('x:atom', ns):
            time = None
            if atom.get('time'):
                time = int(atom.get('time'))
            atype = atom.get('type')
            if not atype or atype == 'text':
                a = QAtom('text', time, atom.text)
            elif atype in {'say', 'marker'}:
                a = QAtom(atype, time, atom.text)
            elif atype in {'image', 'voice', 'video'}:
                a = QAtom(atype, time, atom.text[1:])
                path = resolve_path(a.type, a.value, context)
                if not path:
                    raise ValidationException(f'Missing file {a.value} in question for {q.value}, theme "{theme.name}"')
                a.path = path
            else:
                raise ValidationException(f'Unknown atom type in question for {q.value} in theme "{theme.name}"')
            q.scenario.append(a)
        if not q.scenario:
            raise ValidationException(f'No scenario in question for {q.value} in theme "{theme.name}"')
        right = node.find('x:right', ns)
        if right is not None:
            for answer in right:
                q.right.append(answer.text)
        wrong = node.find('x:wrong', ns)
        if wrong is not None:
            for answer in wrong:
                q.wrong.append(answer.text)
        info = node.find('x:info', ns)
        if info is not None:
            c = info.find('x:comments', ns)
            if c is not None:
                q.comments = c.text
        return q

    @classmethod
    def from_yaml(cls, node: dict, theme: Theme, value='unknown', context: Context = None):
        q = cls(typ=node.get('type'))
        if q.type in ('cat', 'bagcat'):
            if 'cost' not in node:
                q.cost = 100
            elif isinstance(node['cost'], int):
                q.cost = node['cost']
            elif isinstance(node['cost'], (tuple, list)):
                if q.type != 'bagcat':
                    raise ValidationException(f'Variable cost is applicable only to bagcat type questions, see q{value} for theme "{theme.name}"')
                if len(node['cost']) != 3:
                    raise ValidationException(f'Variable cost should have 3 items. Question {value}, theme "{theme.name}"')
                q.cost = node['cost']
            else:
                raise ValidationException(f'Cost should be either a number or a 3-item list for question {value} in theme "{theme.name}"')
        if q.type == 'bagcat':
            q.to_self = node.get('self') is True
            q.knows = node.get('knows') or 'before'
        q.theme = node.get('theme') or theme.name

        if 'scenario' in node:
            scenario = node['scenario']
        else:
            scenario = [node]
        for atom in scenario:
            time = int(atom['time']) if 'time' in atom else None
            # Attempt to create a QAtom object with the first matching key in the atom dictionary.
            for key in atom:
                if key in ['text', 'say', 'image', 'voice', 'video', 'marker']:
                    a = QAtom(key, time, atom[key])
                    break
            else:
                raise ValidationException(f'Unknown atom type in question for {value} in theme "{theme.name}"')
            if a.type in ('image', 'voice', 'video'):
                path = resolve_path(a.type, a.value, context)
                if not path:
                    raise ValidationException(f'Missing file {a.value} in question for {value}, theme "{theme.name}"')
                a.path = path
            q.scenario.append(a)
        if not q.scenario:
            raise ValidationException(f'No scenario in question for {value} in theme "{theme.name}"')
        rights = []
        wrongs = []
        for k, v in node.items():
            if k.startswith('answer'):
                i = int(k[6:] or '1')
                rights.append((i, v))
            elif k.startswith('wrong'):
                i = int(k[5:] or '1')
                wrongs.append((i, v))
        q.right = [a[1] for a in sorted(rights)]
        q.wrong = [a[1] for a in sorted(wrongs)]
        if not q.right:
            raise ValidationException(f'No right answers listed for question for {value} in theme "{theme.name}"')
        q.comments = node.get('comments')
        return q

    def to_xml(self, value: int = None, context: Context = None):
        q = etree.Element('question')
        if value is not None:
            q.set('price', str(value))
        if self.comments:
            info = etree.SubElement(q, 'info')
            etree.SubElement(info, 'comments').text = self.comments
        if self.type:
            typ = etree.SubElement(q, 'type', {'name': self.type})
            params = {}
            if self.type in ('cat', 'bagcat'):
                params['theme'] = self.theme
                if isinstance(self.cost, int):
                    params['cost'] = str(self.cost)
                else:
                    params['cost'] = f'[{self.cost[0]};{self.cost[1]}]/{self.cost[2]}'
            if self.type == 'bagcat':
                params['self'] = 'true' if self.to_self else 'false'
                params['knows'] = self.knows
            for k, v in params.items():
                etree.SubElement(typ, 'param', {'name': k}).text = str(v)
        sc = etree.SubElement(q, 'scenario')
        for atom in self.scenario:
            a = etree.SubElement(sc, 'atom', {'type': atom.type})
            default_time = 3 if not context else context.default_time
            time = atom.time or default_time
            if time:
                a.set('time', str(time))
            if atom.type in ('image', 'voice', 'video'):
                a.text = f'@{atom.value}'
            else:
                a.text = atom.value
        right = etree.SubElement(q, 'right')
        for a in self.right:
            etree.SubElement(right, 'answer').text = a
        wrong = etree.SubElement(q, 'wrong')
        for a in self.wrong:
            etree.SubElement(wrong, 'answer').text = a
        return q

    def to_yaml(self, context: Context = None) -> dict:
        q = {}
        if self.type:
            q['type'] = self.type
        if self.type in ('cat', 'bagcat'):
            q['cost'] = self.cost
            q['theme'] = self.theme
        if self.type == 'bagcat':
            q['self'] = self.to_self
            q['knows'] = self.knows
        scenario = []
        for s in self.scenario:
            res = {}
            if s.time is not None:
                res['time'] = s.time
            res[s.type] = s.value
            scenario.append(res)
        if len(scenario) == 1:
            q.update(scenario[0])
        else:
            q['scenario'] = scenario
        for i, a in enumerate(self.right):
            k = 'answer' if i == 0 else f'answer{i+1}'
            q[k] = a
        for i, a in enumerate(self.wrong):
            k = 'wrong' if i == 0 else f'wrong{i+1}'
            q[k] = a
        return q


def resolve_path(typ, name: str, context: Context = None) -> str:
    base = '.' if not context else context.base_path
    if os.path.exists(os.path.join(base, name)):
        return name
    p = os.path.join(base, 'media', name)
    if os.path.exists(p):
        return p
    dirname = DIRNAMES.get(typ)
    if not dirname:
        return None
    p = os.path.join(base, dirname, name)
    if os.path.exists(p):
        return p
    p = os.path.join(base, 'media', dirname, name)
    if os.path.exists(p):
        return p
    p = os.path.join(base, dirname.lower(), name)
    if os.path.exists(p):
        return p
    return None
