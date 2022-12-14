from selenium import webdriver
import time
import mysql.connector


def scrape_pexels(word):
    # Open the search page using Selenium
    driver = webdriver.Edge()
    driver.set_page_load_timeout(10)  # Como maximo 5 seg espera a que el url
    driver.get('https://www.pexels.com/search/' + word)
    driver.implicitly_wait(10)  # No pausan codigo, son propiedades

    # FUNCION PARA SCROLLEAR HACIA EL FINAL DE LA PAGINA:
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    # Find all images on the page
    images = driver.find_elements_by_tag_name('img')

    # Extract the URLs of the images
    image_urls = [image.get_attribute('src') for image in images]

    # Close the browser
    driver.close()

    # Return the list of image URLs
    return image_urls


ads = scrape_pexels("ads")


def filter_pexels_urls(urls):
    # Filter the URLs that start with "https://images.pexels.com"
    pexels_urls = [url for url in urls if url.startswith(
        'https://images.pexels.com')]

    # Return the filtered list of URLs
    return pexels_urls


ads = filter_pexels_urls(ads)
print(len(ads))


cnx = mysql.connector.connect(
    host='localhost', user='root', password='', database='propuesta_dataset')
cursor = cnx.cursor()

for url in ads:
    # Insert the URL into the table
    cursor.execute('INSERT INTO imagenes (url) VALUES (%s)', (url,))

cnx.commit()

