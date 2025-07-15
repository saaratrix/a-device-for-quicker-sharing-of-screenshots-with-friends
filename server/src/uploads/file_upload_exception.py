class FileUploadException(Exception):
    def __init__(self, message, upload_error):
        super().__init__(message)
        self.upload_error = upload_error

