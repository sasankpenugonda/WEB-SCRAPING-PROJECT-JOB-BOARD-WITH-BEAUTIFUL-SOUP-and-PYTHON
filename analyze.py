import pandas as pd
import numpy as np
import plotly.express as px

# Load the data from the Excel file
df = pd.read_excel('data\TimesJobs_scraped_data.xlsx')

# Job Title Analysis
fig = px.histogram(df, x="Job Title", title='Job Title Distribution')
fig.show()

# Experience Required Analysis
fig = px.histogram(df, x="Experience Reqd", title='Experience Required Distribution')
fig.show()

# Company Analysis
fig = px.histogram(df, x="Company", title='Company Distribution')
fig.show()

# City Analysis
fig = px.histogram(df, x="City", title='City Distribution')
fig.show()

# Salary Range Analysis
# Assuming 'Salary Range' is represented as 'Rs 3.10 - 10.15 Lacs p.a.'
df[['Min Salary', 'Max Salary']] = df['Salary Range'].str.split('-', expand=True)

# Replace "Not Mentioned" with NaN
df['Min Salary'] = df['Min Salary'].replace('Not Mentioned', np.nan)
df['Max Salary'] = df['Max Salary'].replace('Not Mentioned', np.nan)

# Remove 'Rs ', ' Lacs p.a.' and convert to numeric
df['Min Salary'] = pd.to_numeric(df['Min Salary'].str.replace('Rs ', '').str.replace(' Lacs p.a.', ''), errors='coerce') * 100000
df['Max Salary'] = pd.to_numeric(df['Max Salary'].str.replace('Rs ', '').str.replace(' Lacs p.a.', ''), errors='coerce') * 100000

fig = px.histogram(df, x="Min Salary", title='Min Salary Distribution')
fig.show()

fig = px.histogram(df, x="Max Salary", title='Max Salary Distribution')
fig.show()
