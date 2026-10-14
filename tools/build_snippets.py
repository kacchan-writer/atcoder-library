"""Generate static VS Code snippets from an immutable, committed source revision."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/kacchan-writer/atcoder-library'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def extract(source):
    tree = ast.parse(source)
    mains = [node for node in tree.body if isinstance(node, ast.If)
             and ast.dump(node.test) == ast.dump(ast.parse('__name__ == "__main__"', mode='eval').body)]
    if len(mains) != 1 or tree.body[-1] is not mains[0]:
        raise ValueError('Expected exactly one final __main__ demonstration')
    return '\n'.join(source.splitlines()[:mains[0].lineno - 1]).rstrip()

def escape(line):
    return line.replace('\\', '\\\\').replace('$', '\\$').replace('}', '\\}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref', required=True, help='Already committed code revision')
    args = parser.parse_args()
    sha = git('rev-parse', '--verify', args.ref + '^{commit}').decode().strip()
    assert re.fullmatch('[0-9a-f]{40}', sha)
    catalog_bytes = git('show', sha + ':catalog.json')
    assert catalog_bytes == (ROOT / 'catalog.json').read_bytes(), 'Commit catalog changes first'
    provenance = git('show', sha + ':PROVENANCE.md')
    assert provenance == (ROOT / 'PROVENANCE.md').read_bytes(), 'Commit provenance changes first'
    items = json.loads(catalog_bytes)['algorithms']
    snippets, manifest = {}, []
    prefixes = set()
    for item in items:
        source_bytes = git('show', sha + ':' + item['path'])
        assert source_bytes == (ROOT / item['path']).read_bytes(), 'Commit source changes first: ' + item['path']
        code = extract(source_bytes.decode('utf-8'))
        url = REPO + '/blob/' + sha + '/' + item['path']
        prefix = item['prefix']
        assert prefix not in prefixes
        prefixes.add(prefix)
        snippets[item['id']] = {
            'scope': 'python', 'prefix': prefix,
            'description': item['title'] + ' | ' + item['caution'],
            'body': [escape('# Source: ' + url),
                     escape('# Provenance: ' + REPO + '/blob/' + sha + '/PROVENANCE.md'),
                     *map(escape, code.splitlines()), '', '$0'],
        }
        manifest.append({'id': item['id'], 'prefix': prefix, 'path': item['path'], 'source_url': url,
            'source_sha256': hashlib.sha256(source_bytes).hexdigest()})
    directory = ROOT / 'snippets'
    directory.mkdir(exist_ok=True)
    for name, data in [('atcoder-python.code-snippets', snippets),
                       ('manifest.json', {'repository': REPO, 'source_commit': sha, 'algorithms': manifest})]:
        (directory / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'snippets': len(snippets), 'source_commit': sha}))

if __name__ == '__main__':
    main()
