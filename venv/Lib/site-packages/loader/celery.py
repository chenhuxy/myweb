from .function import load as fload

try:
    from celery import chain, chord, group
except Exception as e:
    raise Exception('celery import failed')

def group_chains(payload):
    info = payload.get('info', {})
    callback = info.get('callback')
    callbacks = info.get('callbacks', [])
    data = payload.get('data', [])
    cts = []
    for i, d in enumerate(data):
        ops = []
        ids = d.get('ids')
        for i, tid in enumerate(ids):
            if i == 0:
                args = d.get('args')
                ops.append(fload(tid).s(**args))
            else:
                ops.append(fload(tid).s())
        if len(callbacks) > i:
            cb = callbacks[i]
            if cb:
                cts.append(chain(ops) | fload(cb).s())
            else:
                cts.append(chain(ops))
        else:
            cts.append(chain(ops))
    if callback:
        return group(cts) | fload(callback).s()
    return group(cts)


def chain_groups(payload):
    info = payload.get('info', {})
    data = payload.get('data', [])

    callbacks = info.get('callbacks', [])
    callback = info.get('callback')
    cts = []
    for i, d in enumerate(data):
        ops = []
        for dd in d:
            tid = dd.get('id')
            args = dd.get('args')
            ops.append(fload(tid).s(**args))
        if len(callbacks) > i:
            cb = callbacks[i]
            if cb:
                cts.append(group(ops) | fload(cb).s())
            else:
                cts.append(group(ops))
        else:
            cts.append(group(ops))
    if callback:
        return group(cts) | fload(callback).s()
    return chain(cts)
