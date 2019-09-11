class FileParser():
    def __init__(self, filename):
        self.filename = filename
        self.file = filename.split('.')[0]
        self.extension = filename.split('.')[1]