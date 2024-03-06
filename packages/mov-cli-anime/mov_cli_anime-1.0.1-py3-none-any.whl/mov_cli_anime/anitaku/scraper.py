from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional, Dict

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient

import re

from mov_cli import utils
from mov_cli.scraper import Scraper
from mov_cli import Series, Movie, Metadata, MetadataType
from mov_cli import ExtraMetadata

__all__ = ("AnitakuScraper",)

class AnitakuScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://anitaku.to"
        super().__init__(config, http_client)

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        query = query.replace(' ', '-')
        results = self.__results(query, limit)
        return results

    def scrape(self, metadata: Metadata, episode: Optional[utils.EpisodeSelector] = None) -> Series | Movie:
        if episode is None:
            episode = utils.EpisodeSelector()

        url = self.__cdn(metadata.id, episode)

        if metadata.type == MetadataType.MOVIE:
            return Movie(
                url,
                title = metadata.title,
                referrer = self.base_url,
                year = metadata.year,
                subtitles = None
            )

        return Series(
            url,
            title = metadata.title,
            referrer = self.base_url,
            episode = episode,
            season = episode.season,
            subtitles = None
        )

    def __results(self, query: str, limit: int = None) -> List[Metadata]:
        metadata_list = []
        pagination = 1

        while True:
            req = self.http_client.get(f"{self.base_url}/search.html?keyword={query}&page={pagination}")
            soup = self.soup(req)
            items = soup.find("ul", {"class": "items"}).findAll("li")

            if len(items) == 0:
                break

            for item in items:
                id = item.find("a")["href"].split("/")[-1]
                title = item.find("a")["title"]
                year = item.find("p", {"class": "released"}).text.split()[-1]

                page = self.http_client.get(self.base_url + f"/category/{id}")
                _soup = self.soup(page)

                episode_page = _soup.find("ul", {"id": "episode_page"})
                li = episode_page.findAll("li")
                last = li[-1].find("a")["ep_end"]

                if last == "1":
                    type = MetadataType.MOVIE
                else:
                    type = MetadataType.SERIES

                info_body = _soup.find("div", {"class": "anime_info_body_bg"})

                _p = info_body.findAll("p")

                genres = _p[3].findAll("a")

                metadata_list.append(
                    Metadata(
                        id = id,
                        title = title,
                        type = type,
                        year = year,

                        extra_func = lambda: ExtraMetadata(
                            description = [str.strip(x) for x in _p[2].strings if str.strip(x) != ''][1].replace(r"\r\n", "\r\n"),
                            image_url = item.find("img")["src"],
                            alternate_titles = [],
                            cast = None,
                            genres = [i.text.split(" ")[-1] for i in genres]
                        )
                    )
                )

                if len(metadata_list) == limit:
                    break

            pagination += 1

        return metadata_list

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int, int]:
        page = self.http_client.get(f"{self.base_url}/category/{metadata.id}")
        _soup = self.soup(page)

        episode_page = _soup.find("ul", {"id": "episode_page"})
        li = episode_page.findAll("li")
        last = int(li[-1].find("a")["ep_end"])
        return {1: last} # TODO: Return multiple seasons.

    def __cdn(self, id, episode: utils.EpisodeSelector):
        req = self.http_client.get(self.base_url + f"/{id}-episode-{episode.episode}")
        soup = self.soup(req)
        dood = soup.find("li", {"class": "doodstream"}).find("a")["data-video"]
        url = self.__dood(dood)
        if not url:
            streamwish = soup.find("li", {"class": "streamwish"}).find("a")["data-video"]
            url = self.__streamwish(streamwish)
        return url

    def __dood(self, url):
        video_id = url.split("/")[-1]
        webpage_html = self.http_client.get(
            f"https://dood.to/e/{video_id}", redirect = True
        )

        webpage_html = webpage_html.text
        try:
            pass_md5 = re.search(r"/pass_md5/[^']*", webpage_html).group()
        except Exception as e:
            self.logger.error(e)
            return None
        urlh = f"https://dood.to{pass_md5}"
        res = self.http_client.get(urlh, headers = {"referer": "https://dood.to"}).text
        md5 = pass_md5.split("/")
        true_url = res + "MovCli3oPi?token=" + md5[-1]
        return true_url
    
    def __streamwish(self, url):
        req = self.http_client.get(url).text
        file = re.findall(r'file:"(.*?)"', req)[0]
        return file