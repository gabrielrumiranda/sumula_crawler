import scrapy
import json
import os.path
from urllib.parse import urljoin, urlparse
  
class EventsSofaScoreSpider(scrapy.Spider):
    game_round = 2
    name = 'events_sofa_score_spider'
    json_file_name = 'vila_games.json'

    def start_requests(self):
      links = []
      
      with open(self.json_file_name, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
        for game in data:
          links.append(game['incidents_link'])

      for url in links:
          yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        path = urlparse(response.url).path
        game_id = os.path.split(os.path.split(path)[0])[1]
        incidents = json.loads(response.body.decode("utf-8"))['incidents']
        
        with open(game_id +'.json', 'w', encoding='utf8') as fp:
          json.dump(incidents, fp, ensure_ascii=False)
