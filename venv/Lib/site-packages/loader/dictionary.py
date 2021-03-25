def unpack(d, *keys):
    if len(keys) == 1:
        k = keys[0]
        return d.get(k) if isinstance(k, str) else d.get(k[0], k[1])
    return tuple(d.get(k) if isinstance(k, str) else d.get(k[0], k[1]) for k in keys)


def extract(d, *keys):
    elems = []
    for key in keys:
        if key in d.keys():
            elems.append(d[key])
            del d[key]
        else:
            elems.append(None)
    return tuple(elem for elem in elems)


if __name__ == '__main__':
    c = {
        'a': 11,
    }
    a, b = unpack(c, 'a', ('b', 33))
    print(a, b)
    m = unpack(c, ('a', 55))
    print(m)
    print('>' * 20)

    d = {
        'e': 12,
        'f': 13,
        'g': 14
    }
    e, f = extract(d, 'e', 'a')
    print(d)
    print(f)
