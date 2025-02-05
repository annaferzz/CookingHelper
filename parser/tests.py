import unittest
from unittest.mock import patch, MagicMock
from .utils import get_soup, get_recipe_urls_from_page, get_recipe_from_page, get_pages_range, save_to_csv
import csv
import os


class ParserUtilsTest(unittest.TestCase):

    @patch('requests.get')
    def test_get_soup(self, mock_get):
        """Тестирует функцию get_soup, проверяя, что она правильно парсит HTML"""
        mock_response = MagicMock()
        mock_response.text = '<html><body><div>Test</div></body></html>'
        mock_get.return_value = mock_response

        soup = get_soup('https://example.com')
        self.assertEqual(soup.find('div').text, 'Test')

    @patch('requests.get')
    def test_get_recipe_urls_from_page(self, mock_get):
        """Проверка извлечение URL-ов рецептов с веб-страницы"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <div class="content-md">
                    <article class="item-bl">
                        <h2><a href="/recipe/1">Recipe 1</a></h2>
                    </article>
                    <article class="item-bl">
                        <h2><a href="/recipe/2">Recipe 2</a></h2>
                    </article>
                </div>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        urls = get_recipe_urls_from_page('https://example.com')
        self.assertEqual(urls, ['/recipe/1', '/recipe/2'])

    @patch('requests.get')
    def test_get_recipe_from_page(self, mock_get):
        """Проверка извлечения данных рецепта с веб-страницы"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <h1>Test Recipe</h1>
                <div class="ingredients-bl">
                    <li><a>Ingredient 1</a><span>100 г</span></li>
                    <li><a>Ingredient 2</a><span>200 мл</span></li>
                </div>
                <div class="article-text">Test Description</div>
                <ul itemprop="recipeInstructions">
                    <li>Step 1</li>
                    <li>Step 2</li>
                </ul>
                <img itemprop="image" src="http://example.com/image.jpg">
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        recipe = get_recipe_from_page('https://example.com')
        self.assertEqual(recipe['name'], 'Test Recipe')
        self.assertEqual(recipe['ingredients'], {'Ingredient 1': '100 г', 'Ingredient 2': '200 мл'})
        self.assertEqual(recipe['description'], 'Test Description')
        self.assertEqual(recipe['instruction'], 'Step 1\nStep 2')
        self.assertEqual(recipe['image_url'], 'https://example.com/image.jpg')

    @patch('requests.get')
    def test_get_recipe_from_page_not_found(self, mock_get):
        """Обработка ошибки страницы с отсутствующим рецептом"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <h1>Страница не найдена</h1>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        recipe = get_recipe_from_page('https://example.com')
        self.assertEqual(recipe['name'], 'Страница не найдена')
        self.assertEqual(recipe['ingredients'], {})
        self.assertEqual(recipe['description'], '')
        self.assertEqual(recipe['instruction'], '')
        self.assertEqual(recipe['image_url'], '')

    @patch('requests.get')
    def test_get_pages_range(self, mock_get):
        """Тестирует получение диапазона страниц для парсинга"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <div class="bl-right">
                    <strong>150</strong>
                </div>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        pages = get_pages_range(max_pages=5)
        self.assertEqual(len(pages), 5)
        self.assertEqual(pages[0], 'https://www.povarenok.ru/recipes/~1/')

    def test_save_to_csv(self):
        """Проверка сохранения данных рецептов в CSV файл"""
        data = [
            {
                'name': 'Test Recipe',
                'url': 'https://example.com',
                'ingredients': {'Ingredient 1': '100 г', 'Ingredient 2': '200 мл'},
                'description': 'Test Description',
                'instruction': 'Step 1\nStep 2',
                'image_url': 'https://example.com/image.jpg'
            }
        ]

        file_path = 'test_recipes.csv'
        save_to_csv(data, file_path)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[0], ['Name', 'URL', 'Ingredients', 'Description', 'Instruction', 'Image URL'])
            self.assertEqual(rows[1], [
                'Test Recipe',
                'https://example.com',
                'Ingredient 1: 100 г; Ingredient 2: 200 мл',
                'Test Description',
                'Step 1\nStep 2',
                'https://example.com/image.jpg'
            ])

        os.remove(file_path)

    def test_save_to_csv_empty_data(self):
        """Тестирует сохранение пустого списка данных в CSV файл"""
        data = []
        file_path = 'test_recipes.csv'
        save_to_csv(data, file_path)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[0], ['Name', 'URL', 'Ingredients', 'Description', 'Instruction', 'Image URL'])
            self.assertEqual(len(rows), 1)

        os.remove(file_path)

    def test_save_to_csv_invalid_data(self):
        """Тестирует сохранение данных с ошибками в CSV файл"""
        data = [
            {
                'name': '',
                'url': 'https://example.com',
                'ingredients': {},
                'description': 'Test Description',
                'instruction': 'Step 1\nStep 2',
                'image_url': 'https://example.com/image.jpg'
            }
        ]

        file_path = 'test_recipes.csv'
        save_to_csv(data, file_path)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[0], ['Name', 'URL', 'Ingredients', 'Description', 'Instruction', 'Image URL'])
            self.assertEqual(len(rows), 1)
        os.remove(file_path)
