import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta
from theHarvester.discovery.constants import MissingKey
from theHarvester.lib.core import AsyncFetcher, Core
class SearchHunterHow:
    def __init__(self, word) -> None:
        self.word = word
        self.total_hostnames: set = set()
        self.key = Core.hunterhow_key()
        if self.key is None:
            raise MissingKey('hunterhow')
        self.proxy = False
    async def do_search(self) -> None:
        query = f'domain.suffix="{self.word}"'
        encoded_query = base64.urlsafe_b64encode(query.encode('utf-8')).decode('ascii')
        page = 1
        page_size = 100  # can be either: 10,20,50,100)
        today = datetime.today()
        one_year_ago = today - relativedelta(days=364)
        start_time = one_year_ago.strftime('%Y-%m-%d')
        end_time = today.strftime('%Y-%m-%d')
        url = f'https://api.hunter.how/search?api-key={self.key}&query={encoded_query}&page={page}&page_size={page_size}&start_time={start_time}&end_time={end_time}'
        response = await AsyncFetcher.fetch_all(
            [url],
            json=True,
            headers={'User-Agent': Core.get_user_agent(), 'x-api-key': f'{self.key}'},
            proxy=self.proxy,
        )
        dct = response[0]
        if 'code' in dct.keys():
            if dct['code'] == 40001:
                print(f'Code 40001 indicates for searchhunterhow: {dct["message"]}')
                return
        for sub in dct['data']['list']:
            self.total_hostnames.add(sub['domain'])
    async def get_hostnames(self) -> set:
        return self.total_hostnames
    async def process(self, proxy: bool = False) -> None:
        self.proxy = proxy
        await self.do_search()