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

        def categories_filter(entry):
            return os.path.isdir(products_path+'/'+entry)

        return list(filter(categories_filter, categories))

    def find_articles(self, **kwargs):
        category = kwargs.pop('category', None)


        if category == None:
            searched_categories = self.find_categories()
        else:
            searched_categories = [category]

        library = {}

        for category in searched_categories:
            path = self.root_path + '/staticfiles/products/{0}/'.format(category)
            for root, dirs, files in os.walk(path):
                if len(dirs) > 0:
                    library[category.lower()] = dirs
                break

        return library
