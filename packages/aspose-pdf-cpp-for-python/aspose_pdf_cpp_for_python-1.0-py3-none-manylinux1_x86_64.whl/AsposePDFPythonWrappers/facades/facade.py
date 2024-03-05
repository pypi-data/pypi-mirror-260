import AsposePDFPython
import AsposePDFPythonWrappers


class Facade:
    '''Base facade class.'''

    def __init__(self, handle: AsposePDFPython.facades_facade_handle):
        self.handle = handle

    def __del__(self):
        '''Close handle.'''
        AsposePDFPython.close_handle(self.handle)

    def bind_pdf(self, src_file: str) -> None:
        '''Initializes the facade.
        :param src_file: The PDF file.'''
        AsposePDFPython.facades_facade_bind_pdf(self.handle, src_file)
