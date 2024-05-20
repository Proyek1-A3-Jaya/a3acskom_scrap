from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json


class TokpedScrap:
    """
    Class yang berisi method untuk melakukan web scraping pada Tokopedia

    Author
    ----------
    Thafa - 231524027 - @AllThaf
    """

    def __init__(self, link: str, merek_item: list):
        """
        Constructor dari class TokpedScrap

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        link : str
            Link dari halaman web yang akan di-scrap
        """
        self.link = link
        self.merek_item = merek_item
        self.data_list = []

    def driver_setup(self) -> webdriver:
        """
        Method untuk setup driver chrome pada selenium

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Returns
        ----------
        driver : webdriver
            Instance dari webdriver yang digunakan
        """
        opsi = webdriver.ChromeOptions()
        opsi.add_argument("--start-maximized")
        servis = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=opsi, service=servis)
        return driver

    def scroll(self, driver: webdriver) -> None:
        """
        Method untuk melakukan scroll pada halaman web

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        driver : webdriver
            Instance dari webdriver yang digunakan
        """
        for i in range(1, 10):
            akhir = 1000 * i
            driver.execute_script(f"window.scrollTo(0, {akhir})")
            print(f"loading ke-{i}")
            time.sleep(1)
        time.sleep(7)

    def merek(self, nama_item: str) -> str:
        """
        Method untuk mengekstrak merek dari judul halaman web

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        data : BeautifulSoup
            Instance dari BeautifulSoup yang berisi halaman web

        Returns
        ----------
        merek : str

        """
        for i in range(len(self.merek_item) - 1):
            if (
                self.merek_item[i] in nama_item.title()
                or self.merek_item[i] in nama_item
                or self.merek_item[i].title() in nama_item
            ):
                return self.merek_item[i]
        return "Lainnya"

    def extract_data(self, data: BeautifulSoup) -> list:
        """
        Method untuk mengekstrak data dari halaman web

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        data : BeautifulSoup
            Instance dari BeautifulSoup yang berisi halaman web

        Returns
        ----------
        produk : list
            List yang berisi data produk yang telah diekstrak
        """
        produk = []
        for index, area in enumerate(
            data.find_all("div", class_="css-llwpbs"), start=1
        ):
            nama = (
                area.find("div", class_="prd_link-product-name css-3um8ox").get_text(
                    strip=True
                )
                if area.find("div", class_="prd_link-product-name css-3um8ox")
                else "N/A"
            )

            merek = self.merek(nama)

            harga_text = (
                area.find("div", class_="prd_link-product-price css-h66vau").get_text(
                    strip=True
                )
                if area.find("div", class_="prd_link-product-price css-h66vau")
                else "N/A"
            )
            harga = (
                int(harga_text.replace("Rp", "").replace(".", ""))
                if harga_text != "N/A"
                else "N/A"
            )

            gambar_url = (
                area.find("img", class_="css-1q90pod")["src"]
                if area.find("img", class_="css-1q90pod")
                else "N/A"
            )
            produk_link = area.find("a")["href"] if area.find("a") else "N/A"

            lokasi_toko = (
                area.find(
                    "span", class_="prd_link-shop-loc css-1kdc32b flip"
                ).get_text()
                if area.find("span", class_="prd_link-shop-loc css-1kdc32b flip")
                else "N/A"
            )

            rating_text = (
                area.find(
                    "span", class_="prd_rating-average-text css-t70v7i"
                ).get_text()
                if area.find("span", class_="prd_rating-average-text css-t70v7i")
                else "N/A"
            )
            rating = float(rating_text) if rating_text != "N/A" else "N/A"

            terjual = (
                area.find("span", class_="prd_label-integrity css-1sgek4h").get_text()
                if area.find("span", class_="prd_label-integrity css-1sgek4h")
                else "N/A"
            )

            produk_list = {
                "nama": nama,
                "merek": merek,
                "harga": harga,
                "lokasi_toko": lokasi_toko,
                "rating": rating,
                "terjual": terjual,
                "gambar_url": gambar_url,
                "produk_link": produk_link,
            }

            print(f"{index}: {produk_list}")
            produk.append(produk_list)
        return produk

    def scrap(self) -> None:
        """
        Method untuk melakukan web scraping pada Tokopedia

        Author
        ----------
        Thafa - 231524027 - @AllThaf
        """
        driver = self.driver_setup()
        driver.get(self.link)

        try:
            for i in range(2):  # Change this range to scrap more pages
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "css-llwpbs"))
                )

                self.scroll(driver)
                data = BeautifulSoup(driver.page_source, "html.parser")

                self.data_list.extend(self.extract_data(data))

                next_button = driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Laman berikutnya"]'
                )

                if next_button:
                    driver.execute_script("arguments[0].click();", next_button)
                else:
                    break
        finally:
            driver.quit()

    def save_data(self, filename: str) -> None:
        """
        Method untuk menyimpan data hasil web scraping ke sebuah file json

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        filename : str
            Nama file yang akan digunakan untuk menyimpan data
        """
        with open(f"data/{filename}", "w") as file:
            json.dump(self.data_list, file, indent=2)
