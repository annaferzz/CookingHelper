import bs4
import requests
import csv
import math


def get_soup(url):
    req = requests.get(url)
    return bs4.BeautifulSoup(req.text, 'lxml')


def get_recipe_urls_from_page(url, max_recipes=1000):
    soup = get_soup(url)
    content_div = soup.find('div', 'content-md')
    pages_url = [
        recipe_preview.find('h2').find('a')['href']
        for recipe_preview in content_div.find_all('article', 'item-bl')
    ]
    if max_recipes:
        pages_url = pages_url[:max_recipes]
    return pages_url


def get_recipe_from_page(url):
    soup = get_soup(url)
    recipe_name = soup.find('h1').get_text().strip()

    if recipe_name == 'Страница не найдена':
        return {'url': url, 'name': recipe_name, 'ingredients': {},
                'description': '', 'instruction': '', 'image_url': ''}

    ingredients_tags = soup.find('div', class_='ingredients-bl').find_all('li') if soup.find('div',
                                                                                             class_='ingredients-bl')\
        else []
    ingredients_dict = {}
    for ingredient in ingredients_tags:
        name_tag = ingredient.find('a')
        name = name_tag.get_text(strip=True) if name_tag else ''

        amount_tag = ingredient.find_all('span')[-1] if ingredient.find_all('span') else None
        amount = amount_tag.get_text(strip=True) if amount_tag else ''

        if name:
            ingredients_dict[name] = amount

    description = soup.find('div', class_='article-text').get_text().strip() if soup.find('div',
                                                                                          class_='article-text') else ''
    instruction = ''
    instructions_block = soup.find('ul', itemprop='recipeInstructions')
    if instructions_block:
        instruction = "\n".join([li.get_text(strip=True) for li in instructions_block.find_all('li')])
    image_tag = soup.find('img', {'itemprop': 'image'})
    image_url = image_tag['src'] if image_tag else ''

    if not recipe_name or not ingredients_dict or not instruction:
        return None

    return {
        'url': url,
        'name': recipe_name,
        'ingredients': ingredients_dict,
        'description': description,
        'instruction': instruction,
        'image_url': image_url
    }


def get_pages_range(max_pages=50):
    main_url = 'https://www.povarenok.ru/recipes/~1/'
    soup = get_soup(main_url)

    recipe_count_div = soup.find('div', 'bl-right')
    recipe_count = int(recipe_count_div.find('strong').get_text())
    recipe_per_page_count = 15
    pages_count = math.ceil(recipe_count / recipe_per_page_count)

    if max_pages:
        pages_count = min(pages_count, max_pages)

    return [f'https://www.povarenok.ru/recipes/~{i}/' for i in range(1, pages_count + 1)]


def save_to_csv(data, file_path='recipes.csv'):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'URL', 'Ingredients', 'Description', 'Instruction', 'Image URL'])
        for recipe in data:
            if not recipe or not recipe['name'] or not recipe['ingredients'] or not recipe['instruction']:
                continue
            writer.writerow([
                recipe['name'],
                recipe['url'],
                "; ".join([f"{key}: {value}" for key, value in recipe['ingredients'].items()]),
                recipe['description'],
                recipe['instruction'],
                recipe['image_url']
            ])
