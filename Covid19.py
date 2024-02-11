"""COVID-19 DATADASHBOARD"""

"""Auteur: Kasthury Inparajah"""

"""Dit script bevat functies voor het analyseren en visualiseren van COVID-19 data van IC-patiënten."""

#  LIBRARIES 
import pandas as pd
import numpy as np
import panel as pn
import matplotlib.pyplot as plt
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from bokeh.io import output_notebook
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, HoverTool
import holoviews as hv
import holoviews.plotting.bokeh
from bokeh.plotting import figure


########################################################### COVID DATA ###################################################################

covid_patient_data = 'Covid-data\covid_patienten_export.tsv'
covid_measurement_data = 'Covid-data\covid_meetgegevens_export.tsv'

patient = pd.read_csv(covid_patient_data, sep='\t')
measurement = pd.read_csv(covid_measurement_data, sep='\t')

# Bruikbare data van covid_patient_data
data_bruikbaarheid = patient["BRUIKBAAR"]

# lege lijst voor bruikbare data
Aantal_bruikbaar = []

# Waarden in lege lijsten zetten
for i in range(len(data_bruikbaarheid)):
    if data_bruikbaarheid[i] == "ja":
        Aantal_bruikbaar.append("ja")

Data_patienten = patient.loc[patient['BRUIKBAAR'] == 'ja']


############################################################## DATA VOOR DASHBOARD ########################################################

# Mannen en vrouwen 
geslacht_man = Data_patienten.loc[Data_patienten['GESLACHT'] == 'm']
geslacht_vrouw = Data_patienten.loc[Data_patienten['GESLACHT'] == 'v']

# Aantal mannen en vrouwen
aantal_mannen = len(geslacht_man.index)
aantal_vrouwen = len(geslacht_vrouw.index)
totaal_patienten = aantal_vrouwen + aantal_mannen

# percentage mannen en vrouwen
percentage_mannen = aantal_mannen / totaal_patienten * 100
percentage_vrouwen = aantal_vrouwen / totaal_patienten * 100
afgerond_percentage_mannen = round(percentage_mannen, 2)
afgerond_percentage_vrouwen = round(percentage_vrouwen, 2)


###################################################### LEEFTIJD ###########################################################################

# gem leeftijd patienten 
leeftijd_patienten = Data_patienten['LEEFTIJD']
gemiddelde_leeftijd_patienten = np.round(leeftijd_patienten.mean())

# gemiddelde leeftijd mannen
leeftijd_mannelijke_patienten = Data_patienten.loc[Data_patienten['GESLACHT'] == 'm', 'LEEFTIJD']
gemiddelde_leeftijd_mannelijke_patienten = np.round(leeftijd_mannelijke_patienten.mean(), 2)

# gemiddelde leeftijd vrouwen
leeftijd_vrouwelijke_patienten = Data_patienten.loc[Data_patienten['GESLACHT'] == 'v', 'LEEFTIJD']
gemiddelde_leeftijd_vrouwelijke_patienten = np.round(leeftijd_vrouwelijke_patienten.mean(), 2)


############################################################## GEWICHT #####################################################################

# gewicht patienten
gewicht = Data_patienten['GEWICHT']
gemiddelde_gewicht = np.round(gewicht.mean())

# gemiddeld gewicht mannen
gewicht_mannen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'm', 'GEWICHT']
gemiddeld_gewicht_mannen = np.round(gewicht_mannen.mean(), 2)

# gemiddeld gewicht vrouwen
gewicht_vrouwen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'v', 'GEWICHT']
gemiddeld_gewicht_vrouwen = np.round(gewicht_vrouwen.mean(), 2)


############################################################ LENGTE #####################################################################

# gemiddelde lengte patienten
lengte = Data_patienten['LENGTE']
gemiddelde_lengte = np.round(lengte.mean())

# gemiddelde lengte mannen
lengte_mannen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'm', 'LENGTE']
gemiddelde_lengte_mannen = np.round(lengte_mannen.mean(), 2)

# gemiddelde lengte vrouwen
lengte_vrouwen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'v', 'LENGTE']
gemiddelde_lengte_vrouwen = np.round(lengte_vrouwen.mean(), 2)


########################################################## APACHE SCORE ##################################################################

# gemiddelde apache IV score patienten
apache = Data_patienten['APACHE_IV_SCORE']
gemiddelde_apache = np.round(apache.mean())

# gemiddelde apache IV score mannen
apache_mannen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'm', 'APACHE_IV_SCORE']
gemiddelde_apache_mannen = np.round(apache_mannen.mean(), 2)

# gemiddelde apache IV score vrouwen
apache_vrouwen = Data_patienten.loc[Data_patienten['GESLACHT'] == 'v', 'APACHE_IV_SCORE']
gemiddelde_apache_vrouwen = np.round(apache_vrouwen.mean(), 2)


###################################################### BMI #############################################################################

# BMI patienten
gewicht_pat = Data_patienten['GEWICHT']
lengte_pat = Data_patienten['LENGTE']

# BMI 
bmi_patienten = gewicht / ((lengte / 100) ** 2)
bmi_mannen = gewicht_mannen / ((lengte_mannen / 100) ** 2)
bmi_vrouwen = gewicht_vrouwen / ((lengte_vrouwen / 100) ** 2)

# Gemiddelde BMI 
gemiddelde_bmi_patienten = np.round(bmi_patienten.mean(), 2)
gemiddelde_bmi_mannen = np.round(bmi_mannen.mean(), 2)
gemiddelde_bmi_vrouwen = np.round(bmi_vrouwen.mean(), 2)


# BMI en apache dataframe maken
bmi_apache_data = pd.DataFrame()
bmi_apache_data['PATIENT_ID'] = Data_patienten['PATIENT_ID']
bmi_apache_data['GESLACHT'] = Data_patienten['GESLACHT']
bmi_apache_data['GEWICHT'] = Data_patienten['GEWICHT']
bmi_apache_data['LENGTE'] = Data_patienten['LENGTE']
bmi_apache_data['APACHE_IV_SCORE'] = Data_patienten['APACHE_IV_SCORE']

# BMI berekenen
bmi_apache_data['BMI'] = bmi_apache_data['GEWICHT'] / ((bmi_apache_data['LENGTE'] / 100) ** 2)

# Kleur toevoegen data mannen en vrouwen
geslacht_dict = {'m': 'mannen', 'v': 'vrouwen'}
bmi_apache_data['KLEUR'] = bmi_apache_data['GESLACHT'].map({'m': '#0004FF', 'v': '#FF007C'})


################################################### WIDGET VAN DATA MAKEN #################################################################

# aantal mannen en vrouwen
indicator_aantal_mannen = pn.indicators.Number(name='Aantal mannen', value=afgerond_percentage_mannen, format='{value}%')
indicator_aantal_vrouwen = pn.indicators.Number(name='Aantal vrouwen', value=afgerond_percentage_vrouwen, format='{value}%')

# gemiddelde leeftijd van mannen, vrouwen en allebei samen
indicator_leeftijd = pn.indicators.Number(name='Gemiddelde leeftijd patienten', value=gemiddelde_leeftijd_patienten, format='{value} jaar')
indicator_leeftijd_mannen = pn.indicators.Number(name='Gemiddelde leeftijd mannelijke patienten', value=gemiddelde_leeftijd_mannelijke_patienten, format='{value} jaar')
indicator_leeftijd_vrouwen = pn.indicators.Number(name='Gemiddelde leeftijd vrouwelijke patienten', value=gemiddelde_leeftijd_vrouwelijke_patienten, format='{value} jaar')

# gemiddeld gewicht van mannen, vrouwen en allebei samen
indicator_gewicht = pn.indicators.Number(name='Gemiddeld gewicht patienten', value=gemiddelde_gewicht, format='{value} KG')
indicator_gewicht_mannen = pn.indicators.Number(name='Gemiddeld gewicht mannen', value=gemiddeld_gewicht_mannen, format='{value} KG')
indicator_gewicht_vrouwen = pn.indicators.Number(name='Gemiddeld gewicht vrouwen', value=gemiddeld_gewicht_vrouwen, format='{value} KG')

# gemiddelde lengte van mannen, vrouwen en allebei samen
indicator_lengte = pn.indicators.Number(name='Gemiddelde lengte patienten', value=gemiddelde_lengte, format='{value} m')
indicator_lengte_mannen = pn.indicators.Number(name='Gemiddelde lengte mannen', value=gemiddelde_lengte_mannen, format='{value} m')
indicator_lengte_vrouwen = pn.indicators.Number(name='Gemiddelde lengte vrouwen', value=gemiddelde_lengte_vrouwen, format='{value} m')

# Gauge widget van gemiddelde apache score
apache = pn.indicators.LinearGauge(name='Gem. apache IV score', value=gemiddelde_apache, bounds=(0, 100), format='{value} %', colors=[(0.25, '#009800'), (0.60, '#ffcf00'), (1, '#e00000')], show_boundaries=True)
apache_mannen = pn.indicators.LinearGauge(name='Gem. apache IV score mannen', value=gemiddelde_apache_mannen, bounds=(0, 100), format='{value} %', colors=[(0.25, 'green'), (0.60, 'gold'), (1, 'red')], show_boundaries=True)
apache_vrouwen = pn.indicators.LinearGauge(name='Gem. apache IV score vrouwen', value=gemiddelde_apache_vrouwen, bounds=(0, 100), format='{value} %', colors=[(0.25, 'green'), (0.60, 'gold'), (1, 'red')], show_boundaries=True)

# Gauge widget voor BMI
bmi = pn.indicators.Gauge(name='BMI patienten', value=gemiddelde_bmi_patienten, bounds=(10, 45), format='{value}', colors=[(0.265, '#000386'), (0.45, '#009800'), (0.56, '#ffcf00'), (0.72, '#fa7c00'), (1, '#e00000')])
bmi_mannen = pn.indicators.Gauge(name='BMI mannen', value=gemiddelde_bmi_mannen, bounds=(10, 45), format='{value}', colors=[(0.265, '#000386'), (0.45, '#009800'), (0.56, '#ffcf00'), (0.72, '#fa7c00'), (1, '#e00000')])
bmi_vrouwen = pn.indicators.Gauge(name='BMI vrouwen', value=gemiddelde_bmi_vrouwen, bounds=(10, 45), format='{value}', colors=[(0.265, '#000386'), (0.45, '#009800'), (0.56, '#ffcf00'), (0.72, '#fa7c00'), (1, '#e00000')])


########################################################### FUNCTIES #######################################################################

# pie chart geslacht patienten
def generate_pie_chart(aantal_mannen, aantal_vrouwen):
    """
    Genereert een taartdiagram voor de verdeling van mannen en vrouwen op de IC.

    Parameters:
    - aantal_mannen (int): Het aantal mannen.
    - aantal_vrouwen (int): Het aantal vrouwen.

    Returns:
    - plot (figure): Bokeh figuurobject met het taartdiagram.
    """
    
    # Data
    data = pd.Series([aantal_mannen, aantal_vrouwen], index=['Mannen', 'Vrouwen']).reset_index(name='value').rename(columns={'index': 'category'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi

    # kleuren
    data['color'] = ['#00003b', '#f7003b']

    # figuur
    p = figure(height=350, title="Verdeling mannen & vrouwen op IC", toolbar_location=None,
               tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0),
               background_fill_color="rgba(0, 0, 0, 0)", border_fill_color="rgba(0, 0, 0, 0)")

    # Plot
    source = ColumnDataSource(data)
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="black", fill_color='color', legend_field='category', source=source)

    # plot aanpassen
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p

# pie chart in een variabele zetten
pie_chart = generate_pie_chart(aantal_mannen, aantal_vrouwen)



# plot van gewichten maken
def generate_plot_gewicht(gemiddelde_gewicht, gemiddeld_gewicht_mannen, gemiddeld_gewicht_vrouwen):
    """
    Genereert een staafdiagram voor het gemiddelde gewicht van patiënten, mannen en vrouwen.

    Parameters:
    - gemiddelde_gewicht (float): Het totale gemiddelde gewicht.
    - gemiddeld_gewicht_mannen (float): Het gemiddelde gewicht van mannen.
    - gemiddeld_gewicht_vrouwen (float): Het gemiddelde gewicht van vrouwen.

    Returns:
    - plot (figure): Bokeh figuurobject met het staafdiagram.
    """
    categories = ['TOTAAL GEMIDDELDE', 'MANNEN', 'VROUWEN']
    values = [gemiddelde_gewicht, gemiddeld_gewicht_mannen, gemiddeld_gewicht_vrouwen]
    source = ColumnDataSource(data=dict(categorie=categories, gewicht=values))

    fill_colors = ['#a203a1', '#00003b', '#f7003b']

    color_mapper = factor_cmap(field_name='categorie', palette=fill_colors, factors=categories)

    p = figure(x_range=categories, height=350, title='Gemiddeld gewicht (KG)',
           toolbar_location=None, tools='', background_fill_color='rgba(0, 0, 0, 0)')

    bars = p.vbar(x='categorie', top='gewicht', width=0.9, source=source, line_color="rgba(0, 0, 0, 0)", fill_color=color_mapper)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1.2
    p.title.text_color = 'white'
    p.xaxis.axis_label_text_color = 'rgba(0, 0, 0, 0)'
    p.yaxis.axis_label_text_color = 'rgba(0, 0, 0, 0)'
    p.title.text_font_size = '14pt'

    hover = HoverTool()
    hover.tooltips = [("Categorie", "@categorie"), ("Gewicht", "@gewicht")]
    p.add_tools(hover)

    return p

gewicht_plot = generate_plot_gewicht(gemiddelde_gewicht, gemiddeld_gewicht_mannen, gemiddeld_gewicht_vrouwen)


# scatterplot van bmi en apache score maken
def bmi_scatterplot(gender_bmi='Beiden'):
    """
    Genereert een scatterplot van BMI versus Apache IV Score.

    Parameters:
    - gender_bmi (str): Het geslacht om te visualiseren ('BEIDEN', 'm', 'v').

    Returns:
    - plot (figure): Bokeh figuurobject met het scatterplot.
    """
    print(f"GESELECTEERDE GESLACHT: {gender_bmi}")

    if gender_bmi == 'Beiden':
        data_bmi = bmi_apache_data
    else:
        data_bmi = bmi_apache_data[bmi_apache_data['GESLACHT'].str.lower() == gender_bmi.lower()]

    source = ColumnDataSource(data_bmi)

    hover = HoverTool(tooltips=[
        ("Patient ID", "@PATIENT_ID"),
        ("Gewicht", "@GEWICHT"),
        ("Lengte", "@LENGTE"),
        ("Geslacht", "@GESLACHT"),
        ("BMI", "@BMI"),
        ("Apache IV Score", "@APACHE_IV_SCORE"),
    ])

    p = figure(
        title="BMI vs. Apache IV Score",
        x_axis_label="BMI",
        y_axis_label="Apache IV Score",
        tools=[hover, 'pan', 'wheel_zoom', 'reset']
    )

    scatter = p.scatter(x='BMI', y='APACHE_IV_SCORE', size=10, alpha=0.6, color='KLEUR', legend_field='GESLACHT', source=source)

    # legenda
    p.legend.click_policy = "hide"

    return p


# drop down om keuze te maken voor geslacht
gender_dropdown = pn.widgets.Select(name='Selecteer geslacht', options=['Beiden', 'm', 'v'], value='Beiden')

# pn.interact om scatterplot te updaten voor nieuwe keuze
bmi_scatterplot_dynamic = pn.interact(bmi_scatterplot, gender_bmi=gender_dropdown)


# GridSpec voor layout
grid = pn.GridSpec(sizing_mode='stretch_both', max_width=900)
gridbox = pn.GridBox(
    pn.pane.Markdown("## COVID-19 Data", styles={"color": "white", "font-size": "24px", "margin-bottom": "5px", "background": "#91C4E8"}),
    pn.pane.Markdown("In deze dashboard staan patient- en meetgegevens van COVID-19 patienten op de IC.", styles={"color": "black", "font-size": "16px", "margin-bottom": "5px", "background": "#91C4E8"}),
    pie_chart,
    indicator_aantal_mannen, indicator_aantal_vrouwen,
    indicator_leeftijd, indicator_leeftijd_mannen, indicator_leeftijd_vrouwen,
    gewicht_plot,
    indicator_gewicht, indicator_gewicht_mannen, indicator_gewicht_vrouwen,
    apache, apache_mannen, apache_vrouwen,
    bmi, bmi_mannen, bmi_vrouwen,
    bmi_scatterplot_dynamic,
    background="#D6F2FA",
    ncols=3, 
)

gridbox.show()
