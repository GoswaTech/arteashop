import os
from pathlib import Path


class Finder:

    def __init__(self, **kwargs):
        #root_path = kwargs.pop('root_path', Path(__file__))
        root_path = kwargs.pop('root_path', os.path.dirname(__file__))

        self.root_path = self.__get_root_path(root_path)


    def __get_root_path(self, path):
        # Test le type
        #path = path if (type(path) == type(Path('.'))) else Path(path)
        path = path if (type(path) == type(str())) else os.path.dirname(path)

        # Test la génération
        #path = path.parent.parent if (path == Path(__file__)) else path
        path = path+'/..' if (path == os.path.dirname(__file__)) else path

        return path

    def find_categories(self):
        products_path = self.root_path+'/staticfiles/products'

        categories = os.listdir(products_path)

        def products_filter(entry):
            return os.path.isdir(products_path+'/'+entry)

        return list(filter(products_filter, categories))
