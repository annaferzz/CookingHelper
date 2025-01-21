from bs4 import BeautifulSoup


def parse_recipe(article_html):
    soup = BeautifulSoup(article_html, "html.parser")

    title_tag = soup.find("h2").find("a")
    title = title_tag.get_text(strip=True) if title_tag else "Название отсутствует"

    link = title_tag['href'] if title_tag and title_tag.has_attr('href') else None

    img_tag = soup.find("img", alt=lambda x: x and "Рецепт:" in x)
    image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

    categories = [
        a.get_text(strip=True)
        for a in soup.select(".article-breadcrumbs p span a")
    ]

    description_tag = soup.find("p", text=lambda x: x and "Делюсь" in x)
    description = description_tag.get_text(strip=True) if description_tag else "Описание отсутствует"

    ingredients = [
        a.get_text(strip=True)
        for a in soup.select(".article-tags .tab-content a")
    ]

    author_tag = soup.find("a", class_="user-link")
    author = author_tag.get_text(strip=True) if author_tag else "Автор не указан"

    time_tag = soup.find("span", class_="i-time")
    published_time = time_tag.get_text(strip=True) if time_tag else "Время не указано"

    views_tag = soup.find("span", class_="i-views")
    views = views_tag.get_text(strip=True) if views_tag else "0"

    comments_tag = soup.find("a", class_="i-comments")
    comments = comments_tag.get_text(strip=True) if comments_tag else "0"

    likes_tag = soup.find("span", class_="i-likes")
    likes = likes_tag.get_text(strip=True) if likes_tag else "0"

    recipe_data = {
        "title": title,
        "link": link,
        "image_url": image_url,
        "categories": categories,
        "description": description,
        "ingredients": ingredients,
        "author": author,
        "published_time": published_time,
        "views": views,
        "comments": comments,
        "likes": likes,
    }

    return recipe_data
