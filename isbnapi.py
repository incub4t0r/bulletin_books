import requests


# LINK = "https://openlibrary.org/books/OL7353617M.json"
LINK = "https://openlibrary.org/isbn/002834135X.json"
r = requests.get(LINK)

print(r.text)


# https://openlibrary.org/isbn/002834135X.json
