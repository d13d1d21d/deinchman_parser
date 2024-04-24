import concurrent.futures
import platform

from utils.utils import logger
from colorama import Fore, Style, just_fix_windows_console
from proxy_client import *
from webparser import Parser


PREFIX = "DEI-"
if platform.system() == "Windows":
    just_fix_windows_console()


logger.log_new_run()

proxy_client = ProxyClient(
    map_proxies("http", open("proxy_list.txt").read().split("\n")),
    retries=5
)
parser = Parser(proxy_client, 100)
print(f"[{Fore.CYAN + Style.BRIGHT}⧖{Style.RESET_ALL}] Получение брендов...")

brands = {}
for i in parser.get_brands():
    if (n_pages := parser.get_n_pages(parser.get_n_products(i))) > 0:
        brands |= { i: n_pages }

print(f"[{Fore.GREEN + Style.BRIGHT}✓{Style.RESET_ALL}] Получено {len(brands)} брендов\n")
logger.log(LogType.INFO, f"\"Получено {len(brands)} брендов\"")

insert_headers = [True, True]
executor = concurrent.futures.ThreadPoolExecutor(50)
nb = 0

for brand, pages in brands.items():
    nb += 1
    product_data = []

    print(f"[{Fore.CYAN + Style.BRIGHT}⧖{Style.RESET_ALL}] Получение товаров из {brand}")

    for page in range(pages):
        product_data += parser.get_products(brand, page)

    if product_data:
        print(f"[{Fore.GREEN + Style.BRIGHT}✓{Style.RESET_ALL}] Получено {len(product_data)} товаров. Обработка...")
        n = 0
        products = []

        for variations in executor.map(parser.get_product_data, product_data):
            if variations:
                products += variations
                n += 1
                if n % 100 == 0:
                    print(f"    > [{Fore.CYAN + Style.BRIGHT}{n}/{len(product_data)}{Style.RESET_ALL}] Обработано {len(products)} вариаций")

        print(f"    > [{Fore.CYAN + Style.BRIGHT}{n}/{len(product_data)}{Style.RESET_ALL}] Обработано {len(products)} вариаций")
        print(f"[{Fore.GREEN + Style.BRIGHT}{brand}{Style.RESET_ALL}: {Fore.CYAN + Style.BRIGHT}{nb}/{len(brands)}{Style.RESET_ALL}] Запись...\n")
        create_df(products, False, PREFIX).to_csv(
            "output/deichmann-products.csv",
            sep=";",
            index=False,
            encoding="utf-8",
            header=insert_headers[0], 
            mode="w" if insert_headers[0] else "a"
        )
        if insert_headers[0]: insert_headers[0] = False
        
        create_df(products, True, PREFIX).to_csv(
            "output/deichmann.csv",
            sep=";",
            index=False,
            encoding="utf-8",
            header=insert_headers[1], 
            mode="w" if insert_headers[1] else "a"
        )
        if insert_headers[1]: insert_headers[1] = False

        logger.log(LogType.INFO, f"\"{brand}: Записан чанк из {len(products)} линий. Обработано {n}/{len(product_data)} товаров\"")