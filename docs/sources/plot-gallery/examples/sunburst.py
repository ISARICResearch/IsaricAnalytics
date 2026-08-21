"""
Sunburst Plots
==============
"""

# %%
# Sunburst plots, also known as `ring charts <https://en.wikipedia.org/wiki/Pie_chart#Ring_chart,_sunburst_chart,_and_multilevel_pie_chart>`_, can be generated using the :py:func:`~isaricanalytics.visualisation.fig_sunburst` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
# The plot below was generated using a synthetic dataset of patient enrolment data organised by site and country.
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/sunburst.csv` file).
#
# .. list-table:: Patient enrolment at clinical sites by country and site
#   :header-rows: 1
#   :widths: auto
#
#   * - Site ID
#     - Country
#     - Patient Enrolment Count
#   * - 0
#     - COL
#     - 21
#   * - 2
#     - COL
#     - 25
#   * - 3
#     - GBR
#     - 199
#   * - 5
#     - CAN
#     - 31
#   * - 6
#     - BRA
#     - 156
#   * - 7
#     - BRA
#     - 27
#   * - 8
#     - BRA
#     - 8
#   * - 9
#     - FRA
#     - 174
#   * - 10
#     - POL
#     - 89
#   * - 11
#     - POL
#     - 30
#   * - 13
#     - RWA
#     - 121
#   * - 14
#     - KEN
#     - 1
#   * - 15
#     - KEN
#     - 15
#   * - 16
#     - KEN
#     - 1
#   * - 18
#     - NLD
#     - 102
#
# Here are the Python steps you need to generate the plot using the :py:func:`~isaricanalytics.visualisation.fig_sunburst` function:
import pandas as pd
from isaricanalytics.visualisation import fig_sunburst

# Load the CSV
data = pd.read_csv("./csv/sunburst.csv")

# Create and display the figure
fig = fig_sunburst(
    data,
    title="Sunburst Plot of Synthetic Patient Enrolment Data Organised by Site and Country",
    path=["Country", "Site"],
    values="SubjectID",
)
fig.update_layout(autosize=True)
fig

# %%
#
# .. note::
#
#    Any dataframe or CSV column names, or dictionary field labels, in the
#    example above that are not specific to the dataset must be as given,
#    otherwise the function may throw an exception or return an incorrect figure.
#
#    The figure height and width parameters can be set using the ``height``
#    and ``width`` parameters, but it may be more convenient to let Plotly handle
#    this using the figure layout `autosize <https://plotly.com/python/reference/layout/#layout-autosize>`_
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_sunburst`
#    function docstring for more information.
