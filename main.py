from sel import TokpedScrap as sc
import merek_all_item as mrk

if __name__ == "__main__":
    link_keyboard = "https://www.tokopedia.com/search?st=&q=keyboard&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    merek_keyboard = mrk.merek_keyboard()
    scrap_keyboard = sc(link_keyboard, merek_keyboard)
    scrap_keyboard.scrap()
    scrap_keyboard.save_data("keyboard.json")
    scrap_keyboard.approximate("keyboard.json")

    link_mouse = "https://www.tokopedia.com/search?st=&q=mouse&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    merek_mouse = mrk.merek_mouse()
    scrap_mouse = sc(link_mouse, merek_mouse)
    scrap_mouse.scrap()
    scrap_mouse.save_data("mouse.json")
    scrap_mouse.approximate("mouse.json")

    link_headphone = "https://www.tokopedia.com/search?q=headphone&source=universe&st=product&navsource=home&srp_component_id=02.02.02.01"
    merek_headphone = mrk.merek_headphone()
    scrap_headphone = sc(link_headphone, merek_headphone)
    scrap_headphone.scrap()
    scrap_headphone.save_data("headphone.json")
    scrap_headphone.approximate("headphone.json")
