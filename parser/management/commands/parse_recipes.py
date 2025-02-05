from django.core.management.base import BaseCommand
from CookingHelper.parser.utils import get_pages_range, get_recipe_urls_from_page, get_recipe_from_page, save_to_csv
from functools import reduce
from multiprocessing import Pool
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        n_workers = 4
        pages_range = get_pages_range()

        with Pool(n_workers) as pool:
            recipe_urls = list(
                reduce(
                    lambda x, y: x + y,
                    tqdm(pool.imap_unordered(get_recipe_urls_from_page, pages_range), total=len(pages_range))
                )
            )
            recipe_urls = set(recipe_urls)

        with Pool(n_workers) as pool:
            recipes_data = list(
                tqdm(pool.imap_unordered(get_recipe_from_page, recipe_urls), total=len(recipe_urls))
            )

        save_to_csv(recipes_data)

        self.stdout.write(self.style.SUCCESS(f"Успешно сохранено {len(recipes_data)} рецептов"))
