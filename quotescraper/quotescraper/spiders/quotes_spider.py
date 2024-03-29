import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"

	# def start_requests(self):
	# 	urls = [
	# 		'http://quotes.toscrape.com/page/1/',
	# 		'http://quotes.toscrape.com/page/2/',
	# 	]
	# 	for url in urls:
	# 		yield scrapy.Request(url=url, callback=self.parse)	

	# or shortcut method, kick off with:
	start_urls = [
		'http://quotes.toscrape.com/page/1/',
		'http://quotes.toscrape.com/page/2/',
	]


	def parse(self, response):
		# iterate through the quotes
		for quote in response.css('.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first(),
				'tags': quote.css('.tags .tag::text').extract()
			}

		# spelling it out:
		# next_page = response.css('.next a::attr(href)').extract_first()
		# if next_page is not None:
			# next_page = response.urljoin(next_page) # urljoin builds absolute link
			# yield scrapy.Request(next_page, callback=self.parse)
			
			# or shortcut method, request.follow - supports relative urls natively
			# yield response.follow(next_page, callback=self.parse)

		# super short shortcut
		for a in response.css('.next a'):
			yield response.follow(a, callback=self.parse)

		# even a one-liner - response.css returns a list so need first one
		response.follow(response.css('li.next a')[0])
		
class AuthorSpider(scrapy.Spider):
	name = 'author'

	start_urls = ['http://quotes.toscrape.com/']

	def parse(self, response):
		# crawl author pages
		# note: by default scrapy filters out duplicated requests to URLs already visited
		for href in response.css('.author + a::attr(href)'):
			yield response.follow(href, self.parse_author)
		# crawl pagination links
		for href in response.css('.next a::attr(href)'):
			yield response.follow(href, self.parse)

	def parse_author(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip()

		yield {
			'name': extract_with_css('h3.author-title::text'),
			'birthdate': extract_with_css('.author-born-date::text'),
			'bio': extract_with_css('.author-description::text'),
		}









