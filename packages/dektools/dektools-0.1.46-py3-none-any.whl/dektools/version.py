import re

version_pattern = '[0-9]+.[0-9]+.[0-9]+'


def version_to_tuple(version):
    rs = re.search(version_pattern, version)
    if rs:
        return tuple(int(x) for x in rs.group().split('.'))


def version_is_digits(version):
    return bool(re.search(version_pattern, version))


def version_digits(version):
    return re.search(version_pattern, version).group()


def version_is_release(version):
    rs = re.search(version_pattern, version)
    if rs:
        last = rs.span()[-1]
        return not version[last:]
    return False


def version_sorted(versions, reverse=False):
    keys = {x: version_to_tuple(x) for x in versions}
    return sorted(keys, key=lambda x: keys[x], reverse=reverse)
