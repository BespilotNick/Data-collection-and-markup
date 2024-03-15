from lxml import etree

tree = etree.parse("Seminar_4/src/web_page.html")
# print(tree)

# title_element = tree.find("body/p")
# print(title_element.text)

list_item = tree.findall("body/ul/li")
for li in list_item:
    a = li.find('a')

    if a is not None:
        print(f'{li.text.strip()} {a.text}')
    else:
        print(li.text)
