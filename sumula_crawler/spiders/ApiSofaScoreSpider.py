import scrapy
import json
from urllib.parse import urljoin
from functools import reduce

class ApiSofaScoreSpider(scrapy.Spider):
    game_round = 0
    name = 'api_sofascore_spider'
    prefix_url_incident = 'https://api.sofascore.com/api/v1/event/'
    start_urls = ['https://api.sofascore.com/api/v1/unique-tournament/1281/season/29202/events/last/0']

    def parse(self, response):
        tournament = json.loads(response.body.decode("utf-8"))['events']
        if(self.game_round != 0):
            tournament = list(filter(lambda game: game['roundInfo']['round'] == self.game_round, tournament))
        vila_games = []
        others_games = []
        for game in tournament:
            game['incidents_link'] = self.prefix_url_incident + str(game['id']) + '/incidents'
            
            if game['homeTeam']['name'] == 'Vila Nova' or  game['awayTeam']['name'] == 'Vila Nova':
                vila_games.append(game)
            else:
                others_games.append(game)

        with open('vila_games.json', 'w', encoding='utf8') as fp:
            json.dump(vila_games, fp, ensure_ascii=False)
        with open('others_games.json', 'w', encoding='utf8') as fp:
            json.dump(others_games, fp, ensure_ascii=False)
