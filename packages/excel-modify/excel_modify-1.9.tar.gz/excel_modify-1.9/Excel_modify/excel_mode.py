from Excel_modify.edit_main_comment import EditMainComment
from Excel_modify.edit_share_comment import EditSharedComment


class ExcelMode:
    def __init__(self, file_path, cell_comment):
        self.file_path = file_path
        self._main_comment = EditMainComment(file_path, cell_comment)
        self._shared_comment = EditSharedComment(file_path)
        self._cell_comment = cell_comment
        self._temp = ""

    def set_comment(self, cell, value):
        cell_number = "".join([x for x in str(cell) if x.isnumeric()])
        self._main_comment.set_comment_change(cell, value)
        self._temp += f"E{cell_number}:{value}|"

    def save(self):
        self._temp = self._temp.strip("|")
        self._shared_comment.update_multiple_cells(self._temp)
        self._main_comment.save()
