import sys
from src.logger import logging

def error_message_detail(err,err_detail:sys):
    _,_,exc_tb = err_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    err_msg = "Code fat gya bhai, yaha dekh [{0}],line number [{1}], error message [{2}]".format(file_name,exc_tb.tb_lineno,str(err))
    return err_msg

class CustomException(Exception):
    def __init__(self,err,err_detail:sys):
        super().__init__(err)
        self.err = error_message_detail(err,err_detail=err_detail)

    def __str__(self):
        return self.err 

if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Division by 0")
        raise CustomException(e,sys)