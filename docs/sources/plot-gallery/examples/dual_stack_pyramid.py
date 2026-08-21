"""
Dual Stack Pyramid Plots
========================
"""

# %%
# `Population pyramid <https://en.wikipedia.org/wiki/Population_pyramid>`_ plots can be generated using the :py:func:`~isaricanalytics.visualisation.fig_dual_stack_pyramid` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
#
# The plot below was generated using a synthetic dataset of a patient population with subgroups indicating outcome (Death, Discharged, Censored).
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/dual_stack_pyramid.csv` file).
#
# .. list-table:: Patient population distribution by age group, sex and outcome
#    :header-rows: 1
#    :widths: auto
#
#    * - Age Group
#      - Sex
#      - Outcome
#      - Number
#    * - 0-5
#      - Male
#      - death
#      - 1
#    * - 0-5
#      - Male
#      - censored
#      - 19
#    * - 0-5
#      - Female
#      - discharged
#      - 29
#    * - 0-5
#      - Female
#      - death
#      - 3
#    * - 0-5
#      - Female
#      - censored
#      - 21
#    * - 5-10
#      - Male
#      - discharged
#      - 27
#    * - 5-10
#      - Male
#      - death
#      - 4
#    * - 5-10
#      - Male
#      - censored
#      - 19
#    * - 5-10
#      - Female
#      - discharged
#      - 29
#    * - 5-10
#      - Female
#      - death
#      - 1
#    * - 5-10
#      - Female
#      - censored
#      - 19
#    * - 10-15
#      - Male
#      - discharged
#      - 33
#    * - 10-15
#      - Male
#      - death
#      - 1
#    * - 10-15
#      - Male
#      - censored
#      - 18
#    * - 10-15
#      - Female
#      - discharged
#      - 30
#    * - 10-15
#      - Female
#      - death
#      - 1
#    * - 10-15
#      - Female
#      - censored
#      - 20
#    * - 15-20
#      - Male
#      - discharged
#      - 32
#    * - 15-20
#      - Male
#      - death
#      - 1
#    * - 15-20
#      - Male
#      - censored
#      - 17
#    * - 15-20
#      - Female
#      - discharged
#      - 27
#    * - 15-20
#      - Female
#      - death
#      - 9
#    * - 15-20
#      - Female
#      - censored
#      - 18
#    * - 20-25
#      - Male
#      - discharged
#      - 36
#    * - 20-25
#      - Male
#      - death
#      - 1
#    * - 20-25
#      - Male
#      - censored
#      - 23
#    * - 20-25
#      - Female
#      - discharged
#      - 30
#    * - 20-25
#      - Female
#      - death
#      - 7
#    * - 20-25
#      - Female
#      - censored
#      - 17
#    * - 25-30
#      - Male
#      - discharged
#      - 37
#    * - 25-30
#      - Male
#      - death
#      - 4
#    * - 25-30
#      - Male
#      - censored
#      - 19
#    * - 25-30
#      - Female
#      - discharged
#      - 31
#    * - 25-30
#      - Female
#      - death
#      - 8
#    * - 25-30
#      - Female
#      - censored
#      - 19
#    * - 30-35
#      - Male
#      - discharged
#      - 39
#    * - 30-35
#      - Male
#      - death
#      - 9
#    * - 30-35
#      - Male
#      - censored
#      - 17
#    * - 30-35
#      - Female
#      - discharged
#      - 34
#    * - 30-35
#      - Female
#      - death
#      - 11
#    * - 30-35
#      - Female
#      - censored
#      - 17
#    * - 35-40
#      - Male
#      - discharged
#      - 41
#    * - 35-40
#      - Male
#      - death
#      - 12
#    * - 35-40
#      - Male
#      - censored
#      - 25
#    * - 35-40
#      - Female
#      - discharged
#      - 36
#    * - 35-40
#      - Female
#      - death
#      - 5
#    * - 35-40
#      - Female
#      - censored
#      - 19
#    * - 40-45
#      - Male
#      - discharged
#      - 39
#    * - 40-45
#      - Male
#      - death
#      - 13
#    * - 40-45
#      - Male
#      - censored
#      - 19
#    * - 40-45
#      - Female
#      - discharged
#      - 33
#    * - 40-45
#      - Female
#      - death
#      - 9
#    * - 40-45
#      - Female
#      - censored
#      - 18
#    * - 45-50
#      - Male
#      - discharged
#      - 42
#    * - 45-50
#      - Male
#      - death
#      - 10
#    * - 45-50
#      - Male
#      - censored
#      - 19
#    * - 45-50
#      - Female
#      - discharged
#      - 40
#    * - 45-50
#      - Female
#      - death
#      - 12
#    * - 45-50
#      - Female
#      - censored
#      - 27
#    * - 50-55
#      - Male
#      - discharged
#      - 39
#    * - 50-55
#      - Male
#      - death
#      - 13
#    * - 50-55
#      - Male
#      - censored
#      - 20
#    * - 50-55
#      - Female
#      - discharged
#      - 45
#    * - 50-55
#      - Female
#      - death
#      - 9
#    * - 50-55
#      - Female
#      - censored
#      - 28
#    * - 55-60
#      - Male
#      - discharged
#      - 41
#    * - 55-60
#      - Male
#      - death
#      - 17
#    * - 55-60
#      - Male
#      - censored
#      - 26
#    * - 55-60
#      - Female
#      - discharged
#      - 46
#    * - 55-60
#      - Female
#      - death
#      - 17
#    * - 55-60
#      - Female
#      - censored
#      - 24
#    * - 60-65
#      - Male
#      - discharged
#      - 41
#    * - 60-65
#      - Male
#      - death
#      - 16
#    * - 60-65
#      - Male
#      - censored
#      - 28
#    * - 60-65
#      - Female
#      - discharged
#      - 49
#    * - 60-65
#      - Female
#      - death
#      - 20
#    * - 60-65
#      - Female
#      - censored
#      - 29
#    * - 65-70
#      - Male
#      - discharged
#      - 41
#    * - 65-70
#      - Male
#      - death
#      - 22
#    * - 65-70
#      - Male
#      - censored
#      - 28
#    * - 65-70
#      - Female
#      - discharged
#      - 49
#    * - 65-70
#      - Female
#      - death
#      - 21
#    * - 65-70
#      - Female
#      - censored
#      - 22
#    * - 70-75
#      - Male
#      - discharged
#      - 50
#    * - 70-75
#      - Male
#      - death
#      - 23
#    * - 70-75
#      - Male
#      - censored
#      - 25
#    * - 70-75
#      - Female
#      - discharged
#      - 43
#    * - 70-75
#      - Female
#      - death
#      - 23
#    * - 70-75
#      - Female
#      - censored
#      - 25
#    * - 75-80
#      - Male
#      - discharged
#      - 47
#    * - 75-80
#      - Male
#      - death
#      - 18
#    * - 75-80
#      - Male
#      - censored
#      - 28
#    * - 75-80
#      - Female
#      - discharged
#      - 54
#    * - 75-80
#      - Female
#      - death
#      - 24
#    * - 75-80
#      - Female
#      - censored
#      - 33
#    * - 80-85
#      - Male
#      - discharged
#      - 55
#    * - 80-85
#      - Male
#      - death
#      - 26
#    * - 80-85
#      - Male
#      - censored
#      - 33
#    * - 80-85
#      - Female
#      - discharged
#      - 54
#    * - 80-85
#      - Female
#      - death
#      - 21
#    * - 80-85
#      - Female
#      - censored
#      - 25
#    * - 85-90
#      - Male
#      - discharged
#      - 54
#    * - 85-90
#      - Male
#      - death
#      - 28
#    * - 85-90
#      - Male
#      - censored
#      - 33
#    * - 85-90
#      - Female
#      - discharged
#      - 52
#    * - 85-90
#      - Female
#      - death
#      - 24
#    * - 85-90
#      - Female
#      - censored
#      - 33
#    * - 90-95
#      - Male
#      - discharged
#      - 55
#    * - 90-95
#      - Male
#      - death
#      - 26
#    * - 90-95
#      - Male
#      - censored
#      - 27
#    * - 90-95
#      - Female
#      - discharged
#      - 52
#    * - 90-95
#      - Female
#      - death
#      - 28
#    * - 90-95
#      - Female
#      - censored
#      - 29
#    * - 96-100
#      - Male
#      - discharged
#      - 52
#    * - 96-100
#      - Male
#      - death
#      - 31
#    * - 96-100
#      - Male
#      - censored
#      - 37
#    * - 96-100
#      - Female
#      - discharged
#      - 58
#    * - 96-100
#      - Female
#      - death
#      - 33
#    * - 96-100
#      - Female
#      - censored
#      - 36
#
# The :py:func:`~isaricanalytics.visualisation.fig_dual_stack_pyramid` function expects a dataframe with the following columns (in no particular order):
#
# * ``"y_axis"`` - the age group label
# * ``"side"`` - the sex
# * ``"stack_group"`` - the patient outcome
# * ``"value"`` - the number of patients in the category (combination of age group, sex, outcome)
# * ``"left_side"`` - a boolean to indicate where the value should appear, with ``1`` indicating left and ``0`` indicating right
#
# Here are the Python steps required to generate the plot, where males are on the left and females are on the right, using the :py:func:`~isaricanalytics.visualisation.fig_dual_stack_pyramid` function:
import io, pandas as pd
from isaricanalytics.visualisation import fig_dual_stack_pyramid

# Load the CSV
data = pd.read_csv("./csv/dual_stack_pyramid.csv")

# Create and display the figure
fig = fig_dual_stack_pyramid(
  data=data,
  title="Population Pyramid Plot of Synthetic Patient Dataset",
  xlabel="Count",
  ylabel="Age Group",
  base_color_map={
      "discharged": "#00c26f",
      "death": "#df0069",
      "censored": "#fff500"
  },
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
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_dual_stack_pyramid`
#    function docstring for more information.
