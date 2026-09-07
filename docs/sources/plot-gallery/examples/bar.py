"""
Bar Charts
==========
"""

# %%
# Ordinary `bar charts <https://en.wikipedia.org/wiki/Bar_chart>`_ can be generated using the :py:func:`~isaricanalytics.visualisation.fig_bar_chart` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
# The plot below was generated using a synthetic dataset of cumulative patient enrolment data for a clinical site.
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/bar.csv` file).
#
# .. list-table:: Cumulative patient enrolment at a clinical site between January and June, 2026
#   :header-rows: 1
#   :widths: auto
#
#   * - Month-Year
#     - Cumultative Patient Enrolment
#   * - January 2026
#     - 2
#   * - February 2026
#     - 10
#   * - March 2026
#     - 60
#   * - April 2026
#     - 80
#   * - May 2026
#     - 95
#   * - June 2026
#     - 100
#
# Here are the Python steps you need to generate the plot using the :py:func:`~isaricanalytics.visualisation.fig_bar_chart` function:
import pandas as pd
from isaricanalytics.visualisation import fig_bar_chart

# Load the CSV
data = pd.read_csv("./csv/bar.csv")

# Create and display the figure
fig = fig_bar_chart(
    data,
    title="Bar Chart of Cumulative Patient Enrolment",
    xlabel="Month-Year",
    ylabel="Cumulative Patients Enrolled",
    index_column="month_year"
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
