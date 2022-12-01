import asyncio
import nest_asyncio
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from database.mongo import init_db
from spiders.requests import RequestsSpider


async def main():
    await init_db()
    reactor = AsyncioSelectorReactor()

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(RequestsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
