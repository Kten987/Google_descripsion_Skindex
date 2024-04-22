from bs4 import BeautifulSoup
import requests
import unidecode

# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name


def google_search(product_name):
    url = "https://www.google.com/search?q=product+description+of+" + product_name + "&hl=en&gl=sg" # đảm bảo kết quả tìm kiếm là tiếng anh và khu vực singapore
    response = requests.get(url)
    #print(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Lưu ra file để xem cấu trúc html
    # with open("soup_1.txt", "w", encoding="utf-8") as file:
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
    test = convert_productname("The Auragins Acne Rescue Patch")
    print(google_search(test))
