# Browser_Api
# like
# console.log
# alert
# windows.size
# ...etc

browser_Action = ""

def alert(text):
    browser_Action = f"alert('{text}')"
    return browser_Action

def run():
    with open('./output/actions.js', 'w') as file:
        file.write(browser_Action)