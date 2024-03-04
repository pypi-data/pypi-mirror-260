from __future__ import annotations
from typing import SupportsInt
from semver4.baseversion import BaseVersion
from semver4.errors import FixPartNotSupported


__version__ = '0.0.1-beta.5'


class Version4(BaseVersion):

    # _valid_version_regex = '^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    _valid_base_version_regex = '(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?'

    def _build_version(self, **parts):
        ma, mi, pa, fx, pre, bl = parts['major'], parts['minor'], parts['patch'], parts['fix'], parts['prerelease'], parts['build']
        return f'{ma}.{mi}.{pa}{f".{fx}" if fx else ""}{f"-{pre}" if pre else ""}{f"+{bl}" if bl else ""}'


class SemVersion(BaseVersion):

    # _valid_version_regex = '^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    _valid_base_version_regex = '(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'

    def __init__(
            self,
            version: str | BaseVersion = None,
            major: str | SupportsInt = None,
            minor: str | SupportsInt = None,
            patch: str | SupportsInt = None,
            prerelease: str | SupportsInt | None = None,
            build: str | SupportsInt | None = None
    ):
        super().__init__(version, major, minor, patch, None, prerelease, build)

    @property
    def fix(self) -> int:
        raise FixPartNotSupported('This class supports standard semantic version format 2.0')

    def _build_version(self, **parts):
        ma, mi, pa, pre, build = parts['major'], parts['minor'], parts['patch'], parts['prerelease'], parts['build']
        return f'{ma}.{mi}.{pa}{f"-{pre}" if pre else ""}{f"+{build}" if build else ""}'


Version = Version4
