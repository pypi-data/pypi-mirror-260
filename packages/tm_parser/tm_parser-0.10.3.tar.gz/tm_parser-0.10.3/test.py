from tm_parser import Parser

parser = Parser()

for scout in parser:
    print("----------------------------------------------")
    print(f"{scout['Data']['Name']:26}Date       Eagle Req")
    print("----------------------------------------------")
    ## do something with scout
    if "Merit Badges" in scout:
        for badge, data in sorted(
            scout["Merit Badges"].items(), key=lambda x: x[1]["date"]
        ):
            print(f"{badge:26}{data['date']} {data['eagle_required']}")
