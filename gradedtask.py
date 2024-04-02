import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#Page settings
st.set_page_config(
    page_title='Adventure Works overview',
    page_icon=':chart_with_upwards_trend:',
    layout='wide')
st.title('_Adventure Works Overview_ :bike:')
st.markdown("""
    <style>
        body {
            background-color: #E1E0D5;
            color: black;
        }
        .streamlit-title {
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

soh_url='https://raw.githubusercontent.com/pleskaite/pythonproject-streamlit/main/salesorderheader.csv?token=GHSAT0AAAAAACQBE573NLMMCLYDSDJTYQSGZQMLYQA'
salesorderheader=pd.read_csv(soh_url)

# Running calculations for scorecards
total_revenue= ound(salesorderheader.TotalDue.sum() / 1000000,2)
total_number_of_sales=salesorderheader.SalesOrderID.count()
total_number_of_customers=salesorderheader.CustomerID.nunique()
average_price_per_sale=round(salesorderheader.TotalDue.sum() / total_number_of_sales)

# Arranging scorecards into the same paragraph
scorecard1, scorecard2, scorecard3, scorecard4=st.columns(4)
with scorecard1:
    st.metric(label="Total income ($, millions)", value=total_revenue)
with scorecard2:
    st.metric(label='Number of sales', value="{:,}".format(total_number_of_sales))
with scorecard3:
    st.metric(label='Number of customers', value="{:,}".format(total_number_of_customers))
with scorecard4:
    st.metric(label='Avg. price per sale ($)', value="{:,}".format(average_price_per_sale))
st.divider()

# Running calculations for pie chart
online_purchases=salesorderheader[salesorderheader.purchase_method == 'Online']
offline_purchases=salesorderheader[salesorderheader.purchase_method == 'Offline']
online_percentage=round(online_purchases.TotalDue.sum() * 100 / salesorderheader.TotalDue.sum())
offline_percentage=round(offline_purchases.TotalDue.sum() * 100 / salesorderheader.TotalDue.sum())

pie_chart_labels=['Online', 'Offline']
pie_chart_values=[online_percentage, offline_percentage]
pie_chart_hover_text=[f'Total revenue: ${revenue:,.0f}<br>Perc. of revenue: {percent:.0f}% <extra></extra>' 
              for revenue, percent in zip([online_purchases.TotalDue.sum(), offline_purchases.TotalDue.sum()], [online_percentage, offline_percentage])]
pie_chart = go.Figure(data=[
    go.Pie(
        labels=pie_chart_labels,
        values=pie_chart_values, 
        hovertemplate=pie_chart_hover_text)])
pie_chart.update_layout(
    width=400, 
    height=400,
    margin=dict(l=60, r=60, t=60, b=60),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.1,
        xanchor='center',
        x=0.5,
        font=dict(size=14)))

# Running calculations for time series
salesorderheader['OrderDate']=pd.to_datetime(salesorderheader['OrderDate'])
salesorderheader['YearMonth']=salesorderheader['OrderDate'].dt.strftime('%Y-%m')
total_revenue_by_month=salesorderheader.groupby('YearMonth')['TotalDue'].sum().reset_index()
total_sales_by_month=salesorderheader.groupby('YearMonth')['SalesOrderID'].count().reset_index()

time_series=go.Figure([
    go.Scatter(
        x=total_revenue_by_month['YearMonth'], 
        y=total_revenue_by_month['TotalDue'],
        mode='lines',
        name='Total income ($)',
        yaxis='y2')])
time_series.add_trace(
    go.Bar(
        x=total_sales_by_month['YearMonth'], 
        y=total_sales_by_month['SalesOrderID'],
        name='Number of sales',
        marker_color='rgb(169, 186, 114)'))
time_series.update_layout(
    width = 1000, 
    height = 400,
    margin=dict(l=60, r=60, t=60, b=60),
    xaxis_title=None,
    yaxis=dict(
        showgrid=False,
        title='Number of sales',
        side='left'),
    yaxis2=dict(
        showgrid=False,
        title='Total income ($)',  
        side='right',
        overlaying='y'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.1,
        xanchor='left',
        x=0.01,
        font=dict(size=14)))

# Arranging pie chart and time series into the same paragraph
col1, col2=st.columns((2, 4))
with col1:
    st.subheader('Purchase method (revenue %)')
    st.plotly_chart(pie_chart)
with col2:
    st.subheader('Growth timeline')
    st.plotly_chart(time_series)
st.divider()

total_revenue_by_country = salesorderheader.groupby('country_name')['TotalDue'].sum().reset_index()

country_bar_chart=go.Figure([
    go.Bar(
        x=total_revenue_by_country['TotalDue'],
        y=total_revenue_by_country['country_name'],
        orientation='h',
        marker_color='rgb(169, 186, 114)',
        text=[f'{round(val/1000000, 2):,.2f}' for val in total_revenue_by_country['TotalDue']],
        textposition='outside',
        textfont=dict(size=14))])

country_bar_chart.update_layout(
    xaxis_title='Total income ($, millions)',
    xaxis=dict(range=[0, 100000000]),
    yaxis=dict(categoryorder='total ascending', tickfont=dict(size=14)),    
    width=400,
    height=400,
    margin=dict(l=60, r=60, t=60, b=60))

sr_url='https://raw.githubusercontent.com/pleskaite/pythonproject-streamlit/main/sales_reasons.csv?token=GHSAT0AAAAAACQBE5732CV53OZCUGSNXC6YZQMLZ2A'
sales_reasons=pd.read_csv(sr_url)

# Running calculations for sales reasons bar chart
total_revenue_per_reason=sales_reasons.groupby('sales_reason_name')['LineTotal'].sum().reset_index()
total_revenue_per_reason_sorted=total_revenue_per_reason.sort_values(by='LineTotal', ascending=False)
sales_with_reason=sales_reasons[sales_reasons.sales_reason_availability == 'Available']
total_revenue_per_reason=sales_reasons.LineTotal.sum()

sales_reasons_bar_chart=go.Figure([
    go.Bar(
        x=total_revenue_per_reason_sorted['sales_reason_name'],
        y=total_revenue_per_reason_sorted['LineTotal'],
        marker_color='rgb(169, 186, 114)',
        text=[f'{round(val/1000000, 2):,.2f}' for val in total_revenue_per_reason_sorted['LineTotal']],
        textposition='outside',
        textfont=dict(size=14))])
    
sales_reasons_bar_chart.update_layout(
    xaxis_title='Total income ($, millions)',
    height=400,
    width=800,
    margin=dict(l=60, r=60, t=60, b=60),
    xaxis=dict(color='black', tickfont=dict(size=14)),
    yaxis=dict(showgrid=False, range=[0, 12000000]))

# Arranging country chart and sales reasons chart into the same paragraph
col1, col2=st.columns((2, 4))
with col1:
    st.subheader('Geographical distribution')
    st.plotly_chart(country_bar_chart)
with col2:
    st.subheader('Top sales reasons')
    st.plotly_chart(sales_reasons_bar_chart)
st.divider()

prd_url='https://raw.githubusercontent.com/pleskaite/pythonproject-streamlit/main/products_details.csv?token=GHSAT0AAAAAACQBE573NMWGNN65J76KLFTYZQMLZZQ'
product_details=pd.read_csv(prd_url)

#Running calculations for product bar chart
product_details['revenue_per_product']=product_details['OrderQty'] * product_details['avg_product_price']
revenue_per_category=product_details.groupby('category_name')['revenue_per_product'].sum().reset_index()
items_per_category=product_details.groupby('category_name')['OrderQty'].sum().reset_index()
rounded_revenue_per_category=round(revenue_per_category['revenue_per_product']/1000000,2)
rounded_items_per_category=round(items_per_category['OrderQty']/1000,1)

products_bar_chart=go.Figure(data=[
    go.Bar(
        name='Total income ($, millions)', x=revenue_per_category['category_name'], y=rounded_revenue_per_category, yaxis='y2', offsetgroup=2,
        text=[f'{val:,.2f}' for val in rounded_revenue_per_category], textposition='outside'),
    go.Bar(
        name='No. of items sold (thousands)', x=items_per_category['category_name'], y=rounded_items_per_category, yaxis='y', offsetgroup=1,
        marker_color='rgb(169, 186, 114)',
        text=[f'{val:,.1f}' for val in rounded_items_per_category], textposition='outside')],
    layout={
        'yaxis': {'title': 'Total income ($)'},
        'yaxis2': {'title': 'No. of items sold', 'overlaying': 'y', 'side': 'right'}})

products_bar_chart.update_layout(
    barmode='group',
    bargroupgap=0.1,
    xaxis_title=None,
    height=400,
    width=600,
    margin=dict(r=100, t=60, b=60),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.1,
        xanchor='left',
        x=0.01,
        font=dict(size=14)),
    xaxis=dict(color='black', tickfont=dict(size=14)),
    yaxis=dict(showgrid=False),
    yaxis2=dict(showgrid=False),)

# Preparing two tables to show avg. price per category & subcategory
avg_category_price=product_details.groupby('category_name')['avg_product_price'].mean().reset_index().round({'avg_product_price': 2}).sort_values(by='avg_product_price', ascending=False)
avg_subcategory_price=product_details.groupby('subcategory_name')['avg_product_price'].mean().reset_index().round({'avg_product_price': 2}).sort_values(by='avg_product_price', ascending=False)

avg_category_table=go.Figure(data=[
    go.Table(
        header=dict(values=["Category name", "Avg. price ($, descending)"], align='left', font=dict(color='grey', size=14)),
        cells=dict(values=[avg_category_price['category_name'], avg_category_price['avg_product_price']], align='left',font=dict(color='black', size=14),height=30))])
avg_category_table.update_layout(
    height=400,
    width=400,
    margin=dict(t=40),)

avg_subcategory_table=go.Figure(data=[
    go.Table(
        header=dict(values=["Subcategory name", "Avg. price ($, descending)"], align='left',font=dict(color='grey', size=14)),
        cells=dict(values=[avg_subcategory_price['subcategory_name'], avg_subcategory_price['avg_product_price']], align='left',font=dict(color='black', size=14),height=30))])
avg_subcategory_table.update_layout(
    height=450,
    width=400,
    margin=dict(t=40))

# Arranging products chart and both tables into the same paragraph
col1, col2, col3=st.columns((2, 1.5, 1.5))
with col1:
    st.subheader('Best selling categories')
    st.plotly_chart(products_bar_chart)
with col3:
    st.subheader('Avg. item price per category')
    st.plotly_chart(avg_category_table)
with col2:
    st.subheader('Avg. item price per subcategory')
    st.plotly_chart(avg_subcategory_table)
