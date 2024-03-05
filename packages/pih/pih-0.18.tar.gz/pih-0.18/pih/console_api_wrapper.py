from pih import A, PIH, OutputStub
from pih.tools import n, nl, ne, nn, e, j, js, jnl, one
from typing import Any

output_stub: OutputStub = OutputStub()


class Stub(PIH):
    def arg(self) -> Any | None:
        return self.session.arg()
    
    def __init__(self):
        self.is_force: bool = False

if not A.SE.is_mobile:
    self: Stub = Stub()
b = output_stub.b
i = output_stub.i


def execute(file_search_request: str) -> None:
    with A.ER.detect_interruption():
        A.R_F.execute(
            file_search_request,
            parameters={"self": self},
            stdout_redirect=False,
            catch_exceptions=True,
        )


def execute_file(
    use_authentification: bool, title: str | None, file_search_request: str
) -> None:
    A.O.init()
    if not use_authentification or A.SE.authenticate():
        A.O.clear_screen()
        A.O.pih_title()
        if ne(title):
            A.O.head1(title)  # type: ignore
        execute(file_search_request)
    A.SE.exit(0, "Выход")


def include(
    value: str, class_name: str | None = None, global_dict: dict[str, Any] | None = None
) -> Any | dict[str, Any] | None:
    dictionary: dict[str, Any] = A.R_F.execute(value, stdout_redirect=False)
    if n(class_name):
        return dictionary
    import_data: Any = dictionary[class_name]
    if n(global_dict):
        global_dict[class_name] = import_data
        return
    else:
        return import_data
