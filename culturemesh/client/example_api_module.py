#
# As a first example of what the API module is going to look like. 
#

""" Gets a single novel from Project Gutenberg """

GUTENBERG_BASE_URL_FORMAT = "http://www.gutenberg.org/cache/epub/{ebook_num}/pg{ebook_num}.txt"

def get_gutenberg_novel(client, ebook_num):
	"""
	A simple example API call for testing/showcase. 
	Gets the text for a book with Project Gutenberg number EBOOK_NUM.
	"""
	
	params = {}
	return client._request(GUTENBERG_BASE_URL_FORMAT.format(ebook_num=ebook_num), {}).text