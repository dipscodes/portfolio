import pandas as pd
import PyPDF2

data_list = []
for year in range(2022, 2012, -1):
    
    pdfFileObj = open(f'enr_{year}.pdf', 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    track = 1
    count_line = 0

    start_line = None

    for pange_number in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[pange_number]
        pagetext = pageObj.extract_text()
        if "The Top 250 List" in pagetext and "THE TOP 250 INTERNATIONAL CONTRACTORS" in pagetext:
            print(year)
            start_line = pange_number
            break

    for pange_number in range(start_line, start_line+5, 1):
        pageObj = pdfReader.pages[pange_number]
        pagetext = pageObj.extract_text()
        page_list = pagetext.split("\n")

        for string in page_list:
            string = string.strip()
            string.replace("*", "")
            if string[0] + string[1] + string[2] + string[3] == str(year):
                continue
            if string[0] == str(track) or string[0] + string[1] == str(track) or string[0] + string[1] + string[2] == str(track):
                track = track + 1
            else:
                continue

            temp = list(string)
            count = 0
            for i in range(len(string)):
                if string[i] == " " or string[i] == "\t":
                    temp[i] = "|"
                    count = count + 1
                if count == 2:
                    break

            string = "".join(temp)
            temp = list(string)
            count = 0

            for i in range(len(string)-1, -1, -1):
                if string[i] == " ":
                    temp[i] = "|"
                    count = count + 1
                if count == 12:
                    break

            temp = "".join(temp)
            data = {}
            c_list = ["current_year_rank", "previous_year_rank", "Details", "INT’L_revenue_21_Millions", "TOTAL_revenue_millionsUSD", "2021_NEWCONTRACTS_MIL", "GEN_Building", "Manufacturing", "Power", "Water_Supply", "Sewer/Waste", "Industrial/Petrolium", "Transportation", "Hazardous_Waste", "Telecom"]
            j = 0

            for i in temp.split("|"):
                data[c_list[j]] = i
                j = j + 1
            
            if "†" in data["Details"]:
                data["Tag"] = "Y"
            else:
                data["Tag"] = "N"
            
            data["INT’L_revenue_21_Millions"] = data["INT’L_revenue_21_Millions"].replace(",", "")
            data["TOTAL_revenue_millionsUSD"] = data["TOTAL_revenue_millionsUSD"].replace(",", "")
            data["2021_NEWCONTRACTS_MIL"] = data["2021_NEWCONTRACTS_MIL"].replace(",", "")
            data["current_year_rank"] = int(data["current_year_rank"])

            if len(data["Details"].split(",")) == 3:
                data["Firm"] = data["Details"].split(",")[0].strip()
                data["City"] = data["Details"].split(",")[1].strip()
                data["Country"] = data["Details"].split(",")[2].replace("†", "").strip()

            if len(data["Details"].split(",")) == 4:
                data["Firm"] = data["Details"].split(",")[0].strip()
                data["City"] = data["Details"].split(",")[1] + "," + data["Details"].split(",")[2].strip()
                data["Country"] = data["Details"].split(",")[3].replace("†", "").strip()

            data["Year"] = year
            data_list.append(data)
    pdfFileObj.close()
enr = pd.DataFrame(data_list)
enr.to_csv("sample_enr_data.csv", sep=";")
