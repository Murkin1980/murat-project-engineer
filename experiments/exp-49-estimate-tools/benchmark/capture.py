"""Validate an adapter's event log and preserve exact model text bytes offline."""
import argparse
import base64
import hashlib
import json
import pathlib

def digest(data):
    return hashlib.sha256(data).hexdigest()

def capture(path):
    record = json.loads(path.read_text())
    required = ('session','message','scenario','arm','client','client_version','model',
                'locale','region','clock_id','started_utc','contract_hash','control_hash')
    if any(not isinstance(record.get(k), str) or not record[k].strip() for k in required):
        raise ValueError('Incomplete provenance')
    events = record['events']
    kinds = [e['kind'] for e in events]
    if kinds[:1] != ['send'] or kinds[-1:] != ['complete'] or set(kinds[1:-1]) != {'text'}:
        raise ValueError('Expected send, ordered model-text chunks, complete')
    times = [e['monotonic_ns'] for e in events]
    if any(type(t) is not int or t < 0 for t in times) or times != sorted(times):
        raise ValueError('Invalid monotonic timestamps')
    request = base64.b64decode(events[0]['data'], validate=True)
    if digest(request) != record['expected_request_sha256']:
        raise ValueError('Sent prompt differs from frozen request')
    raw = b''.join(base64.b64decode(e['data'], validate=True) for e in events[1:-1])
    raw.decode('utf-8')
    return dict(bytes_in=len(request), bytes_out=len(raw), request_sha256=digest(request),
                response_sha256=digest(raw), elapsed_ns=times[-1]-times[0],
                source_log_sha256=digest(path.read_bytes()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event_log', type=pathlib.Path)
    print(json.dumps(capture(parser.parse_args().event_log)))
