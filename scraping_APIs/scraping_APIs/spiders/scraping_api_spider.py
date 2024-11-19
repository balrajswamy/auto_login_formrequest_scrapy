import scrapy
import json

class ScrapingApiSpiderSpider(scrapy.Spider):
    name = "scraping_api_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        #print("response_url:\t", response.body)
        #print("response", response.text)
        json_response = json.loads(response.body)
        #print("json_response:\n", json_response)
        quotes = json_response.get("quotes")
        print("\n\n_____\n\n")
        #print("quotes_page==>",json_response.get("has_next"))


        for quote in quotes:
            author_name = quote.get('author', {}).get('name', 'Unknown Author')  # Safe access to nested data
            tags = quote.get('tags', [])  # Returns an empty list if 'tags' key is missing
            title = quote.get('text', 'No text available')  # Default if 'text' key is missing
            yield {"title":title,
                   "author":author_name,
                   "tags": tags}

        next_page = json_response.get("has_next", False)
        print("next_page==>", next_page)
        if next_page:
            next_page_number = json_response.get("page")+1
            next_page_url = f"https://quotes.toscrape.com/api/quotes?page={next_page_number}"
            print("next_page_url==>", next_page_url)
            yield response.follow(url= next_page_url,
                                  callback=self.parse)
