"""Debug what the OTP screen looks like after form submit."""
import asyncio, os, dotenv
import nodriver as uc
dotenv.load_dotenv()

async def main():
    browser = await uc.start(headless=False)
    tab = await browser.get("https://axiom.trade")
    await asyncio.sleep(5)

    # Open modal
    await tab.evaluate("""
        (function() {
            var btns = document.querySelectorAll('button');
            for (var i=0; i<btns.length; i++) {
                if (btns[i].innerText.trim() === 'Login') { btns[i].click(); return; }
            }
        })()
    """)
    await asyncio.sleep(2)

    # Fill email
    e = await tab.select('input[placeholder="Enter email"]', timeout=10)
    await e.clear_input()
    await e.send_keys(os.getenv("AXIOM_EMAIL", ""))

    # Fill password
    p = await tab.select('input[placeholder="Enter password"]', timeout=5)
    await p.clear_input()
    await p.send_keys(os.getenv("AXIOM_PASSWORD", ""))

    await asyncio.sleep(4)  # Turnstile

    # Submit
    await tab.evaluate("""
        (function() {
            var btns = document.querySelectorAll('button');
            for (var i=0; i<btns.length; i++) {
                var r = btns[i].getBoundingClientRect();
                if (btns[i].innerText.trim() === 'Login' && r.top > 100) { btns[i].click(); return; }
            }
        })()
    """)
    print("Form submitted — waiting 5s for OTP screen...")
    await asyncio.sleep(5)

    # Dump ALL inputs on page
    inputs_json = await tab.evaluate("""
        (function() {
            var inputs = document.querySelectorAll('input');
            var r = [];
            for (var i=0; i<inputs.length; i++) {
                r.push({
                    type: inputs[i].type,
                    name: inputs[i].name,
                    placeholder: inputs[i].placeholder,
                    id: inputs[i].id,
                    maxlength: inputs[i].maxLength,
                    class: inputs[i].className.slice(0, 80)
                });
            }
            return JSON.stringify(r, null, 2);
        })()
    """)
    print("\n=== INPUTS ON PAGE AFTER SUBMIT ===")
    print(inputs_json)

    # Also dump visible text to help identify the OTP prompt
    text = await tab.evaluate("""
        (function() {
            var divs = document.querySelectorAll('h1,h2,h3,p,label,span');
            var r = [];
            for (var i=0; i<divs.length; i++) {
                var t = divs[i].innerText && divs[i].innerText.trim();
                if (t && t.length < 120 && t.length > 3) r.push(t);
            }
            return JSON.stringify([...new Set(r)].slice(0, 30));
        })()
    """)
    print("\n=== VISIBLE TEXT ===")
    print(text)

    print("\n(keeping browser open for 30s for manual inspection)")
    await asyncio.sleep(30)
    browser.stop()

asyncio.run(main())
