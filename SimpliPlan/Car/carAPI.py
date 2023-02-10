import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag

f = open("cars.csv", "w")

# Write header
f.write(str("car_code,sub_code,make,model,spec,current_price,depreciation,down_payment,installment,coe,road_tax,omv,arf,fuel_economy,fuel_type,coe_incl\n"))

for i in range(12000,13100):
    print(i)
    carCode = str(i)
    #Ensure that url does not redirect
    url = "https://www.sgcarmart.com/new_cars/newcars_pricing.php?CarCode=" + str(i)
    response = urllib.request.urlopen(url)
    if (response.geturl() != url):
        print("redirect")
        continue

    page = BeautifulSoup(response, "html.parser")

    #Check if parallel imported
    parallel_import = False
    title = page.find("a", {"class": "nounderline globaltitle"})
    for tag in title:
        if "Parallel Imported" in tag.text:
            parallel_import = True
            break

    if parallel_import:
        continue

    #Get Make
    text_navigation = page.find("div", {"id": "text_navigation"})
    for tag in text_navigation:
        if isinstance(tag, Tag):
            if "newcars_listing.php?MOD=" in tag['href']:
                car_make = (tag.text)
            elif "newcars_overview.php?CarCode" in tag['href']:
                model_name = (tag.text)

    model_name.replace(car_make + ' ', '')

    content740 = page.find("div", {"class": "content740"})
    grayboxborders = content740.find_all("div", {"class": "grayboxborder"}, recursive=False)

    try:
        tablerows = grayboxborders[0].find("table").find_all("tr", recursive=False)
    except AttributeError:
        continue

    cells = []      #Contains the information for the different models
    for i in range(len(tablerows)):
        if i % 2 == 0:
            cells.extend(tablerows[i].find_all("td", {"valign": "top"}, recursive=False))       #Split row into individual model cell and add to array

    relevant_rows = {"Spec Name": 1, "Current Price": 3, "Depreciation": 4, "Down Payment": 5,
                     "Installment": 6, "COE": 7, "Road Tax": 8, "OMV": 9, "ARF": 10, "VES": 11}

    for cell in cells:
        cellrows = cell.find("table").find_all("tr", recursive=False)

        #Spec name
        spec_name = cellrows[relevant_rows["Spec Name"]].find("a").text
        href = cellrows[relevant_rows["Spec Name"]].find("a")['href']
        subCode = href[href.index("Subcode=") + 8:]
        # print(spec_name)

        # Current Price
        try:
            current_price = cellrows[relevant_rows["Current Price"]].find("span").text
            coe_incl = str(True)
            if "w/o COE" in cellrows[relevant_rows["Current Price"]].find_all("td", recursive=False)[2].text:
                coe_incl = str(False)
        except AttributeError:
            current_price = "POA"
        # print(current_price)

        #Depreciation
        depreciation = cellrows[relevant_rows["Depreciation"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # depreciation = ''.join(i for i in depreciation if i.isdigit())
        # print(depreciation)

        #Down payment
        down_payment = cellrows[relevant_rows["Down Payment"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(down_payment)

        #Installment
        installment = cellrows[relevant_rows["Installment"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(installment)

        #COE
        coe = cellrows[relevant_rows["COE"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(coe)

        #Road Tax
        road_tax = cellrows[relevant_rows["Road Tax"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(road_tax)

        #OMV
        omv = cellrows[relevant_rows["OMV"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(omv)

        #ARF
        arf = cellrows[relevant_rows["ARF"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(arf)

        #ves
        # ves = cellrows[relevant_rows["VES"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
        # print(ves)

        # print()

        skip = False
        fuelType = "-"
        fuelEconomy = "-"
        url = "https://www.sgcarmart.com/new_cars/newcars_specs.php?" + "CarCode=" + str(carCode) + "&Subcode=" + str(subCode)
        response = urllib.request.urlopen(url)
        if (response.geturl() != url):
            skip = True

        page = BeautifulSoup(response, "html.parser")

        if not skip:
            table = page.find("table", id='submodel_spec').find_all('tr', recursive=False)

            #Get fuel type
            fuelType = table[3].find_all("td", recursive=False)[1].text
            if ("Nickel" in fuelType or "Lithium-ion" in fuelType or fuelType == "unknown"):
                fuelType = table[4].find_all("td", recursive=False)[1].text
            # print(fuelType)

            #Get fuel economy
            if fuelType == "Electric":
                try:
                    fuelEconomy = table[11].find_all("td", recursive=False)[1].text[:table[11].find_all("td", recursive=False)[1].text.index("kWh")]
                except ValueError:
                    pass
            elif "Petrol-Electric" in fuelType or "Diesel-Electric" in fuelType:
                fuelEconomy = table[13].find_all("td", recursive=False)[1].text
            else:
                fuelEconomy = table[10].find_all("td", recursive=False)[1].text
            # print(fuelEconomy)

        input_values = [carCode, subCode, car_make, model_name, spec_name, current_price, depreciation, down_payment, installment, coe,
                        road_tax, omv, arf, fuelEconomy, fuelType, coe_incl]

        for i in range(5,14):
            if (input_values[i] != '-' and input_values[i] != "POA"):
                input_values[i] = ''.join(x for x in input_values[i][:10] if (x.isdigit() or x == '.'))       #Get integer only
        print(input_values)

        f.write(','.join(input_values))
        f.write('\n')


f.close()
