.. _upset-plots:

Upset Plots
===========

`Upset plots <https://en.wikipedia.org/wiki/UpSet_plot>`_ are used to visualise intersections between subsets of a dataset. They can be generated using the :py:func:`~isaricanalytics.visualisation.fig_upset` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.

.. figure:: ../../_static/plot_gallery/fig_upset.png
   :width: 100%
   :alt:   Upset plot
   :target: ../../_static/plot_gallery/fig_upset.html

The plot above was generated using a synthetic dataset of patient treatment complications for Dengue, consisting of five complications and their patient counts, as well counts for the intersections between the subsets of patients associated with the complications. **Click** the image to view the full interactive and fully annotated Plotly Go figure. Here is the dataset below as two tables, the first showing the complications and their patient counts, and the second showing the intersection subsets and their counts.

.. list-table:: Synthetic dataset of Dengue patient treatment complications - patient counts
   :header-rows: 1
   :widths: auto

   * - Complication
     - Patient Count
   * - Shock
     - 891
   * - Meningitis
     - 781
   * - Acute renal injury / acute renal failure
     - 757
   * - Cardiac arrest
     - 709
   * - Focal neurological signs
     - 702

The :py:func:`~isaricanalytics.visualisation.fig_upset` function expects a dataframe with the following columns (in no particular order):

.. todo::

   TODO

Provided your CSV contains these columns and is loaded into a valid Pandas dataframe, here are the Python steps you need to generate the plot above using the :py:func:`~isaricanalytics.visualisation.fig_upset` function:

.. code:: python

   import pandas as pd
   from isaricanalytics.visualisation import fig_upset
   # Load the CSV data from a string buffer
   counts = pd.read_csv(io.StringIO(
       """index,count,short_label,label\n
          compl_shock,891,Shock ,Shock \n
          compl_meningitis,781,Meningitis,Meningitis\n
          compl_acuterenal,757,Acute renal injury / acute renal failure,Acute renal injury / acute renal failure\n
          compl_cardiarrest,709,Cardiac arrest,Cardiac arrest\n
          compl_focalneuro,702,Focal neurological signs,Focal neurological signs\n
       """
   ), skipinitialspace=True)
   intersections = pd.read_csv(io.StringIO(
       """
       index,label,count
       "('compl_shock', 'compl_meningitis', 'compl_acuterenal', 'compl_cardiarrest', 'compl_focalneuro')","('Shock ', 'Meningitis', 'Acute renal injury / acute renal failure', 'Cardiac arrest', 'Focal neurological signs')",256
       "('compl_shock', 'compl_meningitis', 'compl_acuterenal', 'compl_cardiarrest')","('Shock ', 'Meningitis', 'Acute renal injury / acute renal failure', 'Cardiac arrest')",121
       "('compl_shock', 'compl_meningitis', 'compl_acuterenal', 'compl_focalneuro')","('Shock ', 'Meningitis', 'Acute renal injury / acute renal failure', 'Focal neurological signs')",115
       "('compl_shock', 'compl_meningitis', 'compl_cardiarrest', 'compl_focalneuro')","('Shock ', 'Meningitis', 'Cardiac arrest', 'Focal neurological signs')",86
       "('compl_shock', 'compl_acuterenal', 'compl_cardiarrest', 'compl_focalneuro')","('Shock ', 'Acute renal injury / acute renal failure', 'Cardiac arrest', 'Focal neurological signs')",67
       "('compl_shock', 'compl_meningitis', 'compl_focalneuro')","('Shock ', 'Meningitis', 'Focal neurological signs')",37
       "('compl_shock', 'compl_acuterenal', 'compl_cardiarrest')","('Shock ', 'Acute renal injury / acute renal failure', 'Cardiac arrest')",37
       "('compl_shock', 'compl_acuterenal', 'compl_focalneuro')","('Shock ', 'Acute renal injury / acute renal failure', 'Focal neurological signs')",34
       "('compl_shock', 'compl_meningitis', 'compl_cardiarrest')","('Shock ', 'Meningitis', 'Cardiac arrest')",31
       "('compl_shock', 'compl_meningitis', 'compl_acuterenal')","('Shock ', 'Meningitis', 'Acute renal injury / acute renal failure')",30
       "('compl_meningitis', 'compl_acuterenal', 'compl_cardiarrest', 'compl_focalneuro')","('Meningitis', 'Acute renal injury / acute renal failure', 'Cardiac arrest', 'Focal neurological signs')",30
       "('compl_shock', 'compl_cardiarrest', 'compl_focalneuro')","('Shock ', 'Cardiac arrest', 'Focal neurological signs')",26
       "('compl_meningitis', 'compl_acuterenal', 'compl_focalneuro')","('Meningitis', 'Acute renal injury / acute renal failure', 'Focal neurological signs')",18
       "('compl_shock', 'compl_meningitis')","('Shock ', 'Meningitis')",15
       "('compl_meningitis', 'compl_acuterenal', 'compl_cardiarrest')","('Meningitis', 'Acute renal injury / acute renal failure', 'Cardiac arrest')",15
       "('compl_shock', 'compl_acuterenal')","('Shock ', 'Acute renal injury / acute renal failure')",14
       "('compl_shock', 'compl_cardiarrest')","('Shock ', 'Cardiac arrest')",11
       "('compl_shock', 'compl_focalneuro')","('Shock ', 'Focal neurological signs')",9
       "('compl_meningitis', 'compl_cardiarrest', 'compl_focalneuro')","('Meningitis', 'Cardiac arrest', 'Focal neurological signs')",8
       "('compl_meningitis', 'compl_acuterenal')","('Meningitis', 'Acute renal injury / acute renal failure')",7
       "('compl_meningitis', 'compl_cardiarrest')","('Meningitis', 'Cardiac arrest')",6
       "('compl_acuterenal', 'compl_cardiarrest', 'compl_focalneuro')","('Acute renal injury / acute renal failure', 'Cardiac arrest', 'Focal neurological signs')",6
       "('compl_acuterenal', 'compl_cardiarrest')","('Acute renal injury / acute renal failure', 'Cardiac arrest')",5
       "('compl_meningitis', 'compl_focalneuro')","('Meningitis', 'Focal neurological signs')",3
       "('compl_meningitis',)","('Meningitis',)",3
       "('compl_cardiarrest', 'compl_focalneuro')","('Cardiac arrest', 'Focal neurological signs')",3
       "('compl_shock',)","('Shock ',)",2
       "('compl_acuterenal', 'compl_focalneuro')","('Acute renal injury / acute renal failure', 'Focal neurological signs')",2
       "('compl_focalneuro',)","('Focal neurological signs',)",2
       "('compl_cardiarrest',)","('Cardiac arrest',)",1
       """
   ))
   # Create and display the figure
   fig = fig_upset(
       data,
       title="Upset Plot of Synthetic Dengue Patient Treatment Complications",
       height=380
   )
   fig.show()

You should see the plot appearing as given above.

.. note::

   Any dataframe or CSV column names, or dictionary field labels, in the example
   above, must be as given, otherwise the function will throw an exception or
   return unexpected data. Also, the ``height`` parameter, which is optional
   with a default of ``350``, can be used to customise the plot height. Refer
   to the :py:func:`~isaricanalytics.visualisation.fig_frequency_chart` function
   docstring for more information.
