from app.services.macro_service import (
    get_macro_data
)


def test_get_macro_data():

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

    assert True
    assert len(macro) > 0
assert True