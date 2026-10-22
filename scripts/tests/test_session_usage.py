"""Session usage parsing on synthetic logs only."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('session_usage', Path(__file__).resolve().parents[1] / 'session_usage.py')
usage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(usage)


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(json.dumps(r) for r in rows) + '\n', encoding='utf-8')


def codex_tokens(context, cached, output=10):
    return {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'last_token_usage': {
        'input_tokens': context, 'cached_input_tokens': cached, 'output_tokens': output}}}}


def codex_user(text):
    return {'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}]}}


class SessionUsageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.codex = self.root / 'codex'
        self.claude = self.root / 'claude'

    def test_codex_turns_requests_and_secret_text_not_reported(self):
        write(self.codex / '2026' / '10' / '18' / 'rollout-2026-10-18T00-53-36-x.jsonl', [
            {'type': 'session_meta', 'payload': {'cwd': 'C:\\Nature Studio'}},
            {'type': 'turn_context', 'payload': {'model': 'm1'}},
            codex_user('<environment_context>ignored</environment_context>'),
            codex_user('/na-chayvideo secret brief'),
            {'type': 'response_item', 'payload': {'type': 'function_call', 'arguments': '{}'}},
            codex_tokens(100, 90), codex_tokens(150, 140),
            codex_user('sửa lần 1'), {'type': 'compacted', 'payload': {}}, codex_tokens(300, 0),
        ])
        [row] = [usage.summarize(s, True) for s in usage.collect(self.codex, self.claude)]
        self.assertEqual((row['turns'], row['requests'], row['tool_calls']), (2, 3, 1))
        self.assertEqual((row['input'], row['cached'], row['peak_context'], row['compactions']), (550, 230, 300, 1))
        self.assertEqual(row['per_turn'][0]['context_start'], 100)
        self.assertNotIn('secret', json.dumps(row))

    def test_claude_dedupes_request_blocks_and_filters_cwd(self):
        assistant = {'type': 'assistant', 'requestId': 'r1', 'message': {'model': 'c1', 'usage': {
            'input_tokens': 5, 'cache_read_input_tokens': 80, 'cache_creation_input_tokens': 15, 'output_tokens': 7},
            'content': [{'type': 'tool_use'}]}}
        write(self.claude / 'proj' / 'a.jsonl', [
            {'type': 'user', 'cwd': 'C:\\Nature Studio', 'message': {'content': 'audit'}},
            assistant, assistant,
            {'type': 'user', 'message': {'content': [{'type': 'tool_result'}]}},
        ])
        write(self.claude / 'other' / 'b.jsonl', [{'type': 'user', 'cwd': 'C:\\Elsewhere', 'message': {'content': 'x'}}, assistant])
        rows = [usage.summarize(s) for s in usage.collect(self.codex, self.claude)]
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]['requests'], rows[0]['input'], rows[0]['cached'], rows[0]['tool_calls']), (1, 100, 80, 2))


if __name__ == '__main__':
    unittest.main()
