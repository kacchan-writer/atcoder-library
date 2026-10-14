"""Check standalone source and the exact expanded snippet text independently."""
import argparse
import ast
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import time

import reference_checks as ref

ROOT = Path(__file__).resolve().parents[1]

def expand(body):
    assert body[-1] == '$0', 'Expected a final cursor tabstop'
    lines = []
    for line in body[:-1]:
        # Only literal snippets plus the final tabstop are allowed. Decode VS Code escapes.
        out, i = [], 0
        while i < len(line):
            ch = line[i]
            if ch == '\\':
                assert i + 1 < len(line) and line[i + 1] in '\\$}'
                i += 1
                ch = line[i]
            else:
                assert ch != '$', 'Unexpected snippet variable or placeholder'
            out.append(ch)
            i += 1
        lines.append(''.join(out))
    return '\n'.join(lines) + '\n'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snippets', action='store_true')
    args = parser.parse_args()
    started = time.perf_counter()
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))['algorithms']
    hashes = {}
    demo_count = 0
    if args.snippets:
        snippets = json.loads((ROOT / 'snippets/atcoder-python.code-snippets').read_text(encoding='utf-8'))
        manifest = json.loads((ROOT / 'snippets/manifest.json').read_text(encoding='utf-8'))
        sha = manifest['source_commit']
        assert re.fullmatch('[0-9a-f]{40}', sha)
        assert set(snippets) == {x['id'] for x in catalog}
        entries = {x['id']: x for x in manifest['algorithms']}
        assert len(entries) == len(catalog)
    for item in catalog:
        path = ROOT / item['path']
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        name = item['id']
        hashes[item['path']] = hashlib.sha256(path.read_bytes()).hexdigest()
        if args.snippets:
            snippet = snippets[name]
            assert snippet['scope'] == 'python' and snippet['prefix'] == item['prefix']
            entry = entries[name]
            expected_url = f"https://github.com/kacchan-writer/atcoder-library/blob/{sha}/{item['path']}"
            assert entry['source_url'] == expected_url
            assert entry['source_sha256'] == hashes[item['path']]
            # git archive downloads omit .git; compare against the pinned local object if available.
            if (ROOT / '.git').exists():
                committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', sha + ':' + item['path']])
                assert committed == path.read_bytes()
            expanded = expand(snippet['body'])
            assert expanded.splitlines()[0] == '# Source: ' + expected_url
            assert expanded.splitlines()[1] == f'# Provenance: https://github.com/kacchan-writer/atcoder-library/blob/{sha}/PROVENANCE.md'
            assert '# AI生成: OpenAI Codex' in expanded
            assert isinstance(tree.body[-1], ast.If)
            assert ast.dump(tree.body[-1].test) == ast.dump(ast.parse('__name__ == "__main__"', mode='eval').body)
            expected_ast = ast.Module(body=tree.body[:-1], type_ignores=[])
            assert ast.dump(ast.parse(expanded)) == ast.dump(expected_ast), name
            namespace = {'__name__': '__main__'}
            output = io.StringIO()
            with redirect_stdout(output):
                exec(compile(expanded, '<snippet ' + name + '>', 'exec'), namespace)
            assert output.getvalue() == '', 'Demo leaked into snippet'
            ref.MODULES[name] = namespace
        else:
            ref.MODULES[name] = runpy.run_path(str(path))
            run = subprocess.run([sys.executable, '-B', str(path)], capture_output=True,
                text=True, encoding='utf-8', timeout=15)
            assert run.returncode == 0, (name, run.stderr)
            assert run.stdout.strip() == item['expected'], (name, run.stdout)
            demo_count += 1
    for test in (ref.test_c, ref.test_d, ref.test_e, ref.test_f, ref.test_g, ref.test_advanced, ref.stress_structure):
        test()
        print(test.__name__ + ': PASS', flush=True)
    assert set(ref.CHECKS) == set(ref.MODULES)
    result = {'status': 'PASS', 'mode': 'snippets' if args.snippets else 'source', 'seed': 20261012,
        'algorithm_count': len(catalog), 'demo_count': demo_count,
        'independent_assertion_count': sum(ref.CHECKS.values()),
        'assertions_by_algorithm': dict(sorted(ref.CHECKS.items())),
        'source_sha256': hashes, 'seconds': round(time.perf_counter() - started, 3),
        'scope': 'Small independent references, edge cases, 2500-node structure checks. No AtCoder submission or maximum-constraint performance verification.'}
    output = ROOT / '.validation'
    output.mkdir(exist_ok=True)
    (output / (result['mode'] + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('assertions_by_algorithm', 'source_sha256')}))

if __name__ == '__main__':
    main()
