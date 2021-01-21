import requests
from bs4 import BeautifulSoup
import json

# 서울 행정구역 가져오기
url = "https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

# print(soup.prettify())

district_gu_list = soup.select("span.mw-headline > a")
district_dong_list = soup.select("dl > dd")

# for i in range(5):
#     print(district_gu_list[i].text, " : ", district_dong_list[i].text)
#     print(district_dong_list[i].text.split(" · "))


# print(len(district_gu_list), len(district_dong_list))


seoul_district = {
    district_gu_list[i].text : district_dong_list[i].text.split("·") for i in range(len(district_dong_list))}


with open("./insta/seoul_district.json", 'w', encoding='utf-8') as file:
    json.dump(seoul_district, file, ensure_ascii=False, indent=2)


with open("./insta/seoul_district.json", encoding="utf-8") as file:
    json_file = json.load(file)

# initial_search_tags = [
#     [gu + "맛집" for gu in seoul_district.keys()],
#     [dong + "맛집" for dong in seoul_district.values()]]
# print(initial_search_tags)

initial_search_tags = [gu + "맛집" for gu in json_file.keys()]
print(initial_search_tags[0])


# for dongs in seoul_district.values():
#     for dong in dongs:
#         print(dong + "맛집")
