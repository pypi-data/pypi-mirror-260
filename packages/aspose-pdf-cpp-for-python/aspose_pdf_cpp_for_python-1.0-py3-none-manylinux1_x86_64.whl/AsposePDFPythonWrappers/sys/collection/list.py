import AsposePDFPython
import AsposePDFPythonWrappers.layer
import AsposePDFPythonWrappers.artifact

class List:
    '''List Container.'''

    def __init__(self, handle: AsposePDFPython.sys_collection_list_handle):
        self.handle = handle

    def __del__(self):
        '''Close handle.'''
        AsposePDFPython.close_handle(self.handle)

    def count(self):
        '''Gets number of elements in current list.'''
        return AsposePDFPython.sys_collection_list_get_count(self.handle)

    def clear(self):
        '''Deletes all elements.'''
        AsposePDFPython.sys_collection_list_clear(self.handle)

    def add(self, element):
        '''Adds element to the end of list.'''

        ":param item: Item to add."
        AsposePDFPython.sys_collection_list_add(self.handle, element.handle)

    def __getitem__(self, index: int) -> any:
        '''Copy of element at specified position.'''
        hndl_obj = AsposePDFPython.sys_collection_list_idx_get(self.handle, index)
        hash_obj = AsposePDFPython.hash_object(hndl_obj)
        match hash_obj:
            case 6647949587257241386:
                return AsposePDFPythonWrappers.layer.Layer(hndl_obj)
            case 6509845516712748887:
                return AsposePDFPythonWrappers.artifact.Artifact(hndl_obj)

            case _:
                return None

