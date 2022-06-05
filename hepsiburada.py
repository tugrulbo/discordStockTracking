from selenium import webdriver


class HPProductDetailModel:
    url = ""
    title = ""
    brand = ""
    seller = ""
    price = ""
    discount = ""
    rate = ""
    rateCount = ""

    def __init__(self, url, title, brand, seller, price, discount, rate, rateCount):
        self.url = url
        self.title = title
        self.brand = brand
        self.seller = seller
        self.price = price
        self.discount = discount
        self.rate = rate
        self.rateCount = rateCount


class HPCategoryModel:
    title = ""
    oldPrice = ""
    price = ""
    discount = 0

    def __init__(self, title, oldPrice, price, discount):
        self.title = title
        self.oldPrice = oldPrice
        self.price = price
        discount = discount


class Hepsiburada:

    def __init__(self) -> None:
        pass

    def findProduct(productCode):

        driver = webdriver.Firefox()
        r = driver.get(
            'https://www.hepsiburada.com/ara?q={}'.format(productCode))
        driver.find_element_by_xpath(
            '//*[@id="i0"]/div').click()

        productURL = driver.find_element_by_xpath(
            '//*[@id="i0"]/div/a').get_attribute("href")
        driver.get(productURL)
        productTitle = driver.find_element_by_xpath(
            '//*[@id="product-name"]').text
        productBrand = driver.find_element_by_class_name(
            'brand-name').text
        productSeller = driver.find_element_by_class_name(
            'seller').text
        productPrice = driver.find_element_by_class_name(
            'price').text
        productOriginalPrice = ""
        if(driver.find_element_by_class_name('price-old').text != ""):
            driver.find_element_by_class_name('price-old').text
        productRate = driver.find_element_by_class_name(
            'rating-star').text
        productRateCount = driver.find_element_by_class_name(
            'product-comments').text

        model = HPProductDetailModel(
            url=productURL,
            title=productTitle,
            brand=productBrand,
            seller=productSeller,
            price=productPrice,
            discount=productOriginalPrice,
            rate=productRate,
            rateCount=productRateCount
        )

        return model

    def findAllItem(category, discountCount=3):
        productListWithModel = []
        PAGE_ITEM_COUNT = 24
        driver = webdriver.Firefox()
        r = driver.get(
            'https://www.hepsiburada.com/hepsigamer')

        categoryURL = driver.find_element_by_xpath(
            '/html/body/div[2]/main/div/section/section[2]/div/div/div[{}]/a'.format(category)).get_attribute("href")
        driver.find_element_by_xpath(
            '/html/body/div[2]/main/div/section/section[2]/div/div/div[{}]/a/div/i'.format(category)).click()

        totalItemsText = driver.find_element_by_class_name("totalItems").text
        totalItems = totalItemsText.split(" ")
        pageCount = int((int(totalItems[0])/24))+1
        for i in range(1, 2):
            driver.get(categoryURL+"?sayfa={}".format(i))
            for i in range(0, PAGE_ITEM_COUNT):
                productList = driver.find_elements_by_class_name("search-item")
                productTitle = productList[i].find_element_by_class_name(
                    "product-title").text
                productOldPrice = ""
                if(productList[i].find_element_by_class_name("first-price-area").text != ""):
                    productOldPrice = productList[i].find_element_by_class_name(
                        "first-price-area").text
                productPrice = ""
                productDiscount = 0
                checkDiscountAttr = productList[i].find_element_by_class_name(
                    "price-content").get_attribute("class")
                if(checkDiscountAttr in "have-two-price"):
                    if(productList[i].find_element_by_class_name('second-price-area')):
                        productPrice = productList[i].find_element_by_class_name(
                            'second-price-area').text
                        productDiscount = productList[i].find_element_by_class_name(
                            "discount-price").text
                        productDiscount = int(productDiscount.replace("%", ""))
                else:
                    productPrice = "0"
                    productDiscount = "0"

                productListWithModel.append(HPCategoryModel(
                    productTitle, productOldPrice, productPrice, productDiscount))
                productListWithModel.sort(
                    key=Hepsiburada.findSorted, reverse=True)

            return productListWithModel

    def findSorted(item):
        return item.discount
