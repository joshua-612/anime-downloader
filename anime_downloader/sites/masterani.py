import json
import re
import cfscrape

from anime_downloader.sites.anime import BaseAnime, BaseEpisode
from anime_downloader.const import desktop_headers

scraper = cfscrape.create_scraper()


class MasteraniEpisode(BaseEpisode):
    QUALITIES = ['360p', '480p', '720p', '1080p']

    def _get_sources(self):
        res = scraper.get(self.url, headers=desktop_headers)
        sources_re = re.compile(r'mirrors:.*?(\[.*?\])')
        quality = int(self.quality[:-1])

        sources = json.loads(sources_re.findall(res.text)[0])

        ret = []
        for source in sources:
            if source['quality'] != quality:
                continue

            url = source['host']['embed_prefix'] + source['embed_id']

            if source['host']['embed_suffix']:
                url += source['host']['embed_suffix']

            ret.append((source['host']['name'], url))

        return ret


class Masterani(BaseAnime):
    sitename = 'masterani'
    QUALITIES = ['360p', '480p', '720p', '1080p']
    _api_url = 'https://www.masterani.me/api/anime/{}/detailed'
    _episodeClass = MasteraniEpisode

    def get_data(self):
        anime_id = self.url.split('info/')[-1].split('-')[0]
        url = self._api_url.format(anime_id)
        res = scraper.get(url, headers=desktop_headers).json()
        base_url = 'https://www.masterani.me/anime/watch/{}'.format(
            res['info']['slug']) + '/'

        episode_urls = []
        for episode in res['episodes']:
            url = base_url + episode['info']['episode']
            episode_urls.append((episode['info']['episode'], url))

        self._episode_urls = episode_urls
        self.meta = res['info']

        return self._episode_urls
