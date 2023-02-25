# url = "https://www.nur.kz/society/2010824-ulitsu-v-astane-nazvali-v-chest-sultana-beybarsa/"
#
# url = url.split("/")[-2]
# print(url)

def get_not_date(project_date):
    not_date = project_date.split(",")
    if len(not_date) == 3:
        not_date = not_date[1].split()
        return f'{not_date[2]}-{not_date[1]}-{not_date[0]}'
    elif len(not_date) == 2:
        not_date = not_date[0].split()
        return f'{not_date[2]}-{not_date[1]}-{not_date[0]}'

    not_date = not_date.split()
    return f'{not_date[2]}-{not_date[1]}-{not_date[0]}'