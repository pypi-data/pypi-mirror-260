import os
from ctypes import c_char_p, CDLL


class EditSharedComment:
    def __init__(self, file_path):
        self.file_path = file_path
        self._lib = CDLL(os.path.join(os.path.dirname(__file__), 'dll', 'DrCinCo.dll'))

    def update_multiple_cells(self, operation_details):
        self._lib.UpdateMultipleExcelCells(c_char_p(self.file_path.encode('utf-8')),
                                           c_char_p(operation_details.encode('utf-8')))
