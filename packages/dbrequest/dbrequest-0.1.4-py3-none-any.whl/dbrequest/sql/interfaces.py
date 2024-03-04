from typing import Tuple, Any


class ISQLRequest:
    def setArgs(self, *kwargs) -> None:
        raise NotImplementedError()

    def getRequest(self) -> Tuple[str, Tuple[Any]]:
        raise NotImplementedError()

