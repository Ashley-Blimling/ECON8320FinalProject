import requests
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from data import processData
import matplotlib.pyplot as plt
from json.decoder import JSONDecodeError

#This code actually generates my dashboard.

cities = { #This code transforms the numbers provided by the GTCBSA variable into meaningful outcomes. I tried to move it to my data.py file, but my app got mad at me so I just put it back here.
  "33660": "Mobile, AL",
  "17420": "Cleveland, TN",
  "27100": "Jackson, MI",
  "33460": "Minneapolis-St Paul-Bloomington, MN-WI",
  "33340": "Milwaukee-Waukesha-West Allis, WI",
  "26820": "Idaho Falls, ID",
  "12540": "Bakersfield, CA",
  "12420": "Austin-Round Rock, TX",
  "19820": "Detroit-Warren-Dearborn, MI",
  "29740": "Las Cruces, NM",
  "14260": "Boise City, ID",
  "39300": "Providence-Warwick, RI-MA",
  "31700": "Manchester-Nashua, NH",
  "41180": "St. Louis, MO-IL",
  "17980": "Columbus, GA-AL",
  "32580": "McAllen-Edinburg-Mission, TX",
  "13820": "Birmingham-Hoover, AL",
  "37460": "Panama City, FL",
  "37340": "Palm Bay-Melbourne-Titusville, FL",
  "19340": "Davenport-Moline-Rock Island, IA-IL",
  "24020": "Glen Falls, NY",
  "49660": "Youngstown-Warren-Boardman, OH-PA",
  "29460": "Lakeland-Winter Haven, FL",
  "14540": "Bowling Green, KY",
  "49180": "Winston-Salem, NC",
  "49740": "Yuma, AZ",
  "48060": "Watertown-Fort Drum, NY",
  "29540": "Lancaster, PA",
  "39340": "Provo-Orem, UT",
  "42540": "Scranton--Wilkes-Barre--Hazelton, PA",
  "47380": "Waco, TX",
  "47260": "Virginia Beach-Norfolk-Newport News, VA-NC",
  "42060": "Santa Barbara-Santa Maria-Goleta, CA",
  "22900": "Fort Smith, AR-OK",
  "16580": "Champaign-Urbana, IL",
  "44100": "Springfield, IL",
  "25260": "Hanford-Corcoran, CA",
  "30980": "Longview, TX",
  "11540": "Appleton, WI",
  "41620": "Salt Lake City, UT",
  "41740": "San Diego-Carlsbad, CA",
  "10580": "Albany-Schenectady-Troy, NY",
  "35980": "Norwich-New London, CT",
  "10900": "Allentown-Bethlehem-Easton, PA-NJ",
  "35620": "New York-Newark- Jersey City, NY-NJ-PA (White Plains central city recoded to balance of metropolitan)",
  "15680": "California-Lexington Park, MD",
  "42140": "Santa Fe, NM",
  "37100": "Oxnard-Thousand Oaks-Ventura, CA",
  "22660": "Fort Collins, CO",
  "22420": "Flint, MI",
  "19100": "Dallas-Fort Worth-Arlington, TX",
  "29820": "Las Vegas-Henderson-Paradise, NV",
  "39740": "Reading, PA",
  "18140": "Columbus, OH",
  "36100": "Ocala, FL",
  "36220": "Odessa, TX",
  "12020": "Athens-Clarke County, GA",
  "22500": "Florence, SC",
  "26420": "Houston-Baytown-Sugar Land, TX",
  "21500": "Erie, PA",
  "40140": "Riverside-San Bernardino-Ontario, CA",
  "30460": "Lexington-Fayette, KY",
  "25540": "Hartford-West Hartford-East Hartford, CT",
  "10180": "Abilene, TX",
  "28700": "Kingsport-Bristol, TN-VA",
  "28020": "Kalamazoo-Portage, MI",
  "48620": "Wichita, KS",
  "30780": "Little Rock-North Little Rock, AR",
  "41420": "Salem, OR",
  "45460": "Terre Haute, IN",
  "43620": "Sioux Falls, SD",
  "37860": "Pensacola-Ferry Pass-Brent, FL",
  "35840": "North-Port-Sarasota-Bradenton, FL",
  "46540": "Utica-Rome, NY",
  "13740": "Billings, MT",
  "22220": "Fayetteville-Springdale-Rogers, AR-MO",
  "21340": "El Paso, TX",
  "23060": "Fort Wayne, IN",
  "47940": "Waterloo-Cedar Falls, IA",
  "26900": "Indianapolis-Carmel-Anderson, IN",
  "20100": "Dover, DE",
  "10420": "Akron, OH",
  "42220": "Santa Rosa, CA",
  "32780": "Medford, OR",
  "16980": "Chicago-Naperville-Elgin, IL-IN-WI",
  "47220": "Vineland-Bridgeton, NJ",
  "44180": "Springfield, MO",
  "44060": "Spokane-Spokane Valley, WA",
  "31420": "Macon, GA",
  "31540": "Madison, WI",
  "36540": "Omaha-Council Bluffs, NE-IA",
  "31180": "Lubbock, TX",
  "24780": "Greenville, NC",
  "35300": "New Haven-Milford, CT",
  "23580": "Gainesville, GA",
  "12220": "Auburn-Opelika, AL",
  "12100": "Atlantic City-Hammonton, NJ",
  "17660": "Coeur d'Alene, ID",
  "14010": "Bloomington, IL",
  "29180": "Lafayette, LA",
  "45300": "Tampa-St. Petersburg-Clearwater, FL",
  "36260": "Ogden-Clearfield, UT",
  "27780": "Johnstown, PA",
  "33780": "Monroe, MI",
  "29700": "Laredo, TX",
  "41940": "San Jose-Sunnyvale-Santa Clara, CA",
  "35380": "New Orleans-Metairie, LA",
  "17140": "Cincinnati, OH-KY-IN",
  "27740": "Johnson City, TN",
  "46140": "Tulsa, OK",
  "33740": "Monroe, LA",
  "47580": "Warner Robins, GA",
  "12940": "Baton Rouge, LA",
  "19660": "Deltona-Daytona Beach-Ormond Beach, FL",
  "19300": "Daphne-Fairhope-Foley, AL",
  "29340": "Lake Charles, LA",
  "48660": "Wichita Falls, TX",
  "42660": "Seattle-Tacoma-Bellevue, WA",
  "38940": "Port St. Lucie-Fort Pierce, FL",
  "25180": "Hagerstown-Martinsburg, MD-WV",
  "41540": "Salisbury, MD-DE",
  "14500": "Boulder, CO",
  "27140": "Jackson, MS",
  "46340": "Tyler, TX",
  "12580": "Baltimore-Columbia-Towson, MD",
  "32820": "Memphis, TN-MS-AR",
  "40420": "Rockford, IL",
  "31140": "Louisville/Jefferson, KY-IN",
  "28420": "Kennewick-Richland, WA",
  "49340": "Worcester, MA-CT",
  "42020": "San Luis Obispo-Paso Robles-Arroyo Grande, CA",
  "46060": "Tucson, AZ",
  "43900": "Spartanburg, SC",
  "22520": "Florence-Muscle Shoals, AL",
  "24140": "Goldsboro, NC",
  "46700": "Vallejo-Fairfield, CA",
  "42100": "Santa Cruz-Watsonville, CA",
  "12260": "Augusta-Richmond County, GA-SC",
  "33860": "Montgomery, AL",
  "34820": "Myrtle Beach-Conway-North Myrtle Beach, SC-NC",
  "40380": "Rochester, NY",
  "39140": "Prescott, AZ",
  "24340": "Grand Rapids-Wyoming, MI",
  "10740": "Albuquerque, NM",
  "28140": "Kansas City, MO-KS",
  "40220": "Roanoke, VA",
  "20500": "Durham-Chapel Hill, NC",
  "14860": "Bridgeport-Stamford-Norwalk, CT",
  "45220": "Tallahassee, FL",
  "49020": "Winchester, VA-WV",
  "17900": "Columbia, SC",
  "19740": "Denver-Aurora-Lakewood, CO",
  "12620": "Bangor, ME",
  "23540": "Gainesville, FL",
  "36740": "Orlando-Kissimmee-Sanford, FL",
  "48700": "Williamsport, PA",
  "46520": "Urban Honolulu, HI",
  "19380": "Dayton, OH",
  "41500": "Salinas, CA",
  "20700": "East Stroudsburg, PA",
  "28660": "Killeen-Temple-Fort Hood, TX",
  "12060": "Atlanta-Sandy Springs-Roswell, GA",
  "15540": "Burlington-South Burlington, VT",
  "40980": "Saginaw, MI",
  "34980": "Nashville-Davidson-Murfreesboro, TN",
  "45060": "Syracuse, NY",
  "42340": "Savannah, GA",
  "27500": "Janesville-Beloit, WI",
  "17820": "Colorado Springs, CO",
  "47900": "Washington-Arlington-Alexandria, DC-VA-MD-WV",
  "16620": "Charleston, WV",
  "16060": "Carbondale-Marion, IL",
  "22180": "Fayetteville, NC",
  "15980": "Cape Coral-Fort Myers, FL",
  "25420": "Harrisburg-Carlisle, PA",
  "30340": "Lewiston-Auburn, ME",
  "15500": "Burlington, NC",
  "11700": "Asheville, NC",
  "45820": "Topeka, KS",
  "45940": "Trenton, NJ",
  "18580": "Corpus Christi, TX",
  "24580": "Green Bay, WI",
  "17460": "Cleveland-Elyria, OH",
  "34580": "Mount Vernon-Anacortes, WA",
  "15380": "Buffalo-Cheektowaga-Niagara Falls, NY",
  "44140": "Springfield, MA",
  "35660": "Niles-Benton Harbor, MI",
  "26620": "Huntsville, AL",
  "33700": "Modesto, CA",
  "26980": "Iowa City, IA",
  "16820": "Charlottesville, VA",
  "12980": "Battle Creek, MI",
  "37900": "Peoria, IL",
  "17300": "Clarksville, TN-KY",
  "13980": "Blacksburg-Christiansburg-Radford, VA",
  "23420": "Fresno, CA",
  "27340": "Jacksonville, NC",
  "33100": "Miami-Fort Lauderdale-West Palm Beach, FL",
  "25940": "Hilton Head Island-Bluffton-Beaufort, SC",
  "38900": "Portland-Vancouver-Hillsboro, OR-WA",
  "41860": "San Francisco-Oakland-Hayward, CA",
  "45780": "Toledo, OH",
  "13140": "Beaumont-Port Arthur, TX",
  "43340": "Shreveport-Bossier City, LA",
  "16540": "Chambersburg-Waynesboro, PA",
  "40060": "Richmond, VA",
  "41700": "San Antonio-New Braunfels, TX",
  "17020": "Chico, CA",
  "27980": "Kahului-Wailuku-Lahaina, HI",
  "43300": "Sherman-Dennison, TX",
  "43780": "South Bend-Mishawaka, IN-MI",
  "12700": "Barnstable Town, MA",
  "19780": "Des Moines-West Des Moines, IA",
  "15180": "Brownsville-Harlingen, TX",
  "34940": "Naples-Immokalee-Marco Island, FL",
  "41100": "St. George, UT",
  "36780": "Oshkosh-Neenah, WI",
  "11100": "Amarillo, TX",
  "39580": "Raleigh, NC",
  "24540": "Greeley, CO",
  "29200": "Lafayette-West Lafayette, IN",
  "47300": "Visalia-Porterville, CA",
  "26580": "Huntington-Ashland, WV-KY-OH",
  "17780": "College Station-Bryan, TX",
  "38220": "Pine Bluff, AR",
  "29620": "Lansing-East Lansing, MI",
  "48140": "Wausau, WI",
  "14020": "Bloomington, IN",
  "39540": "Racine, WI",
  "24860": "Greenville-Anderson-Mauldin, SC",
  "16300": "Cedar Rapids, IA",
  "21660": "Eugene, OR",
  "38300": "Pittsburgh, PA",
  "21780": "Evansville, IN-KY",
  "34060": "Morgantown, WV",
  "34740": "Muskegon, MI",
  "14460": "Boston-Cambridge-Newton, MA-NH",
  "13460": "Bend-Redmond, OR",
  "16740": "Charlotte-Concord-Gastonia, NC-SC",
  "16860": "Chattanooga, TN-GA",
  "38860": "Portland-South Portland, ME",
  "38060": "Phoenix-Mesa-Scottsdale, AZ",
  "28940": "Knoxville, TN",
  "49620": "York-Hanover, PA",
  "39820": "Redding, CA",
  "13780": "Binghamton, NY",
  "40900": "Sacramento--Arden-Arcade-Roseville, CA",
  "25860": "Hickory-Morganton-Lenoir, NC",
  "21140": "Elkhart-Goshen, IN",
  "15940": "Canton-Massillon, OH",
  "24660": "Greensboro-High Point, NC",
  "36420": "Oklahoma City, OK",
  "27260": "Jacksonville, FL",
  "37980": "Philadelphia-Camden-Wilmington, PA-NJ-DE",
  "31080": "Los Angeles-Long Beach-Anaheim, CA (Note the CBSA code change between 2003 and 2013)",
  "22140": "Farmington, NM",
  "22020": "Fargo, ND-MN",
  "16700": "Charleston-North Charleston, SC",
  "44700": "Stockton-Lodi, CA",
  "11460": "Ann Arbor, MI"
}

def plotBoxWhisker(data):  #This code creates my box and whisker plot for Hours Usually Worked.
    st.subheader("Hours Usually Worked:")
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.boxplot(x = data["PEERNHRO"].astype(int), ax = ax, color = "mediumslateblue", whiskerprops = dict(color = "royalblue"), medianprops = dict(color = "green"), capprops = dict(color = "royalblue"))
    ax.set_xlabel("Hours Usually Worked")
    ax.set_xticks(range(0, 81, 5))
    ax.set_xticklabels(range(0, 81, 5))
    st.pyplot(fig)

def plotBarChart(data): #This code creates my bar chart for Hours Worked at a Second Job by Education Level.
  st.subheader("Hours Worked at a Second Job by Education Level:")
  educationOrder = ["Less Than 1st Grade", "1st,2nd,3rd Or 4th Grade", "5th Or 6th Grade", "7th Or 8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade No Diploma", "High School Grad-Diploma Or Equiv (GED)", "Some College But No Degree", "Associate Degree-Occupational/Vocational", "Associate Degree-Academic Program", "Bachelor's Degree", "Master's Degree", "Professional School Degree", "Doctorate Degree"] #This orders my x-axis tick marks, because they were all out of order.
  hoursOrder = [0, 10, 20, 30, 40] #This orders my y-axis tick marks, because they were all out of order.
  fig, ax = plt.subplots(figsize=(10, 6))
  sns.barplot(x = "PEEDUCALabel", y = "PEHRACT2", data = data, hue = "PEEDUCALabel", ci = None, ax = ax, dodge = False, order = educationOrder, bottom = 0)
  ax.set_xlabel("Highest Level of Education Completed")
  ax.set_ylabel("Hours Worked at Other Job(s)")
  plt.gca().invert_yaxis()
  plt.xticks(rotation = 45, ha = "right")
  plt.yticks(ticks = hoursOrder, labels = hoursOrder)
  st.pyplot(fig)


def plotPieCharts(data): #This code creates my pie charts.
  st.subheader("Family Demographics Overview:")

  st.write("Type of Family:")
  fig, ax = plt.subplots()
  pieData = data["HRHTYPELabel"].value_counts(normalize = True)
  labels = pieData.index
  sizes = pieData.values
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pieData.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax) #I took out the labels for any piece of the pie under 3%, because they were too close together, making them unreadable.
  ax.set_ylabel("") #This makes it so the word 'proportion' isn't on the left side of my charts.
  st.pyplot(fig)

  st.write("Number of Members in Families:")
  fig, ax = plt.subplots()
  pieData = data["HRNUMHOU"].value_counts(normalize=True)
  labels = pieData.index
  sizes = pieData.values
  labels = [f"{label} Member" if label == 1 else f"{label} Members" for label in labels]
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pieData.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax)
  ax.set_ylabel("")
  st.pyplot(fig)

  st.write("Presence of Children by Age Group:")
  fig, ax = plt.subplots()
  pieData = data["PRCHLDLabel"].value_counts(normalize=True)
  labels = pieData.index
  sizes = pieData.values
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pieData.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax)
  ax.set_ylabel("")
  st.pyplot(fig)

def main():  #This code generates and orders my dashboard.
  incomeLabels = { #This code transforms the numbers provided by the HEFAMINC variable into meaningful outcomes. The backslashes keep the dollar signs from messing up my formatting. I also tried to move this to my data.py file, but my app got mad at me again so I just put it back here.
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

  st.title("Average Work and Family Demographics of Cities in America")
  year = st.slider("Select Year:", 2010, 2023) #This code lets people select what year they want information for.
  month = st.slider("Select Month:", 1, 12) #This code lets people select what month they want information for.

  df = processData(year, month) #This code pulls the data frame from my data.py.

  selectedCity = st.selectbox("Select City:", list(cities.values()))
  cityCode = list(cities.keys())[list(cities.values()).index(selectedCity)] #This code lets people select what city they want information for.

  if not df.empty:
    df["HEFAMINC"] = df["HEFAMINC"].astype(str)

    df["HEFAMINCLabel"] = df["HEFAMINC"].map(incomeLabels)

    #These codes convert some of my code to numeric data for my charts to process.
    df["PTERNH1O"] = pd.to_numeric(df["PTERNH1O"], errors = "coerce")
    df["PEHRACT1"] = pd.to_numeric(df["PEHRACT1"], errors = "coerce")
    df["PECYC"] = pd.to_numeric(df["PECYC"], errors = "coerce")
    df["HEFAMINC"] = pd.to_numeric(df["HEFAMINC"], errors = "coerce")
    df["HRNUMHOU"] = pd.to_numeric(df["HRNUMHOU"], errors = "coerce")

    col1, col2 = st.columns([1, 1]) #This code seperates my dashboard into two columns. I orginally had the columns as [3, 2], but I think [1, 1] looks beter.

    with col1: #Left Column
      #These codes display the average hourly pay rate.
      avgEarnings = df["PTERNH1O"].mean()
      st.subheader("Average Hourly Pay Rate:")
      st.write(f"${avgEarnings:.2f}")

      #These codes display the average family income.
      modeIncomeLevel = df["HEFAMINCLabel"].mode().iloc[0]
      st.subheader("Average Family Income:")
      st.write(modeIncomeLevel)

      #This code puts my charts in the left column.
      plotBoxWhisker(df)
      plotBarChart(df)

    with col2: #Right Column
      #This code puts my charts in the right column.
      plotPieCharts(df)


if __name__ == "__main__":
  main()
