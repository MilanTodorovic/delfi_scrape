from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from threading import Thread


if __name__ == "__main__":

	base_url = "http://www.delfi.rs/"
	extension = "knjige/zanr/114_kompjuteri_i_internet_delfi_knjizare.html"
	books = []

	start = base_url + extension
	while start:
		print("Current: {}".format(start))
		resp = urlopen(start)

		soup = bs(resp, "html.parser")

		book_tables = soup.find_all("div", {"id": "table_spisa_artikala"})
		for _ in book_tables:
			__ = _.find("tr").find_all("td")
			for res in __:
				try:
					url = base_url + res.a["href"]
					s = bs(urlopen(url), "html.parser")
					if s.find("div", {"id": "art_rasprodato"}):
						pass
					else:
						price = s.find("div", {"id": "art_stara_cena"})
						if price:
							books.append([res.a["href"], float(price.span.text)])
						else:
							price = s.find("div", {"id": "art_nova_cena"})
							books.append([res.a["href"], float(price.span.text)])
				except Exception as e:
					pass
		pagination = soup.find("div", {"id": "paginacija"}).find_all("td")
		start = ""
		for page in pagination:
			if page.a.findChildren():
				if page.a.img["alt"] == "sledeca":
					start = base_url + page.a["href"]
			else:
				start = ""
	# print("Books: ")
	# print(books)
	books.sort(key=lambda book: book[1])
	for book in books:
		if book[1] < 1500:
			print(book)
