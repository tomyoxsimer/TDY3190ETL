import pandas as pd
import numpy as np
import pandas_bokeh as pb
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import streamlit as st

pb.output_notebook()

#EXTRACT
df = pd.read_csv("https://raw.githubusercontent.com/tomyoxsimer/TDY3190ETL/main/zillow.csv")

df.plot_bokeh(kind='bar', x='RegionName', y=['2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Initial Data Set')

#TRANSFORMATION
# transformation 1 drop 2014 through 2019
df = df.drop(df.loc[:, '2014-01':'2019-12'].columns, axis =1)

df.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Data Set after Dropping 2014 through 2019')

# transformation 2 drop RegionID and SizeRank
df = df.drop('RegionID', axis=1)
df = df.drop('SizeRank', axis =1)

# transformation 3 drop every state besides NC, SC, VA, TN, and GA
values = ["NC", "GA", "SC", "VA", "TN"]
df = df[df.RegionName.str.contains('|'.join(values))]

df.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Data Set after Dropping States I will not live in')

# transformation 4 average 2020, 2021, & 2020 through 2021
df['Rent Average Since 2020'] = df.iloc[:, 2:-1].sum(axis=1) / 22
df['2020 Rent Average'] = df.iloc[:, 2:13].sum(axis=1) / 12
df['2021 Rent Average'] = df.iloc[:, 14:-1].sum(axis=1) / 10

df.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Data Set after Dropping States I will not live in')


# transformation 5 seperate states into individual dataframes
GAdf = df[df.RegionName.str.contains("GA")]
NCdf = df[df.RegionName.str.contains("NC")]
SCdf = df[df.RegionName.str.contains("SC")]
TNdf = df[df.RegionName.str.contains("TN")]
VAdf = df[df.RegionName.str.contains("VA")]

# transformation 6 average rent per month per state
VAdf2= VAdf.iloc[:, 1:-1].sum(axis= 0) / 2
VAdf = VAdf.append(VAdf2, ignore_index = True)
VAdf['RegionName'] = VAdf['RegionName'].replace([np.nan],'Average Rent by Month')

NCdf2= NCdf.iloc[:, 1:-1].sum(axis= 0) / 5
NCdf = NCdf.append(NCdf2, ignore_index = True)
NCdf['RegionName'] = NCdf['RegionName'].replace([np.nan],'Average Rent by Month')

GAdf2= GAdf.iloc[:, 1:-1].sum(axis= 0) / 3
GAdf = GAdf.append(GAdf2, ignore_index = True)
GAdf['RegionName'] = GAdf['RegionName'].replace([np.nan],'Average Rent by Month')

SCdf2= SCdf.iloc[:, 1:-1].sum(axis= 0) / 3
SCdf = SCdf.append(SCdf2, ignore_index = True)
SCdf['RegionName'] = SCdf['RegionName'].replace([np.nan],'Average Rent by Month')

TNdf2= TNdf.iloc[:, 1:-1].sum(axis= 0) / 3
TNdf = TNdf.append(TNdf2, ignore_index = True)
TNdf['RegionName'] = TNdf['RegionName'].replace([np.nan],'Average Rent by Month')

#LOAD
pb.output_notebook()

NCchart = NCdf.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Rent Prices by Month in North Carolina')

TNchart = TNdf.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Rent Prices by Month in Tennessee')

SCchart = SCdf.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Rent Prices by Month in South Carolina')

GAchart = GAdf.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Rent Prices by Month in Georgia')

VAchart = VAdf.plot_bokeh(kind='bar', x='RegionName', y=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10'], xlabel = 'City', ylabel = 'Rent Price', title = 'Rent Prices by Month in Virginia')

st.bokeh_chart(NCchart, use_container_width=True)

st.bokeh_chart(SCchart, use_container_width=True)

st.bokeh_chart(TNchart, use_container_width=True)

st.bokeh_chart(VAchart, use_container_width=True)

st.bokeh_chart(GAchart, use_container_width=True)
