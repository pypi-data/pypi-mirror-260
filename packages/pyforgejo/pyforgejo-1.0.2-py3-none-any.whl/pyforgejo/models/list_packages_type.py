from enum import Enum


class ListPackagesType(str, Enum):
    ALPINE = "alpine"
    CARGO = "cargo"
    CHEF = "chef"
    COMPOSER = "composer"
    CONAN = "conan"
    CONDA = "conda"
    CONTAINER = "container"
    CRAN = "cran"
    DEBIAN = "debian"
    GENERIC = "generic"
    GO = "go"
    HELM = "helm"
    MAVEN = "maven"
    NPM = "npm"
    NUGET = "nuget"
    PUB = "pub"
    PYPI = "pypi"
    RPM = "rpm"
    RUBYGEMS = "rubygems"
    SWIFT = "swift"
    VAGRANT = "vagrant"

    def __str__(self) -> str:
        return str(self.value)
