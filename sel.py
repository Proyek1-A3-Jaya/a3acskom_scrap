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

    def __init__(self, link: str, merek_item: list, filename: str):
        """
        Constructor dari class TokpedScrap

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        link : str
            Link dari halaman web yang akan di-scrap
        merek_item : list
            List yang berisi merek dari item yang akan di-scrap
        filename : str
            Nama file yang akan digunakan untuk menyimpan data hasil scrap
        """
        self.link = link
        self.merek_item = merek_item
        self.filename = filename
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
        nama_item : str
            Nama item yang akan diekstrak mereknya

        Returns
        ----------
        merek : str

        """
        for i in range(len(self.merek_item) - 1):
            if self.merek_item[i].lower() in nama_item.lower():
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
            for i in range(30):  # Change this range to scrap more pages
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
            self.save_data()
            driver.quit()

    def save_data(self) -> None:
        """
        Method untuk menyimpan data hasil web scraping ke sebuah file json

        Author
        ----------
        Thafa - 231524027 - @AllThaf
        """
        with open(f"data/{self.filename}", "w") as file:
            json.dump(self.data_list, file, indent=2)
        self.approximate()

    def approximate(self) -> int:
        """
        Method untuk melakukan aproksimasi data harga

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Return
        ----------
        total_terjual : int
            Jumlah kategori yang terjual
        """
        with open(f"data/{self.filename}", "r") as file:
            data = json.load(file)

        appr_per_merek = {}
        total_terjual = 0

        for produk in data:
            merek = produk["merek"]
            harga = int(produk["harga"])
            rating = float(produk["rating"]) if produk["rating"] != "N/A" else 0
            terjual = self.parse_terjual(produk["terjual"])

            if merek in appr_per_merek:
                appr_per_merek[merek]["jumlah_produk"] += 1
                appr_per_merek[merek]["terjual"] += terjual
                appr_per_merek[merek]["total_harga"] += harga
                appr_per_merek[merek]["rerata_rating"] += rating
                total_terjual += appr_per_merek[merek]["terjual"]

                if harga < appr_per_merek[merek]["harga_terendah"]:
                    appr_per_merek[merek]["harga_terendah"] = harga
                if harga > appr_per_merek[merek]["harga_tertinggi"]:
                    appr_per_merek[merek]["harga_tertinggi"] = harga
            else:
                appr_per_merek[merek] = {
                    "jumlah_produk": 1,
                    "total_harga": harga,
                    "terjual": terjual,
                    "harga_terendah": harga,
                    "harga_tertinggi": harga,
                    "rerata_rating": rating,
                }

        hasil = []

        for merek, info in appr_per_merek.items():
            info["harga_rata_rata"] = info["total_harga"] / info["jumlah_produk"]
            hasil.append(
                {
                    "merek": merek,
                    "jumlah_produk": info["jumlah_produk"],
                    "terjual": info["terjual"],
                    "harga_tertinggi": info["harga_tertinggi"],
                    "harga_terendah": info["harga_terendah"],
                    "harga_rata_rata": round(info["harga_rata_rata"], 2),
                    "rerata_rating": round(
                        info["rerata_rating"] / info["jumlah_produk"], 1
                    ),
                }
            )

        filename_parser = self.filename.split(".")
        with open(f"data/{filename_parser[0]}_appr.json", "w") as file:
            json.dump(hasil, file, indent=2)

        return total_terjual

    def parse_terjual(self, terjual_str: str) -> int:
        """
        Method untuk mengubah string terjual menjadi integer

        Author
        ----------
        Thafa - 231524027 - @AllThaf

        Parameters
        ----------
        terjual_str : str
            String yang akan diubah menjadi integer
        """
        terjual_str = terjual_str.replace(" terjual", "").replace(" terjual", "")
        if "rb" in terjual_str:
            return int(
                float(terjual_str.replace("rb", "").replace("+", "").strip()) * 1000
            )
        elif "+" in terjual_str:
            return int(terjual_str.replace("+", "").strip())
        elif terjual_str == "N/A":
            return 0
        else:
            return int(terjual_str.strip())
