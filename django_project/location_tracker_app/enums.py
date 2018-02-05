import inspect
from enum import Enum


class UserRoles(Enum):
    Admin = 0
    Employee = 1

    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        choices = tuple([(int(p[1].value), p[0]) for p in props if p[0] not in ['name', 'value']])
        return choices
