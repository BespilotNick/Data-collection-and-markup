from lxml import etree

tree = etree.parse("Seminar_4/src/web_page.html")
# print(tree)

# title_element = tree.find("body/p")
# print(title_element.text)

# list_item = tree.findall("body/ul/li")
# for li in list_item:
#     a = li.find('a')

#     if a is not None:
#         print(f'{li.text.strip()} {a.text}')
#     else:
#         print(li.text)


# title_element = tree.xpath('//title/text()')[0]
# # print(title_element)

# list_items = tree.xpath('//li')
# for li in list_items:
#     text = ''.join(map(str.strip, li.xpath('.//text()')))
#     print(text)

# list_items = tree.xpath('//ul/descendant::li')
# for li in list_items:
#     text = ''.join(map(str.strip, li.xpath('.//text()')))
#     print(text)


html = tree.getroot()

title_element = html.cssselect('title')
print(title_element[0].text)
