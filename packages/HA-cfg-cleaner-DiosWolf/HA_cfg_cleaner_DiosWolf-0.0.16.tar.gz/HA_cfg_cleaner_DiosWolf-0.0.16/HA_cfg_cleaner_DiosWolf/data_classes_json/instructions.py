from dataclasses import dataclass


# TODO: for instructions file
@dataclass
class BasePath:
    path: str


@dataclass
class BaseIntegrationsIds:
    integrations_ids: list[str]


@dataclass
class DeleteObjects(BasePath):
    objects_names: list[str]


@dataclass
class DeleteInConfig(BaseIntegrationsIds):
    config_id: str


@dataclass
class DeleteScript(BasePath):
    scripts_ids: list[str]


@dataclass
class DeleteObjects(BasePath):
    objects_names: list[str]


@dataclass
class CleanFolders(BasePath):
    folders_names: list[str]


@dataclass
class CleanFiles(BasePath):
    files_names: list[str]


@dataclass
class ChangeFiles(BasePath):
    new_content: list


@dataclass
class FindInFiles:
    report_path: str
    text_to_find: list[str]


@dataclass
class Instructions:
    delete_in_config: list[DeleteInConfig]
    delete_integrations: BaseIntegrationsIds
    enable_integration: BaseIntegrationsIds
    disable_integration: BaseIntegrationsIds
    delete_automations: BaseIntegrationsIds
    delete_objects: list[DeleteObjects]
    delete_script: list[DeleteScript]
    clean_folders: list[CleanFolders]
    clean_files: list[CleanFiles]
    change_files: list[ChangeFiles]
    find_in_all_files: FindInFiles

    # def get_keys(self):
    #     keys = []
    #     for key in fields(Instructions):
    #         keys.append(key.name)
    #     return keys
