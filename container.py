from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager


class RatingContainer:
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')
    _available_rating_types = ['open', 'men_rapid', 'men_blitz', 'women', 'women_rapid', 'women_blitz']

    def __init__(self):
        self._ratings = {}
        self.update_ratings()

    def update_ratings(self):
        with Chrome(ChromeDriverManager().install(), options=self._chrome_options) as driver:
            for rating_type in self._available_rating_types:
                driver.get(f'https://ratings.fide.com/a_top.php?list={rating_type}')
                top_ten = driver.find_elements_by_tag_name('tr')[1:11]
                self._ratings[rating_type] = '\n'.join(
                    f'{(td := tr.find_elements_by_tag_name("td"))[3].text} - {td[1].text}'
                    for tr in top_ten
                )

    def get(self, item, default_value):
        return self._ratings.get(item, default_value)
