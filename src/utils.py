# import os
# import sys
# import numpy as np
# import pandas as pd
# import dill
# from src.exception import CustomException
# from src.logger import logging

# def save_obj(file_path,obj):
#     try:
#         dir_path = os.path.dirname(file_path)
#         os.makedirs(dir_path,exist_ok=True)
        
#         with open(file_path,"wb") as file_obj:
#             dill.dump(obj,file_obj)

#         logging.info(f"Object saved successfully at {file_path}")
#     except Exception as e:
#         raise CustomException(e,sys)

import dill
import os
import sys
from src.logger import logging
from src.exception import CustomException

def save_obj(file_path, obj):
    try:
        logging.info(f"Creating directory for: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        logging.info(f"Saving object to {file_path}")
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Object saved successfully.")
    except Exception as e:
        logging.error(f"Error occurred while saving object: {e}")
        raise CustomException(e, sys)
