# http://quotes.toscrape.com

# import requests
# from bs4 import BeautifulSoup

# all_quotes=[]
# response=requests.get("http://quotes.toscrape.com")
# # print(response.text)
# soup=BeautifulSoup(response.text, "html.parser")
# # print(soup.body)
# quotes=soup.find_all(class_="quote")
# # print(quotes)
# for quote in quotes:
# 	# print(quote.find(class_="text").text)
# 	# print(quote.find(class_="text").get_text())
# 	# print(quote.find(class_="text"))
# 	# print(quote.find(class_="author").text)
# 	all_quotes.append({
# 		"text":quote.find(class_="text").get_text(),
# 		"author":quote.find(class_="author").get_text(),
# 		"bio-link":quote.find("a")["href"]
# 		})
# # print(all_quotes)
# next_btn=soup.find(class_="next")
# print(next_btn.find("a")["href"])


import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

base_url="http://quotes.toscrape.com"
#  

def scrape_quotes():
	all_quotes=[]
	url="/page/1"
	while url:
		response=requests.get(f"{base_url}{url}")
		print(f"Now scrapping {base_url}{url}...")
		soup=BeautifulSoup(response.text, "html.parser")
		quotes=soup.find_all(class_="quote")

		for quote in quotes:
			all_quotes.append({
				"text":quote.find(class_="text").get_text(),
				"author":quote.find(class_="author").get_text(),
				"bio-link":quote.find("a")["href"]
				})
		next_btn=soup.find(class_="next")	
		url=next_btn.find("a")["href"] if next_btn else None
		# sleep(2)
	return all_quotes

def start_game(quotes):
	# quote=choice(all_quotes)
	quote=choice(quotes)
	print("Herte's a quote : ")
	print(quote["text"])
	print(quote["author"])
	remaining_gusses=4
	guess=''

	while guess.lower() != quote["author"].lower() and remaining_gusses > 0 :
		guess=input(f"Who said this quote ? Guess remaining {remaining_gusses} ")
		remaining_gusses -=1
		if remaining_gusses == 3 :
			response=requests.get(f"{base_url}{quote['bio-link']}")
			soup=BeautifulSoup(response.text, "html.parser")
			birth_date=soup.find(class_="author-born-date").get_text()
			birth_place=soup.find(class_="author-born-location").get_text()
			print(f"Here's a hint : The author was born on {birth_date} in {birth_place}")
		elif remaining_gusses == 2 :
			print(f"Here's a hint : The author's first name starts with {quote['author'][0]}")
		elif remaining_gusses == 1:
			last_initial=quote["author"].split(" ")[1][0]
			print(f"Here's a hint : The authors last name starts with : {last_initial}")
		else:
			print(f"Sorry, you ran out of guess. The answer was {quote['author']}")

		again=''
		while again.lower() not in ('y','yes','n','no'):
			again=input("Would you like to play again ? (y/n)")
		if again.lower() in ('yes','y'):
			return start_game(quotes)
		else:
			print("OK! Goodbye")

quotes=scrape_quotes()
start_game(quotes)
# start_game()		
# print("After while loop!")	

# print(choice(all_quotes)["text"])
# next_btn=soup.find(class_="next")
# print(next_btn.find("a")["href"])
# print(all_quotes)