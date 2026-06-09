"""Debug script — fill the login form and inspect what happens after submit."""
import asyncio, os
import nodriver as uc
import dotenv
dotenv.load_dotenv()

async def check():
    browser = await uc.start(headless=False)
    tab = await browser.get("https://axiom.trade")
    await asyncio.sleep(4)

    # Click Login
    login_btn = await tab.find("Login", best_match=True)
    await login_btn.click()
    await asyncio.sleep(2)

    # Fill email
    email_input = await tab.select('input[placeholder="Enter email"]', timeout=10)
    print("Email input found:", email_input is not None)
    await email_input.send_keys(os.getenv("AXIOM_EMAIL", ""))

    # Fill password
    pw_input = await tab.select('input[placeholder="Enter password"]', timeout=5)
    print("Password input found:", pw_input is not None)
    await pw_input.send_keys(os.getenv("AXIOM_PASSWORD", ""))

    # Wait for Turnstile to auto-solve (watches for hidden field to get a value)
    print("Waiting for Turnstile to solve...")
    for i in range(30):
        await asyncio.sleep(1)
        val = await tab.evaluate(
            'document.querySelector("input[name=\'cf-turnstile-response\']") ? '
            'document.querySelector("input[name=\'cf-turnstile-response\']").value : ""'
        )
        if val and len(val) > 10:
            print(f"Turnstile solved after {i+1}s, token length: {len(val)}")
            break
    else:
        print("Turnstile did NOT solve in 30s")

    # Find submit button inside the modal — look for the button that's near the inputs
    js_submit = """
    (function(){
        var btns = document.querySelectorAll('button');
        for (var i=0; i<btns.length; i++){
            var r = btns[i].getBoundingClientRect();
            if (r.top > 100 && btns[i].innerText.trim() === 'Login') return btns[i].innerText + '|' + r.top;
        }
        return 'not found';
    })()
    """
    btn_info = await tab.evaluate(js_submit)
    print("Submit button info:", btn_info)

    # Click submit
    # We find all Login buttons and click the one that's in the viewport modal area
    all_btns = await tab.select_all('button')
    submit_btn = None
    for btn in all_btns:
        try:
            txt = await btn.get_html()
            if 'Login' in txt:
                rect = await tab.evaluate(
                    f'(function(){{ var el = document.querySelectorAll("button")[{all_btns.index(btn)}]; '
                    f'var r=el.getBoundingClientRect(); return r.top+","+r.left; }})()'
                )
                print(f"  Button 'Login' at {rect}")
        except Exception:
            pass

    print("Done — check the browser window")
    await asyncio.sleep(60)  # Keep open for manual inspection
    browser.stop()

asyncio.run(check())
