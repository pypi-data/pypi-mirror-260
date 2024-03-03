from Excel_modify.edit_excel import EditExcel


class EditMainComment(EditExcel):
    def __init__(self, file_path, cell_comment):
        self._cell_comment = cell_comment
        super().__init__(file_path, r"xl/comments1.xml")

    def _get_value(self, cell):
        cell_number = "".join([x for x in str(cell) if x.isnumeric()])
        comments = self._path_content.find_all('comment')
        for comment in comments:
            ref = comment['ref']
            if ref == self._cell_comment + cell_number:
                return comment.find('t')

    def set_comment_change(self, cell: str | int, value):
        old = self._get_value(cell)
        if old:
            old.string = value
