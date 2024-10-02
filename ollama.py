import requests
from bs4 import BeautifulSoup
import json

# Function to send scraped text to llama3 model via Ollama API
def get_llama3_summary(text):
    url = "https://ollama.dealwallet.com/v1/llama3"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": "llama3",
        "prompt": f"Extract and summarize the product details from the following text:\n{text}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json().get('text', "No summary available")
    else:
        return f"Failed to get response from llama3: {response.status_code}, {response.text}"

# eBay search URL for mobiles
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=mobiles&_sacat=0"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all product items
items = soup.find_all('div', class_='s-item__info')

# Iterate over each item and extract the relevant details
for idx, item in enumerate(items, start=1):
    # Extract name, price, link, and raw text of the product
    name = item.find('div', class_='s-item__title')
    price = item.find('span', class_='s-item__price')
    link = item.find('a', class_='s-item__link')['href'] if item.find('a', class_='s-item__link') else "No link available"

    # Get text from each item and handle missing data
    name = name.get_text(strip=True) if name else "No name available"
    price = price.get_text(strip=True) if price else "No price available"
    
    # Combine product information into one text block to send to llama3
    product_info = f"Product: {name}\nPrice: {price}\nLink: {link}"

    # Get detailed summary from llama3
    llama3_summary = get_llama3_summary(product_info)
    
    # Print the extracted and summarized information
    print(f"{idx}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Link: {link}")
    print(f"   Summary by Llama3: {llama3_summary}\n")
