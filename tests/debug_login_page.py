import asyncio
import nodriver as uc

async def check():
    browser = await uc.start(headless=False)
    tab = await browser.get("https://axiom.trade")
    await asyncio.sleep(4)

    # Click Login button
    login_btn = await tab.find("Login", best_match=True)
    if login_btn:
        print("Found Login button, clicking...")
        await login_btn.click()
        await asyncio.sleep(3)
    else:
        print("No Login button found")

    url = await tab.evaluate("window.location.href")

    js = """
    (function() {
        var inputs = document.querySelectorAll('input');
        var result = [];
        for (var i = 0; i < inputs.length; i++) {
            result.push({type: inputs[i].type, name: inputs[i].name, placeholder: inputs[i].placeholder, id: inputs[i].id, class: inputs[i].className.slice(0,60)});
        }
        return JSON.stringify(result);
    })()
    """
    inputs_json = await tab.evaluate(js)

    js2 = """
    (function() {
        var btns = document.querySelectorAll('button');
        var result = [];
        for (var i = 0; i < Math.min(btns.length, 10); i++) {
            result.push({text: btns[i].innerText.trim().slice(0, 40), type: btns[i].type});
        }
        return JSON.stringify(result);
    })()
    """
    btns_json = await tab.evaluate(js2)

    print("URL after click:", url)
    print("Inputs after click:", inputs_json)
    print("Buttons after click:", btns_json)
    browser.stop()

asyncio.run(check())
