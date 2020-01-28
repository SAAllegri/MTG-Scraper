from bs4 import BeautifulSoup
import requests
import googlesearch as gs

export = input('Export official names? (Y/N)')

if export == 'Y':
    with open('Test_doc.txt', 'w'):
        pass

with open('Card_Links.txt') as file:
    names = file.readlines()

names = [x.strip() for x in names]

c = 0

urls = []

for n in names:

    if n == '':
        break

    query = str(names[c]) + 'TCG Player'

    for z in gs.search(query, tld='com', num=1, stop=1):
        urls.append(z)

    c = c + 1

v = 0

for r in urls:
    if r.find('http://shop.tcgplayer.com/magic/') and r.find('https://shop.tcgplayer.com/magic/') == -1:
        print('Program error: not specified TCG site for ' + str(names[v]))
        urls[v] = 0

    v = v + 1

c = 0

price_list = []
name_list = []

print('NOTE: This program uses normal card market value *NOT FOIL* unless foil is the only market option')

for n in urls:
    if n == '':
        break

    if n != 0:

        source = requests.get(urls[c]).text

        soup = BeautifulSoup(source, features='html.parser')

        find_price = str(soup.find('td', class_='price-point__data'))

        find_name = str(soup.find('h1', class_='product-details__name'))

        split_price_1 = find_price.split('>')[1]

        split_price_2 = split_price_1.split('<')[0]

        market_price = split_price_2.split('$')[1]

        split_name_1 = find_name.split('<')[1]

        name = split_name_1.split('>')[1]

        price_list.append(float(market_price))

        name_list.append(str(name))

    else:
        price_list.append(0)
        name_list.append(str(names[c] + ' - ERROR'))

    if export == 'Y':
        with open('Test_doc.txt', 'a') as the_file:
            the_file.write(name_list[c] + '\n')

    print(str(name_list[c]) + ' = [$' + str(price_list[c]) + ']' + ' -----link----> ' + str(urls[c]))

    c = c + 1

print('---------------------------------------------------------------------')
print('Deck count: ' + str(len(price_list)))
print('Total deck cost based on TCG market values: $' + str(round(sum(price_list), 4)))
print('---------------------------------------------------------------------')