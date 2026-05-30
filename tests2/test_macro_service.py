from app.services.macro_service import (
    get_macro_data
)

macro=get_macro_data()

print(
    "\nMACRO DATA\n"
)

for k,v in macro.items():

    print(

        f"{k} | "

        f"Price={v['price']} | "

        f"Daily={v['daily_change_pct']}%"
    )