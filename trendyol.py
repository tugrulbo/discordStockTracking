from selenium import webdriver


class TYProductDetailModel:
    url = ""
    title = ""
    seller = ""
    price = ""
    discount = ""
    discountPrice = ""
    rateCount = ""

    def __init__(self, url, title, seller, price, discount, discountPrice, rateCount):
        self.url = url
        self.title = title
        self.seller = seller
        self.price = price
        self.discount = discount
        self.discountPrice = discountPrice
        self.rateCount = rateCount


class Trendyol:

    def findProduct(productUrl):
        #query = query.replace(" ", "%20")
        #query = query.replace("/", "%20")
        driver = webdriver.Firefox()
        # r = driver.get(
        #    'https://www.trendyol.com/sr?q={}'.format(query))
#
        # productUrl = driver.find_element_by_xpath(
        #    '//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div/div/div[1]/a').get_attribute("href")
        # driver.find_element_by_xpath(
        #    '//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div/div/div[1]/a').click()
        driver.get(productUrl)
        productTitle = driver.find_element_by_xpath(
            '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/h1').text

        productSeller = driver.find_element_by_xpath(
            '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/a').text
        productRatingCounter = driver.find_element_by_xpath(
            '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[3]/div/a[1]')
        productPriceClass = driver.find_element_by_xpath(
            '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[5]/div[1]').get_attribute("class")
        productPrice = ""
        productDiscount = ""
        productOldPrice = ""
        if("discounted-stamp" in productPriceClass):
            productOldPrice = driver.find_element_by_xpath(
                '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[5]/div[2]/div/span[1]').text
            productDiscount = driver.find_element_by_xpath(
                '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[5]/div[1]/span').text
            productPrice = driver.find_element_by_xpath(
                '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[5]/div[2]/div/span[2]').text
        else:
            productDiscount = "0"
            productOldPrice = driver.find_element_by_xpath(
                '/html/body/div[1]/div[5]/main/div/div[2]/div[1]/div[2]/div[2]/div/div/div[5]').text

            productPrice = "0"

        return TYProductDetailModel(productUrl, productTitle, productSeller, productPrice, productDiscount, productOldPrice, productRatingCounter)
