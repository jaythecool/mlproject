import dill
import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

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

def evaluate_model(x_train,x_test,y_train,y_test,models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)


            #model.fit(x_train,y_train)

            y_pred_train = model.predict(x_train)
            y_pred_test = model.predict(x_test)

            train_model_score = r2_score(y_train,y_pred_train)
            test_model_score = r2_score(y_test,y_pred_test)

            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e,sys)
