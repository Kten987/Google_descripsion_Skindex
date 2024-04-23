from bs4 import BeautifulSoup
import requests
import unidecode
import random


# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name

# Danh sách các proxy
proxies = [f"http://52.73.224.54:3128", f"http://44.219.175.186:80", f"http://162.223.94.164:80", f"http://178.63.230.135:80"]

def google_search(product_name):
    url = "https://www.google.com/search?q=product+description+of+" + product_name + "&hl=en&gl=sg" # đảm bảo kết quả tìm kiếm là tiếng anh và khu vực singapore
    proxy = {"http": random.choice(proxies)} # Chọn ngẫu nhiên một proxy từ danh sách

    response = requests.get(url, proxies=proxy)
    #print(url)
    soup = BeautifulSoup(response.text, "html.parser",)

    ## Lưu ra file để xem cấu trúc html
    with open("soup_3.txt", "w", encoding="utf-8") as file:
        file.write(str(soup))

    results = ""
    # Lấy đoạn mô tả sản phẩm, đk: class_="BNeawe s3v9rd AP7Wnd"
    divs = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    k = 0
    for div in divs:
            # Loại các đoạn về giá, đánh giá, ...
            if not div.find("div") and not div.find("span", class_="r0bn4c rQMQod") and "Missing" not in div.text:
                k += 1
                print(str(div) + "\n" + "--" * 10 )
                results = results + " " + div.text

            if k == 5: # chỉ lây 5 đoạn mô tả đầu tiên
                break
    return results

if __name__ == "__main__":
    test = convert_productname("Channel SUBLIMAGE LE FLUIDE")
    print(google_search(test))
