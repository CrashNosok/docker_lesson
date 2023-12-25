import asyncio
import json
import time

import aiohttp
import fake_useragent
from bs4 import BeautifulSoup as BS
from config import logger
from Interfaces import DatabaseStorage, MessageBroker


class Parser:
    def __init__(self, *, url, message_broker: MessageBroker, database_storage: DatabaseStorage):
        self.url = url
        self.news_refs = []
        self.references_selectors = [".top-story.primary-story",
                                     ".top-story.secondary-story.desktop",
                                     ".news-section-container",
                                     ".content-feed-list"
                                     ]
        self.article_selectors = [".sc-fHekdT.ksRSID.layout-title",
                                  ".sc-jkFpIc.kVHBJX.article-content-body"]
        self.user_agent = fake_useragent.UserAgent().random
        self.headers = {
            'user-agent': self.user_agent
        }
        self.message_broker = message_broker
        self.database_storage = database_storage

    async def run(self, delay_time):
        try:
            await self.get_articles_references()
            await self.parse_articles()
            time.sleep(delay_time)
        except Exception as error:
            logger.error(error)

    async def get_articles_references(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    html = await response.text()
                    soup = BS(html, 'html.parser')

                    for content_selector in self.references_selectors:
                        await self._parse_references(soup=soup, content_selector=content_selector)

            logger.info("Completed main page parsing")
        except Exception as error:
            logger.error(f"Failed main page parsing with error: {error}")

    async def _parse_references(self, *, soup, content_selector):
        try:
            top_section = soup.select(content_selector)[0]

            articles = top_section.select('a')

            for article in articles:
                ref = article.get("href")
                if not ref.startswith("https"):
                    ref = "https://www.benzinga.com" + ref
                if not await self.database_storage.find_news(ref):
                    self.news_refs.append(ref)

            logger.info("Completed references parsing")
            logger.info(f"Was found {len(self.news_refs)} {content_selector} news")
        except Exception as error:
            logger.error(f"Failed to parse references from main page with error: {error}")

    async def parse_articles(self):
        tasks = [self._parse_article(ref=ref) for ref in self.news_refs]
        self.news_refs.clear()
        return await asyncio.gather(*tasks)

    async def _parse_article(self, ref):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=ref, headers=self.headers) as response:
                    response.raise_for_status()
                    html = await response.text()

                    article = BS(html, 'html.parser')
                    title = article.select(".sc-fHekdT.ksRSID.layout-title")[0].text
                    body = article.select("#article-body")[0]

                    logger.info(f"Completed article parsing: {ref}")

                    self.message_broker.send(json.dumps({"title": title, "body": body.text}))
                    logger.info(f"Sent to rabbit: {ref}")

                    await self.database_storage.save({"reference": ref, "title": title, "body": body.text})
                    logger.info(f"Saved in mongo: {ref}")

                    return title, body
        except Exception as error:
            logger.error(f"Failed to parse article: {ref}  with error: {error}")
