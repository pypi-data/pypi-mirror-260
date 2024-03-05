from HA_cfg_cleaner_DiosWolf.parse_classes.arguments_parse import ConsoleArguments
from HA_cfg_cleaner_DiosWolf.files_editors.fileIO_cls import FileIO
from HA_cfg_cleaner_DiosWolf.data_classes_json.file_config import ConfigurationFile
from HA_cfg_cleaner_DiosWolf.data_classes_json.instructions import Instructions
from HA_cfg_cleaner_DiosWolf.instruction_classes.instruction_executor import InstructionsExecute


class StartScript:
    def __init__(self):
        self.cls_args = ConsoleArguments()
        self.file_io = FileIO()
        self.all_instructions = self.file_io.json_read(
            self.cls_args.args.inst_path, Instructions)

        self.all_configs = self.file_io.json_read(
            self.cls_args.args.cfg_ha_path, ConfigurationFile)

        self.instruction_executor = InstructionsExecute(
            self.all_instructions, self.file_io, self.all_configs)

    def start(self):
        self.instruction_executor.del_in_cfg()
        self.instruction_executor.del_integrations()
        self.instruction_executor.enable_integrations()
        self.instruction_executor.disable_integrations()
        self.instruction_executor.del_automations()
        self.instruction_executor.del_automations_restore_state()
        self.instruction_executor.change_files()
        self.instruction_executor.del_script()
        self.instruction_executor.del_script_restore_state()
        self.instruction_executor.del_objects()
        self.instruction_executor.clean_folders()
        self.instruction_executor.clean_files()
        self.instruction_executor.searching_in_files()


def start_script():
    try:
        start = StartScript()
        start.start()
        print("Script finished. Press Enter to exit\n")
    except Exception as exp:
        print(exp)
        print("Error! Press Enter to exit\n")


# if __name__ == "__main__":
#     try:
#         start = StartScript()
#         start.start()
#         print("Script finished. Press Enter to exit\n")
#     except Exception as exp:
#         print(exp)
