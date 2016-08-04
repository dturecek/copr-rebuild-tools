import json
from helpers import is_greater


class Entity(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Implemented in particular backends
    name = NotImplemented
    pkgname = NotImplemented
    version = NotImplemented


class Backend(object):
    def get_all(self):
        """
        Implemented in particular backends
        """
        raise NotImplementedError


class Query(object):
    def __init__(self, objects):
        self.objects = objects

    def limit(self, n):
        return Query(self.objects[:n])

    def offset(self, obj):
        try:
            i = self.objects.index(obj) + 1
            return Query(self.objects[i:])
        except ValueError:
            return Query(self.objects)

    def get(self):
        return self.objects

    def succeeded(self, packages):
        packages_set = set(p.name for p in packages)
        return Query([e for e in self.get() if e.pkgname in packages_set])

    def unsucessful(self, packages):
        return Query(list(set(self.get()) - set(self.succeeded(packages).get())))

    def newer(self, packages, name_key):
        """
        :param packages: dict {pkg_name: version, ...}
        :return:
        """
        rebuild = []
        for p in self.get():
            if p.pkgname not in packages or is_greater(p.version, packages[p.pkgname]):
                rebuild.append(p)
        return Query(rebuild)

    def values(self, allowed, key):
        return Query([e for e in self.get() if getattr(e, key) in allowed])
