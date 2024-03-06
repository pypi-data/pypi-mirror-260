from requests import Response

from HA_cfg_cleaner_DiosWolf.data_classes_json.file_config import (
    Configuration,
    HostInfo,
)
from HA_cfg_cleaner_DiosWolf.ha_requests.ha_request import HARequests


class AutomationsEditor:
    def __init__(
        self, configuration: Configuration, full_cfg: dict, host_cfg: HostInfo = None
    ):
        self.configuration = configuration
        self.full_cfg = full_cfg

        if host_cfg:
            self.ha_request = HARequests(host_cfg)

    def __get_editable_cfg(self) -> dict:
        if self.configuration.first_key is None:
            return self.full_cfg

        elif self.configuration.second_key is None:
            return self.full_cfg[self.configuration.first_key]

        else:
            return self.full_cfg[self.configuration.first_key][
                self.configuration.second_key
            ]

    def __set_editable_cfg(self, edit_cfg_part: list[dict]) -> list[dict] | dict:

        if self.configuration.first_key is None:
            self.full_cfg = edit_cfg_part

        elif self.configuration.second_key is None:
            self.full_cfg: dict
            self.full_cfg[self.configuration.first_key] = edit_cfg_part

        else:
            self.full_cfg: dict
            self.full_cfg[self.configuration.first_key][
                self.configuration.second_key
            ] = edit_cfg_part

        return self.full_cfg

    def __get_entities_ids(self, automations_ids: list[str]) -> list[str]:
        entities_list = self.__get_editable_cfg()
        automations_entities_ids = []

        for entity in entities_list:
            if entity[self.configuration.id_key] in automations_ids:
                automations_entities_ids.append(entity[self.configuration.on_off_field])

        return automations_entities_ids

    def delete_automation(self, integrations_list: list[str]) -> list[dict]:
        editable_part = self.__get_editable_cfg()
        new_cfg_list = []

        for config_dict in editable_part:

            if config_dict[self.configuration.id_key] not in integrations_list:
                new_cfg_list.append(config_dict)

        return self.__set_editable_cfg(new_cfg_list)

    def disable_automation(self, automations_ids: list[str]) -> Response:
        automations_entities_ids = self.__get_entities_ids(automations_ids)

        if automations_entities_ids:
            data = {self.configuration.on_off_field: automations_entities_ids}
            return self.ha_request.post_requests(data)
