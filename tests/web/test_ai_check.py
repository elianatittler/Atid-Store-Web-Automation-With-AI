def test_forced_failure_for_ai(page):
    page.goto("http://atid.store/")
    # ניסיון לחיצה על אלמנט פיקטיבי כדי לייצר שגיאה וצילום מסך
    page.click("#this-element-does-not-exist-12345")