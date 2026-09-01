import os
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src import config
from src.exception import customException
from src.logger import logging

# Transformation Imports
from src.components.data_transform import DataTransformationConfig
from src.components.data_transform import DataTransformation


# Use - Gives required paths to DataIngestion Class
@dataclass
class DataIngestionConfig:
    train_data_path : str=os.path.join("artifacts", "train.csv")
    test_data_path : str=os.path.join("artifacts", "test.csv")
    raw_data_path : str=os.path.join("artifacts", "raw.csv")

# Create Train , Test , Split File out of Given Dataset
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered Data Ingestion")

        try:
            df = pd.read_csv(os.path.join("dataset", "stud.csv"))
            logging.info("Read Dataset")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size = config.TEST_SIZE, random_state = config.RANDOM_STATE)
            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Ingestion of the data is Completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise customException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
