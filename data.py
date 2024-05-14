import requests
import pandas as pd

#This is how I will get my data for my dashboard each month.

def dataURL(year, month, city=None, key="d8414676496c9d829cf648e2d51701e2f415548e"): #This code generates the URL I need for all of my variables.
    monthAbbr = {
        1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
        7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec"
    }
    url = "https://api.census.gov/data/"
    year = f"{year}/cps/basic/"
    monthStr = monthAbbr.get(month, "")
    month = f"{monthStr}?get=GTCBSA,PEERNHRO,PEHRACT1,PEHRACT2,PECYC,PEEDUCA,HEFAMINC,HRHTYPE,HRNUMHOU,PRCHLD,PTERNH1O"
    if city:
        cityFilter = f"&GTCBSA={city}"
    else:
        cityFilter = ""
    key = f"&key={key}"
    return url + year + month + cityFilter + key

#GTCBSA = Metropolitan Statistical Area FIPS Code
#PEERNHRO = #Hours usually worked
#PEHRACT1 = # Hours actually worked at main job
#PEHRACT2 = # Hours actually worked at other job(s)
#PECYC = Years of college credit completed
#PEEDUCA = Highest level of school completed
#HEFAMINC = Total family income in past 12 months
#HRHTYPE = Type of family/single individual
#HRNUMHOU = Total # of members
#PRCHLD = Presence of own children <18 years by age group
#PTERNH1O = Earnings-hourly pay rate,amount

def processData(year, month):
  incomeLabels = { #This code transforms the numbers provided by the HEFAMINC variable into meaningful outcomes. The backslashes keep the dollar signs from messing up my formatting.
    "1": "Less Than \$5,000",
    "2": "\$5,000 To \$7,499",
    "3": "\$7,500 To \$9,999",
    "4": "\$10,000 To \$12,499",
    "5": "\$12,500 To \$14,999",
    "6": "\$15,000 To \$19,999",
    "7": "\$20,000 To \$24,999",
    "8": "\$25,000 To \$29,999",
    "9": "\$30,000 To \$34,999",
    "10": "\$35,000 To \$39,999",
    "11": "\$40,000 To \$49,999",
    "12": "\$50,000 To \$59,999",
    "13": "\$60,000 To \$74,999",
    "14": "\$75,000 To \$99,999",
    "15": "\$100,000 To \$149,999",
    "16": "\$150,000 or More",
  }

  educationLabels = { #This code transforms the numbers provided by the PEEDUCA variable into meaningful outcomes.
    "31": "Less Than 1st Grade",
    "32": "1st,2nd,3rd Or 4th Grade",
    "33": "5th Or 6th Grade",
    "34": "7th Or 8th Grade",
    "35": "9th Grade",
    "36": "10th Grade",
    "37": "11th Grade",
    "38": "12th Grade No Diploma",
    "39": "High School Grad-Diploma Or Equiv (GED)",
    "40": "Some College But No Degree",
    "41": "Associate Degree-Occupational/Vocational",
    "42": "Associate Degree-Academic Program",
    "43": "Bachelor's Degree",
    "44": "Master's Degree",
    "45": "Professional School Degree",
    "46": "Doctorate Degree"
  }

  familyTypeLabels = { #This code transforms the numbers provided by the HRHTYPE variable into meaningful outcomes.
    "0": "Non-Interview Household",
    "1": "Husband/Wife Primary Family",
    "2": "Husband/Wife Primary Family",
    "3": "Unmarried Civilian Male - Primary Family Household",
    "4": "Unmarried Civilian Female - Primary Family Household",
    "6": "Civilian Male Primary - Individual",
    "7": "Civilian Female Primary - Individual",
    "9": "Group Quarters With Family",
    "10": "Group Quarters Without Family"
  }

  presenceOfChildrenLabels = { #This code transforms the numbers provided by the PRCHLD variable into meaningful outcomes.
    "-1": "Not a Parent",
    "0": "No Own Children Under 18 Years Old",
    "1": "All Own Children 0-2 Years Old",
    "2": "All Own Children 3-5 Years Old",
    "3": "All Own Children 6-13 Years Old",
    "4": "All Own Children 14-17 Years Old",
    "5": "Own Children 0-2,3-5 Years Old (None 6-17)",
    "6": "Own Children 0-2,6-13 Years Old (None 3-5 or 14-17)",
    "7": "Own Children 0-2,14-17 Years Old (None 3-13)",
    "8": "Own Children 3-5,6-13 Years Old (None 0-2 or 14-17)",
    "9": "Own Children 3-5,14-17 Years Old (None 0-2 or 6-13)",
    "10": "Own Children 6-13 and 14-17 Years Old (None 0-5)",
    "11": "Own Children 0-2, 3-5, and  6-13 Years Old (None 14-17)",
    "12": "Own Children 0-2, 3-5, and 14-17 Years Old \(None 6-13\)",
    "13": "Own Children 0-2, 6-13, and 14-17 Years Old (None 3-5)",
    "14": "Own Children 3-5, 6-13, and 14-17 Years Old (None 0-2)",
    "15": "Own Children from All Age Groups",
  }

#The following code takes the URL and the data it provides and turns it into a data frame for my app to read. It also gets rid of '-1' data variables which just mean that nothing was given and mess up my charts.

  url = dataURL(year, month)
  response = requests.get(url)

  response.raise_for_status()
  data = response.json()
  df = pd.DataFrame(data[1:], columns = data[0])
  df["PEEDUCALabel"] = df["PEEDUCA"].map(educationLabels)
  df["HRHTYPELabel"] = df["HRHTYPE"].map(familyTypeLabels)
  df["PRCHLDLabel"] = df["PRCHLD"].map(presenceOfChildrenLabels)
  df["PEHRACT2"] = df["PEHRACT2"].astype(str)
  df = df[df["PEEDUCA"] != "-1"]
  df = df[df["PEHRACT2"] != "-1"]
  df = df[df["HRHTYPE"] != "-1"]
  df = df[df["HRHTYPE"] != "5"]
  df = df[df["HRHTYPE"] != "8"]
  df = df[df["PEERNHRO"] != "-1"]
  df = df[df["PTERNH1O"] != "-1"]
  return df
