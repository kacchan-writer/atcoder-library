"""Install project-scoped Python snippets, preserving any previous files as backups."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def backup(path):
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, path.with_name(path.name + '.backup-' + stamp))

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--workspace-file', type=Path, help='A JSON .code-workspace; use its first folder')
    group.add_argument('--folder', type=Path, help='A folder opened in VS Code')
    args = parser.parse_args()
    source = ROOT / 'snippets/atcoder-python.code-snippets'
    snippets = json.loads(source.read_text(encoding='utf-8'))
    assert snippets and all(item['scope'] == 'python' for item in snippets.values())
    if args.workspace_file:
        config_path = args.workspace_file.resolve(strict=True)
        config = json.loads(config_path.read_text(encoding='utf-8-sig'))
        folder = (config_path.parent / config['folders'][0]['path']).resolve(strict=True)
        settings = config.setdefault('settings', {})
        config_changed = settings.get('editor.tabCompletion') != 'onlySnippets'
        settings['editor.tabCompletion'] = 'onlySnippets'
    else:
        folder = args.folder.resolve(strict=True)
    assert folder.is_dir()
    destination = folder / '.vscode/atcoder-python.code-snippets'
    destination.parent.mkdir(exist_ok=True)
    if not destination.exists() or destination.read_bytes() != source.read_bytes():
        backup(destination)
        shutil.copy2(source, destination)
    if args.workspace_file and config_changed:
        backup(config_path)
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=4) + '\n', encoding='utf-8', newline='\n')
    assert destination.read_bytes() == source.read_bytes()
    print(json.dumps({'installed_snippets': len(snippets), 'path': str(destination),
        'tab_completion': 'onlySnippets' if args.workspace_file else 'Use Ctrl+Space or configure editor.tabCompletion'}, ensure_ascii=True))

if __name__ == '__main__':
    main()
