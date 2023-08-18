import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.header('ECO Score')

# Load the file
df = pd.read_csv('../data/clustered_products.csv')

# Select a protein source
source = st.multiselect(' ', df['SOURCE'].unique())
if not source:
    st.write("Please select a protein source.")
    st.stop()

# Filtering the dataframe for source
mask_source = df['SOURCE'].isin(source)
df_source = df[mask_source]

# Select products
selected_products = st.multiselect(' ', df_source['PRODUCT'].unique())
if not selected_products:
    st.write("Please select a product.")
    st.stop()

# Filtering dataframe for product
mask_product = df_source['PRODUCT'].isin(selected_products)
df_selected_products = df_source[mask_product]

if not df_selected_products.empty:
    score = df_selected_products['LEVEL'].iloc[0]
    st.header(f'ECO Score level: {score}')
else:
    st.write("No products matched the selection or the source is empty.")
    st.stop()

# IMAGE
level_to_image = {
    1: 'pic_1.png',
    2: 'pic_2.png',
    3: 'pic_3.png',
    4: 'pic_4.png'
}

image = None

# Check if the 'LEVEL' column exists and has valid values
if 'LEVEL' in df_selected_products.columns and df_selected_products['LEVEL'].isin(level_to_image.keys()).all():
    selected_level = df_selected_products['LEVEL'].iloc[0]
    image_filename = level_to_image[selected_level]
    image_path = f'../Streamlit/pictures/{image_filename}'
    image = Image.open(image_path)

if image:
    st.image(image)

# Details expander
with st.expander('See more details'):
    st.dataframe(df_selected_products)
    
    if 'PRODUCT' in df_selected_products.columns:
        name_product = df_selected_products['PRODUCT']
        data = pd.read_csv('../data/agribalyse_plot.csv', index_col='PRODUCT')
        
        if name_product.iloc[0] in data.index:
            product = data.loc[name_product]
            product = product.transpose()

            # Create the plot
            fig = px.bar(product, x=product.index, y=name_product)

            # Update bar colors
            total_bar_index = len(product) - 1
            fig.update_traces(marker_color=['pink'] * total_bar_index + ['grey'])

            # Update layout
            fig.update_layout(
                xaxis_title='Stage',
                yaxis_title='Emissions',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            fig.update_yaxes(range=[0, 50])

            st.plotly_chart(fig)
        else:
            st.write("Product not found in the plotting data.")
    else:
        st.write("Product column not available in the selected data.")
