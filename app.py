from time import sleep

import bokeh

bokeh.sampledata.download()
from bokeh.palettes import brewer
from bokeh.plotting import output_file
import numpy as np
import pandas as pd
import streamlit as st
from bokeh.models import HoverTool
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as us_counties
from bokeh.transform import cumsum


def home():
    st.markdown("# Kandu Prime | The Harel Farm")
    st.markdown("## :warning: Important alerts :warning:")
    st.error("Thunder storm predicted on thursday afternoon :cloud::zap:")
    st.text("Take recommended actions to be applicable to insurance claims")
    show_thunder = st.checkbox("What should I do?")
    if show_thunder:
        st.info(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    st.warning("Your current batch of rice is due Friday next week :ear_of_rice:")
    st.text("Plan the logistics of your harvest - pre-sell your batch")
    show_rice = st.checkbox(label="More information")
    if show_rice:
        st.info(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    st.success("We have found a buyer for 30% of your next batch of rice! :moneybag:")
    st.markdown("**Sell now, don't miss this opportunity - turn on auto sell for automatic presales.**")
    show_sale = st.checkbox(label="Recommended measures")
    if show_sale:
        st.info(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    st.markdown("## :bar_chart: Analytics brief :bar_chart:")
    st.markdown("You can manage your analytics reviews in the _Analytics_ page")
    st.markdown("### Temperatures in your field")
    st.line_chart(pd.DataFrame(np.random.randint(15, 25, 10), columns=['Celsius']))
    st.markdown("### Prices of your products over the last days")
    veggie_prices = np.array([np.random.randint(500, 630, 10), np.random.randint(800, 830, 10), np.random.randint(1000, 1100, 10)]).T
    st.line_chart(pd.DataFrame(veggie_prices, columns=['Tomato', 'Cucumber', 'Beets']))
    st.markdown("### Crop health map")
    st.image("farms.jpg", use_column_width=True)

    st.markdown("## Finances :moneybag:")
    st.markdown("### Expenses")
    expenses = ['10000', '4350', '500', '500', '500']
    df = pd.DataFrame(expenses, columns=['Price'], index=['Land rent', 'Water', 'Fertilizer', 'Fertilizer', 'Fertilizer'])
    st.dataframe(df)

    st.markdown("### Income")
    incoming = ['7600', '300']
    df = pd.DataFrame(incoming, columns=['Price'], index=['Rice', 'Beets'])
    st.dataframe(df)


def show_analytics():
    st.title("Land analytics :seedling:")
    st.text("Welcome to the analytics page, here you can easily view all your data")
    crops = {
        'Peppers': 150,
        'Tomatoes': 300,
        'Beet': 100,
        'Rice': 63,
    }
    data = pd.Series(crops).reset_index(name='value').rename(columns={'index': 'crop'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * np.pi
    data['color'] = Category20c[len(crops)]
    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@crop: @value", x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.3,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='crop', source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    st.markdown("## Crop diversity")
    st.bokeh_chart(p, use_container_width=True)

    st.markdown("## Land Nitrogen status")
    n = 500
    x = 2 + 2 * np.random.uniform(-5, 5, n)
    y = 2 + 2 * np.random.uniform(-5, 5, n)

    p = figure(title="Farm hexagons", match_aspect=True,
               tools="wheel_zoom,reset", background_fill_color='#440154')
    p.grid.visible = False
    r, bins = p.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)
    p.circle(x, y, color="white", size=1)
    p.add_tools(HoverTool(
        tooltips=[("amount", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))
    st.bokeh_chart(p)

    st.markdown("## Soil humidity")
    palette = tuple(reversed(Viridis6))
    counties = {
        code: county for code, county in us_counties.items() if county["state"] == "wy"
    }

    county_xs = [county["lons"] for county in counties.values()]
    county_ys = [county["lats"] for county in counties.values()]

    crops = [np.random.choice(list(crops.keys())) for _ in counties.values()]
    county_rates = [unemployment[county_id] for county_id in counties]
    color_mapper = LogColorMapper(palette=palette)

    data = dict(
        x=county_xs,
        y=county_ys,
        name=crops,
        rate=county_rates,
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Soil humidity in your field", tools=TOOLS,
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("Crop", "@name"), ("Soil humidity", "@rate%"), ("(Long, Lat)", "($x, $y)")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'rate', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)
    st.bokeh_chart(p)


def show_finances():
    st.title("Finances :euro:")
    st.markdown("## Monthly expenses vs. income, last 12 months")
    monthly_spend = np.random.randint(4000, 6000, 12)
    monthly_gains = np.random.randint(3000, 10000, 12)
    df = pd.DataFrame(np.array([monthly_gains, monthly_spend]).T, columns=["Income", "Expenses"])
    st.area_chart(df)

    st.markdown("## Breakdown of income")

    N = 5
    df = pd.DataFrame(np.random.randint(1000, 2000, size=(12, N)), columns=["Rice", "Tomatoes", "Cucumbers", "Beets", "Carrots"])

    p = figure(x_range=(0, len(df) - 1), y_range=(0, 800))
    p.grid.minor_grid_line_color = '#eeeeee'

    names = ["Rice", "Tomatoes", "Cucumbers", "Beets", "Carrots"]
    p.varea_stack(stackers=names, x='index', color=brewer['Spectral'][N], legend_label=names, source=df)

    # reverse the legend entries to match the stacked order
    p.legend.items.reverse()
    st.bokeh_chart(p)

    st.markdown("## Breakdown of expenses")

    N = 4
    df = pd.DataFrame(np.array(
        [np.random.randint(3000,4000,12),np.random.randint(1000,2000,12),np.random.randint(300,400,12),np.random.randint(500,1000,12)]
    ).T, columns=["Water", "Rent", "Fertilizer", "Electricity"])

    p = figure(x_range=(0, len(df) - 1), y_range=(0, 800))
    p.grid.minor_grid_line_color = '#eeeeee'

    names = ["Water", "Rent", "Fertilizer", "Electricity"]
    p.varea_stack(stackers=names, x='index', color=brewer['Spectral'][N], legend_label=names, source=df)

    # reverse the legend entries to match the stacked order
    p.legend.items.reverse()
    st.bokeh_chart(p)


def show_insurance():
    st.title("Insurances")
    insurances_ppd = {
        "Adverse weather conditions": 100,
        "Fire": 200,
        "Insects": 100,
        "Plant disease": 50,
        "Wildlife": 30,
        "Earthquake": 5,
        "Failure of the irrigation water supply": 300
    }
    st.text("Kandu's insurances are your way to protect your hard work")
    ins_type = st.selectbox("Select Insurance type", list(insurances_ppd.keys()))

    if st.checkbox("I already own prevention and protection tools:"):
        protectors = st.multiselect("Please select:", ["Fences", "Cloud Cannons"])

    crop = st.text_input("Type of crop")
    land_area = st.number_input("Land area")
    land_unit = st.radio("Unit", ["Acre", "KM Sq."])

    date_start = st.date_input("Start date of the insurance")

    if ins_type and crop and land_area and land_unit and date_start:
        with st.spinner('Estimating costs...'):
            sleep(3)
        st.markdown(f"### Total estimated cost: {8.5 * land_area}$")


def show_contact():
    st.title("Contact us")
    st.text("Need help? Kandu team is here for you 24/7. Ask away!")
    topic = st.text_input("Topic")
    content = st.text_area("Question")
    if st.button("Send"):
        if not content:
            st.error("Content is empty")
        elif not topic:
            st.error("Please fill in the topic")
        else:
            # topic.empty()
            # content.empty()
            st.success("Message sent successfully! Our team will contact you soon.")


def main():
    # Sidebar
    st.sidebar.image('jon.jpg', width=150)
    st.sidebar.markdown("## Welcome back, Jonathan!")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Please select a page",
                                ["Home", "Land analytics", "Finances", "Insurance", "Contact"])
    if app_mode == "Home":
        home()

    elif app_mode == "Land analytics":
        show_analytics()

    elif app_mode == "Finances":
        show_finances()

    elif app_mode == "Insurance":
        show_insurance()

    elif app_mode == "Contact":
        show_contact()


if __name__ == '__main__':
    main()
