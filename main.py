from sel import TokpedScrap as sc
import merek_all_item as mrk

if __name__ == "__main__":
    # link_keyboard = "https://www.tokopedia.com/search?st=&q=keyboard&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    # scrap_keyboard = sc(link_keyboard, mrk.merek_keyboard(), "keyboard.json")
    # scrap_keyboard.scrap()

    # link_mouse = "https://www.tokopedia.com/search?st=&q=mouse&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    # scrap_mouse = sc(link_mouse, mrk.merek_mouse(), "mouse.json")
    # scrap_mouse.scrap()

    # link_headphone = "https://www.tokopedia.com/search?q=headphone&source=universe&st=product&navsource=home&srp_component_id=02.02.02.01"
    # scrap_headphone = sc(link_headphone, mrk.merek_headphone(), "headphone.json")
    # scrap_headphone.scrap()

    # link_tas_laptop = "https://www.tokopedia.com/search?st=&q=tas%20laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    # scrap_tas_laptop = sc(link_tas_laptop, mrk.merek_tas_laptop(), "tas_laptop.json")
    # scrap_tas_laptop.scrap()

    # link_monitor = "https://www.tokopedia.com/search?st=&q=monitor&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
    # scrap_monitor = sc(link_monitor, mrk.merek_monitor(), "monitor.json")
    # scrap_monitor.scrap()

    # link_speaker = "https://www.tokopedia.com/search?navsource=&q=speaker%20komputer%20laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st="
    # scrap_speaker = sc(link_speaker, mrk.merek_speaker(), "speaker.json")
    # scrap_speaker.scrap()

    link_webcam = "https://www.tokopedia.com/search?navsource=&q=webcam&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st="
    scrap_webcam = sc(link_webcam, mrk.merek_webcam(), "webcam.json")
    scrap_webcam.scrap()
