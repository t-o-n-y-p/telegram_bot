from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from sample import AVAILABLE_RATING_TYPES


class RatingContainer:
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')

    def __init__(self):
        self._ratings = {}
        self.update_ratings()

    def update_ratings(self):
        with Chrome(ChromeDriverManager().install(), options=self._chrome_options) as driver:
            for rating_type in AVAILABLE_RATING_TYPES:
                driver.get(f'https://ratings.fide.com/a_top.php?list={rating_type}')
                top_ten = driver.find_elements(By.TAG_NAME, 'tr')[1:11]
                self._ratings[rating_type] = '\n'.join(
                    f'{(td := tr.find_elements(By.TAG_NAME, "td"))[3].text} - {td[1].text}'
                    for tr in top_ten
                )

    def get(self, item, default_value):
        return self._ratings.get(item, default_value)
