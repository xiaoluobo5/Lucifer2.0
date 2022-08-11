import os
import sys
from PyQt5.QtWidgets import QApplication, QTextBrowser


class MyTextBrowser(QTextBrowser):  # 1
    def __init__(self, parent):
        super(MyTextBrowser, self).__init__(parent)
        self.setAcceptDrops(True)  # 2
        self.filepath = ""
        self.fileName = ""

    def dragEnterEvent(self, QDragEnterEvent):  # 3
        print('Drag Enter')
        if QDragEnterEvent.mimeData().hasText():
            QDragEnterEvent.acceptProposedAction()

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        # print('Drag Move')
        pass

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        # print('Drag Leave')
        pass

    def dropEvent(self, QDropEvent):  # 6
        print('Drag Drop')
        # MacOS
        self.filepath = QDropEvent.mimeData().text().replace('file:///', '/')
        # Linux
        # txt_path = QDropEvent.mimeData().text().replace('file:///', '/').strip()
        # Windows
        # txt_path = QDropEvent.mimeData().text().replace('file:///', '')
        # self.setText(self.filepath)
        fileName = os.path.basename(self.filepath)
        if fileName:
            # fileType = os.path.splitext
            if fileName.endswith(".tgz"):
                self.append("Input \"{}\"".format(fileName))

                self.fileName = fileName
            elif fileName.endswith(".json") and fileName.lower() == "io_map.json":
                self.fileName = fileName
                self.append("Input \"io_map.json\"")
            else:
                self.append("<font color='red'> invalid file!!! <font>")
        else:
            self.append("<font color='red'>\"{}\" is a directory, not a file<font>".format(self.filepath))
        # with open(txt_path, 'r') as f:
        #     self.setText(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MyTextBrowser()
    demo.show()
    sys.exit(app.exec_())
