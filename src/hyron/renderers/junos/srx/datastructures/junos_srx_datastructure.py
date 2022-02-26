from typing import Any, List, Protocol, Text


class JunosSrxDatastructure(Protocol):
    def get_json_config_element(self) -> Any:
        raise NotImplementedError

    def get_set_commands(self) -> List[Text]:
        raise NotImplementedError
