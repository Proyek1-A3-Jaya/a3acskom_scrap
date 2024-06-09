from sel import TokpedScrap as sc
import merek_all_item as mrk
import json

if __name__ == "__main__":
    total_terjual_per_kategori = {}

    def scrap_and_approximate(link, merek_func, filename, kategori):
        scrap = sc(link, merek_func, filename)
        scrap.scrap()
        total_terjual = scrap.approximate()
        total_terjual_per_kategori[kategori] = total_terjual

    scrap_and_approximate(
        "https://www.tokopedia.com/search?st=&q=keyboard&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=",
        mrk.merek_keyboard(),
        "keyboard.json",
        "keyboard",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?st=&q=mouse&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=",
        mrk.merek_mouse(),
        "mouse.json",
        "mouse",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?q=headphone&source=universe&st=product&navsource=home&srp_component_id=02.02.02.01",
        mrk.merek_headphone(),
        "headphone.json",
        "headphone",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?st=&q=tas%20laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=",
        mrk.merek_tas_laptop(),
        "tas_laptop.json",
        "tas_laptop",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?st=&q=monitor&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=",
        mrk.merek_monitor(),
        "monitor.json",
        "monitor",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?navsource=&q=speaker%20komputer%20laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=",
        mrk.merek_speaker(),
        "speaker.json",
        "speaker",
    )
    scrap_and_approximate(
        "https://www.tokopedia.com/search?navsource=&q=webcam&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=",
        mrk.merek_webcam(),
        "webcam.json",
        "webcam",
    )

    with open("data/total_terjual_per_kategori.json", "w") as file:
        json.dump(total_terjual_per_kategori, file, indent=2)
