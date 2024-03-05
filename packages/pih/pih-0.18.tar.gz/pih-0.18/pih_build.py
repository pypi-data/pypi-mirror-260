import ipih

from pih import A
from pih.tools import js
from build_tools import build

NAME: str = A.NAME

def build_main() -> None:
    build(NAME, js((NAME.upper(), "package")), A.V.value, ["consts", "tools", "collections", "rpc"])


if __name__ == "__main__":
    build_main()