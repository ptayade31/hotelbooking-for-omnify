from selenium import webdriver

def get_web_driver(browser='chrome'):
    if browser == 'chrome':
        return webdriver.Chrome()
    elif browser == 'firefox':
        return webdriver.Firefox()
    elif browser == 'safari':
        return webdriver.Safari()
    elif browser == 'edge':
        return webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")