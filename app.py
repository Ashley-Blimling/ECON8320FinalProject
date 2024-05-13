import requests
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from data import processData
import matplotlib.pyplot as plt
from json.decoder import JSONDecodeError

#This code actually generates my dashboard.

def plotBoxWhisker(data):  #This code creates my box and whisker plot for hours usually worked..
    st.subheader("Hours Usually Worked:")
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.boxplot(x = data["PEERNHRO"].astype(int), ax = ax, color = "mediumslateblue", whiskerprops = dict(color = "royalblue"), medianprops = dict(color = "green"), capprops = dict(color = "royalblue"))
    ax.set_xlabel("Hours Usually Worked")
    ax.set_xticks(range(0, 81, 5))
    ax.set_xticklabels(range(0, 81, 5))
    st.pyplot(fig)

def plotBarChart(data): #This code creates my bar chart for hours worked at a second job by education level.
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
  pie_data = data["HRHTYPELabel"].value_counts(normalize = True)
  labels = pie_data.index
  sizes = pie_data.values
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pie_data.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax) #I took out the labels for any piece of the pie under 3%, because they were too close together, making them unreadable.
  ax.set_ylabel("")
  st.pyplot(fig)

  st.write("Number of Members in Families:")
  fig, ax = plt.subplots()
  pie_data = data["HRNUMHOU"].value_counts(normalize=True)
  labels = pie_data.index
  sizes = pie_data.values
  labels = [f"{label} Member" if label == 1 else f"{label} Members" for label in labels]
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pie_data.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax)
  ax.set_ylabel("")
  st.pyplot(fig)

  st.write("Presence of Children by Age Group:")
  fig, ax = plt.subplots()
  pie_data = data["PRCHLDLabel"].value_counts(normalize=True)
  labels = pie_data.index
  sizes = pie_data.values
  labels = [label if size >= 0.03 else "" for label, size in zip(labels, sizes)]
  pie_data.plot.pie(autopct = lambda pct: f"{pct:.1f}%" if pct >= 3 else "", labels = labels, ax = ax)
  ax.set_ylabel("")
  st.pyplot(fig)

def main():  #This code generates and orders my dashboard.
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

      #This code puts my charts in the left column.
      plotBoxWhisker(df)
      plotBarChart(df)

    with col2: #Right Column
      #These codes display the average family income.
      modeIncomeLevel = df["HEFAMINCLabel"].mode().iloc[0]
      st.subheader("Average Family Income:")
      st.write(modeIncomeLevel)

      #This code puts my charts in the right column.
      plotPieCharts(df)


if __name__ == "__main__":
  main()
