from . UI import functions as UI

UI.banner()
try:
    UI.run()
except Exception as e:
    print(e)
