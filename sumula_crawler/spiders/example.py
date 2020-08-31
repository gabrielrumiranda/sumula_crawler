import scrapy
import json
from urllib.parse import urljoin

class ApiSofaScoreSpider(scrapy.Spider):
    name = 'api_sofascore_spider'
    prefix_url_incident = 'https://api.sofascore.com/api/v1/event'
    start_urls = ['https://api.sofascore.com/api/v1/unique-tournament/1281/season/29202/events/last/0']

    def parse(self, response):
        tournament = json.loads(response.body.decode("utf-8"))
        vila_games = []
        for game in tournament['events']:
            if game['homeTeam']['name'] == 'Vila Nova' or  game['awayTeam']['name'] == 'Vila Nova':
                game_id = str(game['id'])
                url_incident = urljoin(self.prefix_url_incident, game_id, '/incidents')
                vila_games.append(game)
        with open('vila_games.json', 'w', encoding='utf8') as fp:
            json.dump(vila_games, fp, ensure_ascii=False)

    def stole_events(self, response):
        incidents = json.loads(response.body.decode('utf-8'))
        yield incidents
