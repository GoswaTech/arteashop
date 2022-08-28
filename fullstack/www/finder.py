import os
from pathlib import Path

from django.templatetags.static import static
from django.conf import settings


class Finder:

    def __init__(self, **kwargs):
        #root_path = kwargs.pop('root_path', Path(__file__))
        root_path = kwargs.pop('root_path', os.path.dirname(__file__))
        productsdir = kwargs.pop('productsdir', 'products')

        self.root_path = self.__get_root_path(root_path)
        self.static_path = self.root_path+'/staticfiles' if not settings.DEBUG else self.root_path+'/www/static'

        self.products_path = self.static_path+'/{0}'.format(productsdir)


    def __get_root_path(self, path):
        # Test le type
        #path = path if (type(path) == type(Path('.'))) else Path(path)
        path = path if (type(path) == type(str())) else os.path.dirname(path)

        # Test la génération
        #path = path.parent.parent if (path == Path(__file__)) else path
        path = path+'/..' if (path == os.path.dirname(__file__)) else path

        return path


    def find_categories(self):
        products_path = self.products_path

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
            path = self.products_path + '/{0}/'.format(category)
            for root, article_dirs, files in os.walk(path):
                if len(article_dirs) > 0:
                    library[category.lower()] = self.find_article_infos(path, article_dirs, category)
                break

        return library

    def find_article_infos(self, path, article_dirs, category):

        article_infos = []

        for article_dir in article_dirs:

            infos = {
                'id': '{0}_{1}'.format(category, article_dir),
                'title': article_dir,
                'description': 'Hey U',
                'cover_image': {
                    'alt': 'Unsplash Random Image',
                    'src': 'https://source.unsplash.com/random/512x512/',
                },
                'images': [
                    {
                        'alt': 'Unsplash Sample Image 1',
                        'src': 'https://source.unsplash.com/4eWwSxaDhe4/512x512/',
                    },
                    {
                        'alt': 'Unsplash Sample Image 2',
                        'src': 'https://source.unsplash.com/hteGzeFuB7w/512x512/',
                    },
                    {
                        'alt': 'Unsplash Sample Image 3',
                        'src': 'https://source.unsplash.com/xdD-x2Y2SPI/512x512/',
                    },
                ],
                'article': article_dir.upper(),
            }

            # Walk In Directory
            article_path = '{0}{1}/'.format(path, article_dir)
            for root, info_dirs, info_files in os.walk(article_path):

                # Set ID
                if 'id.txt' in info_files:
                    id = open("{0}id.txt".format(article_path), "r")
                    infos['id'] = id.read()

                # Set Title
                if 'title.txt' in info_files:
                    title = open("{0}title.txt".format(article_path), "r")
                    infos['title'] = title.read()

                # Set Description
                if 'description.txt' in info_files:
                    description = open("{0}description.txt".format(article_path), "r")
                    infos['description'] = description.read()

                # Set Cover Image
                if 'cover_image.png' in info_files:
                    infos['cover_image'] = {
                        'alt': 'Cover Image {0}'.format(infos['title']),
                        'src': static("products/{0}/{1}/cover_image.png".format(category, article_dir)),
                    }

                if 'images' in info_dirs:
                    image_path = article_path+'images/'
                    for image_root, image_dirs, image_files in os.walk(image_path):
                        for image_file in image_files:
                            infos['images'].append({
                                'alt': 'Info Image {0} {1}'.format(infos['title'], image_file),
                                'src': static("products/{0}/{1}/images/{2}".format(category, article_dir, image_file)),
                            })
                        break

                break

            article_infos.append(infos)

        return article_infos
