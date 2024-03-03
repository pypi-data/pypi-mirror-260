import os.path
from pathlib import Path
import yaml
import logging

from powernovo.utils.utils import Singleton

CONFIG_FILE = "config.yaml"

logger = logging.getLogger("powernovo")


class ModelParams(object):
    pass


class PWNConfig(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self.working_folder = None
        self.models_folder = None
        self.preprocessing_folder = None
        self.assembler_folder = None
        self.output_folder_name = None
        self.temporary_folder = None
        self.figshare_id = None
        self.annotated = False
        self.n_workers = 0
        self.train_batch_size = 1
        self.inference_batch_size = 1
        self.device = 'auto'
        self.use_bert_inference = False

        config_path = Path(__file__).parent.resolve() / CONFIG_FILE
        try:
            with open(config_path, 'r') as fh:
                config_records = yaml.safe_load(fh)
        except FileNotFoundError as e:
            logger.error(f'Cant load pipeline_config file: {config_path}')
            raise e

        # environments
        for r in config_records['environments']:
            for k, v in r.items():
                self.__setattr__(k, v)

        try:
            assert self.working_folder is not None
            assert self.models_folder is not None
        except AssertionError as e:
            logger.error(f'Invalid pipeline_config records: {config_path}')
            raise e

        try:
            working_folder = kwargs['working_folder']
            self.working_folder = working_folder
            self.working_folder = Path(self.working_folder)
            self.working_folder.mkdir(exist_ok=True)
            logger.info(f'Current work folder is {self.working_folder}')
            self.models_folder = self.working_folder / self.models_folder
            self.models_folder.mkdir(exist_ok=True)
            self.assembler_folder = self.working_folder / self.assembler_folder
            self.assembler_folder.mkdir(exist_ok=True)
            self.temporary_folder = self.working_folder / self.temporary_folder
        except Exception as e:
            logger.error(f'Path not found: {e}')
            raise e

        for r in config_records['models']:
            for model in r:
                self.__setattr__(model, ModelParams())
                for params in r[model]:
                    m = self.__getattribute__(model)
                    for k, v in params.items():
                        m.__setattr__(k, v)

        for r in config_records['assignment']:
            for assignment in r:
                self.__setattr__(assignment, ModelParams())
                for params in r[assignment]:
                    m = self.__getattribute__(assignment)
                    for k, v in params.items():
                        m.__setattr__(k, v)

        for r in config_records['spectrum_model_train']:
            for k, v in r.items():
                self.__setattr__(k, v)


if __name__ == '__main__':
    config = PWNConfig()
