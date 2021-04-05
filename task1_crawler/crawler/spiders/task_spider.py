import scrapy


class TaskSpider(scrapy.Spider):
    name = "spider_task"
    start_urls = [
        'https://stackoverflow.com/questions?tab=newest&page=1',
    ]
    # allowed_domains = [
    #     'stackoverflow.com/questions',
    # ]

    def parse(self, response, **kwargs):
        page = response.url.split("/")[-1].split("=")[-1]
        filename = f'output/page-{page}.html'
        with open(filename, 'wb') as f:
            if f.write(response.body):
                with open('index.txt', 'a') as f1:
                    f1.write(f'{response.url}  {filename}\n')

        yield from response.follow_all(xpath='.//a[@rel="next"]', callback=self.parse)
