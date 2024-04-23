from bs4 import BeautifulSoup
import requests
import unidecode
import random
from functools import partial
import time

# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name

# Danh sách các proxy
with open("list_proxies.txt", "r") as file:
    proxies = [line.strip() for line in file]

list_proxies = [partial(requests.get, proxies={"http": proxy}) for proxy in proxies]

def google_search(product_name):
    url = "https://www.google.com/search?q=product+description+of+" + product_name + "&hl=en&gl=sg" # đảm bảo kết quả tìm kiếm là tiếng anh và khu vực singapore
    proxy = {"http": random.choice(list_proxies)} # Chọn ngẫu nhiên một proxy từ danh sách

    response = requests.get(url, proxies=proxy)
    # Nếu không lấy được dữ liệu thì chờ 10s và chọn một proxy khác
    if response.status_code != 200 or "This page checks to see if it's really you sending the requests, and not a robot" in response.text:
        time.sleep(10)  # Dừng lại 10s
        list_proxies.remove(proxy) # Xóa proxy hiện tại
        proxy = {"http": random.choice(list_proxies)}  # Chọn ngẫu nhiên một proxy khác
        response = requests.get(url, proxies=proxy)
        
    soup = BeautifulSoup(response.text, "html.parser")
    # ## Lưu ra file để xem cấu trúc html
    # with open("soup_3.txt", "w", encoding="utf-8") as file:
    #     file.write(str(soup))

    results = ""
    # Lấy đoạn mô tả sản phẩm, đk: class_="BNeawe s3v9rd AP7Wnd"
    divs = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    k = 0
    for div in divs:
            # Loại các đoạn về giá, đánh giá, ...
            if not div.find("div") and not div.find("span", class_="r0bn4c rQMQod") and "Missing" not in div.text:
                k += 1
                #print(str(div) + "\n" + "--" * 10 )
                results = results + " " + div.text

            if k == 5: # chỉ lây 5 đoạn mô tả đầu tiên
                break
    return results

if __name__ == "__main__":
    test = convert_productname("Channel SUBLIMAGE LE FLUIDE")
    print(google_search(test))
