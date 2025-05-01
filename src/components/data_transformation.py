import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
from sklearn.pipeline import Pipeline
import os
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['math_score', 'reading_score', 'writing_score', 'average']
            categorical_columns = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            numerical_pipeline = Pipeline(
                steps = [
                    ("Imputer", SimpleImputer(strategy="median")),
                    ("stdsclr",StandardScaler())

                ]
            )

            # categorical_pipeline = Pipeline(
            #     steps=[
            #         ("Imputer",SimpleImputer(strategy="most_frequent")),
            #         ("OHE", OneHotEncoder()),
            #         ("stdsclr",StandardScaler(with_mean=False))
            #     ]
            # )

            categorical_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("OHE", OneHotEncoder(sparse_output=False, handle_unknown="ignore")),  # ✅ FORCE dense matrix
                    ("stdsclr", StandardScaler(with_mean=False))  # ✅ Okay now
                ]
            )

            logging.info(f"numerical colums : {numerical_columns}")
            logging.info(f"Categorical pipeline exceuted : {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline",numerical_pipeline,numerical_columns),
                    ("Categorical_pipeline",categorical_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test dataset completed")

            logging.info("obtaining preprocessing object")

            preprocessor_obj = self.get_data_transformer_object()

            target_column = "total score"
            
            
            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            input_feature_train_df = input_feature_train_df.drop(columns=['Unnamed: 0'], errors='ignore')
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info('Applying the preprocessor to the training and testing dataframes')

            logging.info(f"Columns in input_feature_train_df: {input_feature_train_df.columns.tolist()}")


            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("Saving the preprocessing objects")

            save_obj(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )


            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        


