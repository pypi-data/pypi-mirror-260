from HA_cfg_cleaner_DiosWolf.files_editors.fileIO_cls import FileIO


class ScriptsEditor:
    def __init__(self, original_file: dict[str, any]):
        self.edit_file = None
        self.file_editor = FileIO()
        self.original_file = original_file

    def change_file(self, new_file_part: dict[any]) -> dict:
        if isinstance(self.original_file, dict):
            self.original_file = self.original_file | new_file_part

            return self.original_file

    def delete_scripts(self, script_id: str) -> dict:
        self.edit_file = self.original_file
        if isinstance(self.original_file, dict):
            del self.edit_file[script_id]
        return self.edit_file
