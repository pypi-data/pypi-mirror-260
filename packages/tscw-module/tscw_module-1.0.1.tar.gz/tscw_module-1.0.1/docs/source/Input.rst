TSCW - INPUT - Erstellung
=====

Felddaten
------------

Um eine Felddaten-Datei zu erstellen, muss die Klasse ``GacaFieldData`` erstellt und mit Daten belegt werden.


0. Importiere benötigte Module:
~~~~~~~~~~

.. code-block:: python
   :linenos:

   import numpy as np
   from tscw_module import GacaFieldData, GacaProcessData
   import matplotlib.pyplot as plt

1. Initialisiere **GacaFieldData**:
~~~~~~~~~~

.. code-block:: python
   :linenos:

   n_boreholes        = 1         
   n_fluid            = 1         
   delta_z            = 122.5    # [m] Dicke vertikal Schicht (äquidistant)
   tvd_max_borehole   = 4*122.5  # [m] RS lzRT ()
   medium_type_cavern = 'GAS'    # 
   medium_id_cavern   = 'Nordverbundgas' # Name der Substanz, welche in TSCW/Stoffwerte/Bibliothek definiert wurde

   # Initialisiere GacaFieldData Class
   Gaca_field = GacaFieldData(n_boreholes,n_fluid,tvd_max_borehole,delta_z, \
                              medium_type_cavern,medium_id_cavern)


2. Definition der radialen Stützstellen um das Bohrloch:
~~~~~~~~~~
Die radialen Stützstellen werden in diesem Beispiel in dem array ``radial_vector_borehole`` definiert.
Die Unterteilung sollte so erfolgen, dass alle revelanten Installationselemente in radialer Richtung erfasst werden.

.. code-block:: python
   :linenos:

   radial_vector_borehole = np.array([0.0942, 0.1095, 0.1372, 0.1492, 0.2, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]) # [m]
    # Manuell werden beliebig viele Sützstellen mit Agregatzuständen beleget.
    # Die restlichen sind automatisch 'SOLID'
   Gaca_field.add_boreholeVector(radial_vector_borehole,['FLUID','SOLID'])
    # OPTIONAL: Kommentare der jeweiligen Stütztstelle beginnend ab dem ersten Element.
   Gaca_field.add_radialComment(['GAS','STAHL','RRSF','STAHL','ZEM','Gebirge---->'])

3. Definition der Materialeigenschaften um das Bohrloch:
~~~~~~~~~~

Geometrisch besteht das Bohrlochmodell aus einer Matrix, welche sich aus ``Gaca_field.p_borehole`` Zeilen und ``Gaca_field.m_borehole`` Spalten besteht.
Diese müssen nun mit Stoffwerten versehen werden über die Funktion ``add_materialProperty`` hinzugefügt werden.

.. code-block:: python
   :linenos:

   # Material Properties
   Gaca_field.add_materialProperty(0,250,  # jeweils UK von Start und Ende angeben (range)
                                 np.array([0.0000, 3.6000, 4.2000, 3.6000, 1.6000, 1.9200, 1.9200,   # heat_capacity * rho  [MJ/(m3K)]
                                             1.9200, 1.9200, 1.9200, 1.9200, 1.9200, 1.9200, 1.9200]), 
                                 np.array([0.000, 50.000, 0.500, 50.000, 1.000, 2.330, 2.330,        # thermal_conductivity [W/(m K)]
                                             2.330, 2.330, 2.330, 2.330, 2.330, 2.330, 2.330]),'Schicht 1') # Name

   Gaca_field.add_materialProperty(350,500,
                                 np.array([0.0000, 3.6000, 4.2000, 3.6000, 1.6000, 1.9500, 1.9500,
                                             1.9500, 1.9500, 1.9500, 1.9500, 1.9500, 1.9500, 1.9500]),
                                 np.array([0.000, 50.000, 0.500, 50.000, 1.000, 5.500, 5.500,
                                             5.500, 5.500, 5.500, 5.500, 5.500, 5.500, 5.500]), 'Schicht 2' )

4. Temperatur und Neigung des Bohrlochs
~~~~~~~~~~

.. code-block:: python

   temparature_bh = np.transpose(np.tile(np.array([8, 12, 17, 22]),(Gaca_field.m_borehole, 1)))
   Gaca_field.add_temperature(temparature_bh,'borehole')
   Gaca_field.add_boreholeInclination('vertical')

5. Kaverneneigenschaften
~~~~~~~~~~

.. code-block:: python
   :linenos:

   rad_kav           = 30.3      # radius
   v_kav             = 464366    # Volumen
   # Höhe des Zylinders, wenn das Volumen aus einem Zylinder mit zwei aufgesetzten Halbkugel approximiert wird.
   h                 = (v_kav - 4/3*np.pi*rad_kav**3) / (np.pi*rad_kav**2) 
   density_salt                 = 2170     # [kg/m3]
   specific_heat_capacity_salt  = 900      # [J/(kg*K)]
   heat_conductivity_salt       = 5.5      # [W/(m*K)]
   height_cavern                = h + 2*rad_kav   # [m]
   volume_brine_equivalent      = 30000      # [m3]
   radius_brine_level           = rad_kav    # [m]
   refdepth_cavern              = tvd_max_borehole     # [m] RS
   temperature_brine_equivalent = None # 30
   pressure_cavern              =  9.8       # [MPa]


   # radiale Stützstellen in der Kaverne
   radial_vector_cavern   = np.array([rad_kav, 35.18, 39.51, 43.85, 48.19, 52.52, 56.86, 61.19,
                                    65.53, 69.87, 74.23, 78.54, 82.88, 87.22, 91.56, 95.90, 
                                    100.24, 104.58, 109.92, 113.26, 117.60, 121.90, 126.24,
                                    135.00, 140.00, 145.00, 150.00])
   
   # temperatur
   temparature_cav = np.array([22.00]*radial_vector_cavern.shape[0])   # const temperature


   # Füge die Daten der Klasse hinzu
   Gaca_field.add_cavernVector(radial_vector_cavern)
   Gaca_field.add_temperature(temparature_cav,'cavern')
   Gaca_field.add_cavernCharacteristics(refdepth_cavern, density_salt, specific_heat_capacity_salt,heat_conductivity_salt,
                                       height_cavern, volume_brine_equivalent, radius_brine_level,pressure_cavern, temperature_brine_equivalent)


6. Export 
~~~~~~~~~~

.. code-block:: python
   :linenos:

   save_folder     = r'L:\Projekte\SG-UBT\40_Thermodynamik\TSCW_GACA_Bernburg\Gruppe1'
   project_name    = 'BB_Bb122'
   Gaca_field.export_fieldData(save_folder,project_name, True)

Beim exportieren wird in der Konsole folgendes angezeigt:

.. code-block:: shell

   Run sucessfull
   L:\Projekte\SG-UBT\40_Thermodynamik\TSCW_GACA_Bernburg\Gruppe1\BB_Gruppe1_Bb122\BB_Gruppe1_Bb122_gaca.fd.txt
   Backend TkAgg is interactive backend. Turning interactive mode on.
   Exported L:\Projekte\SG-UBT\40_Thermodynamik\TSCW_GACA_Bernburg\Gruppe1\BB_Gruppe1_Bb122\BB_Gruppe1_Bb122_fd.pickle


Die Felddaten-Datei ``BB_Gruppe1_Bb122_gaca.fd.txt`` ist:

.. code-block:: shell

   NUMBER_BOREHOLES	1
   N_FLUID	1
   M_BOREHOLE	14	# (M)
   P_BOREHOLE	4	# (P)
   DL	122.5000	# [m]
   M_CAVERN	27	# (MK)
   MEDIUM_TYPE_CAVERN	GAS
   MEDIUM_ID_CAVERN	Nordverbundgas
   DEPTH_CAVERN	490.00	# Referenztiefe fuer Druck

   RADIAL_VECTOR_BOREHOLE # [m]
   #GAS	STAHL	RRSF	STAHL	ZEM	Gebirge---->
   0.0942	0.1095	0.1372	0.1492	0.2000	0.5000	1.0000	2.0000	4.0000	8.0000	16.0000	32.0000	64.0000	128.0000

   COLUMN_CHARACTER_BOREHOLE # [/] der Radialelemente um die Bohrung (M Werte)
   FLUID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID

   HEAT_CAPACITY_BOREHOLE # [MJ/(K*m3)]  Dichte * spez. Waermekapazitaet der Radialelemente um die Bohrung (P*M Werte)
   #GAS	STAHL	RRSF	STAHL	ZEM	Gebirge---->
   0.000	3.600	4.200	3.600	1.600	1.920	1.920	1.920	1.920	1.920	1.920	1.920	1.920	1.920	# UK 122.50m - Schicht 1
   0.000	3.600	4.200	3.600	1.600	1.920	1.920	1.920	1.920	1.920	1.920	1.920	1.920	1.920	# UK 245.00m - Schicht 1
   0.000	3.600	4.200	3.600	1.600	1.950	1.950	1.950	1.950	1.950	1.950	1.950	1.950	1.950	# UK 367.50m - Schicht 2
   0.000	3.600	4.200	3.600	1.600	1.950	1.950	1.950	1.950	1.950	1.950	1.950	1.950	1.950	# UK 490.00m - Schicht 2


   THERMAL_CONDUCTIVITY_BOREHOLE # [W/(m*K)]  Waermeleitfaehigkeit der Radialelemente um die Bohrung (P*M Werte)
   #GAS	STAHL	RRSF	STAHL	ZEM	Gebirge---->
   0.000	50.000	0.500	50.000	1.000	2.330	2.330	2.330	2.330	2.330	2.330	2.330	2.330	2.330	# UK 122.50m - Schicht 1
   0.000	50.000	0.500	50.000	1.000	2.330	2.330	2.330	2.330	2.330	2.330	2.330	2.330	2.330	# UK 245.00m - Schicht 1
   0.000	50.000	0.500	50.000	1.000	5.500	5.500	5.500	5.500	5.500	5.500	5.500	5.500	5.500	# UK 367.50m - Schicht 2
   0.000	50.000	0.500	50.000	1.000	5.500	5.500	5.500	5.500	5.500	5.500	5.500	5.500	5.500	# UK 490.00m - Schicht 2


   TEMPERATURE_BOREHOLE  # [deg C] Temperatur der Radialelemente um die Bohrung (P*M Werte)
   #GAS	STAHL	RRSF	STAHL	ZEM	Gebirge---->
   8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	# UK 122.50m - Schicht 1
   12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	# UK 245.00m - Schicht 1
   17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	# UK 367.50m - Schicht 2
   22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	# UK 490.00m - Schicht 2


   WELL_VERTICALITY  # [deg] Winkel zwischen Bohrlochachse und Bohrung (P Werte)
   0.000	# UK 122.50m - Schicht 1
   0.000	# UK 245.00m - Schicht 1
   0.000	# UK 367.50m - Schicht 2
   0.000	# UK 490.00m - Schicht 2


   RADIAL_VECTOR_CAVERN # [m] (MK Werte)
   30.3000	35.1800	39.5100	43.8500	48.1900	52.5200	56.8600	61.1900	65.5300	69.8700	74.2300	78.5400	82.8800	87.2200	91.5600	95.9000	100.2400	104.5800	109.9200	113.2600	117.6000	121.9000	126.2400	135.0000	140.0000	145.0000	150.0000

   TEMPERATURE_CAVERN  #  [deg C] Temperatur der Radialelemente um die Kaverne (MK Werte) 
   22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000	22.0000

   DENSITY_SALT	2170.00	#[kg/m3]
   SPECIFIC_HEAT_CAPACITY_SALT	900.00	#[J/(kg*K)]
   HEAT_CONDUCTIVITY_SALT	5.50	#[W/(m*K)]
   HEIGHT_CAVERN	181.20	#[m]
   VOLUME_BRINE_EQUIVALENT	30000.00	#[m3]
   RADIUS_BRINE_LEVEL	30.30	#[m]
   PRESSURE_CAVERN	9.80	#[MPa] at DEPTH_CAVERN 490.00m


``BB_Gruppe1_Bb122_fd.pickle`` ist eine Binär-Datei der exportieren Felddatenklasse.
Sie kann mit dem Befehl in ein anderes Skript geladen werden.

.. code-block:: python
   :linenos:

   import pickle
   with open(field_data_picklePath, 'rb') as f:
      field_data = pickle.load(f)

6. Geometrie QC 
~~~~~~~~~~

Es empfiehlt sich, vor dem Starten der Simulation die erstellte txt-Datei zu kontrollieren.
Außerdem kann die Geometrie mit folgendem Befehl geplottet werden:

.. code-block:: python
   :linenos:

      Gaca_field.plot_geometry([0, 0.5]) # radial range
      plt.show()

.. image:: Geometry_HeatCapactiyRho.png
  :width: 700
  :alt: Geometry_HeatCapactiyRho.png


.. image:: Geometry_ThermalConductivity.png
  :width: 700
  :alt: Geometry_ThermalConductivity.png



Prozessdaten
----------------


Für die Prozessdaten wird die Klasse  ``GacaProcessData`` erstellt und mit Daten belegt.

1. Initialisierung 
~~~~~~~~~~

.. code-block:: python
   :linenos:

   coupled_annuli  = [1]
   medium_type     = ['GAS']
   medium_id       = [medium_id_cavern]
   description     = 'Gasspeicher Bernburg Bbg 122 Ausspeisung'
   PD_Ausspeisung  = GacaProcessData(description, coupled_annuli, medium_type, medium_id)

2. Hinzufügen von Etappen
~~~~~~~~~~

Etappen können chronologisch hinzugefügt werden.
Dies hat den Vorteil, dass beispielsweise treppenstufige Aus- oder Einspeisungen in for-loops zu der Klasse hinzugefügt werden können (siehe unten).
Beim Export der Klasse werden die Etappen automatisch nummeriert und formatiert.
Wichtig ist dass die Parameter in einer 'dict' Klasse erstellt werden und die Schlüsselnamen den Parameternamen aus dem Handbuch entsprechen.
Siehe dafür die Dokumentation von :py:func:add_stage

.. code-block:: python
   :linenos:

   # Initialisiere Parameter Dictionary
   ausspeisung_param = {
   'TERMINATION_ID': 6,    
   'TERMINATION_QUANTITY': None,
   'DT_MAX': 1,
   'FLOW_RATE': None,
   'K_S': 0.2 ,
   'P_BOUNDARY_CONDITION': 'CAVERN',
   'BOUNDARY_PRESSURE': 0,
   'T_BOUNDARY_CONDITION': 'CAVERN',
   'BOUNDARY_TEMPERATURE': 0
   }

   flow_rate_array            = np.array([2e5, 1.5e5, 1e5, 0.75e5, 0.3e5])  # verschiedene Raten
   termination_quantity_array = np.array([9.5, 7.5,6.31,6.03,1.1])          # verschiedene min. Drücke


   for flow_rate, termination_quantitiy in zip(flow_rate_array,termination_quantity_array): # for Schleife 
      ausspeisung_param['FLOW_RATE']            = flow_rate
      ausspeisung_param['TERMINATION_QUANTITY'] = termination_quantitiy
      PD_Ausspeisung.add_stage(ausspeisung_param)

2. Export
~~~~~~~~~~

.. code-block:: python
   :linenos:

   save_folder     = r'L:\Projekte\SG-UBT\40_Thermodynamik\TSCW_GACA_Bernburg\Gruppe1'
   project_name    = 'BB_Bb122'
   PD_Ausspeisung.export_processData(save_folder,project_name)
   

In der Konsole wird folgendes angezeigt:

.. code-block:: shell

   L:\Projekte\SG-UBT\40_Thermodynamik\TSCW_GACA_Bernburg\Gruppe1\BB_Gruppe1\Ausspeisung\Bb122_gaca.pd.txt
   Run sucessfull

Die entsprechende Prozessdatei hat folgende Gestalt:

.. code-block:: shell

   DESCRIPTION	Gasspeicher Bernburg Bbg 122 Ausspeisung
   N_FLUID	1
   NUMBER_OF_STAGES [/]	5

   MEDIUM_TYPE
   GAS

   MEDIUM_ID
   Nordverbundgas

   COUPLED_ANNULI	# [integer required!]
   1



   # ++++++++++++++++++++++++++++++++
   STAGE	1

   TERMINATION_ID	6
   TERMINATION_QUANTITY	9.50
   DT_MAX	1
   FLOW_RATE	200000.00
   K_S	0.20
   P_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_PRESSURE	0
   T_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_TEMPERATURE	0

   # ++++++++++++++++++++++++++++++++
   STAGE	2

   TERMINATION_ID	6
   TERMINATION_QUANTITY	7.50
   DT_MAX	1
   FLOW_RATE	150000.00
   K_S	0.20
   P_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_PRESSURE	0
   T_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_TEMPERATURE	0

   # ++++++++++++++++++++++++++++++++
   STAGE	3

   TERMINATION_ID	6
   TERMINATION_QUANTITY	6.31
   DT_MAX	1
   FLOW_RATE	100000.00
   K_S	0.20
   P_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_PRESSURE	0
   T_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_TEMPERATURE	0

   # ++++++++++++++++++++++++++++++++
   STAGE	4

   TERMINATION_ID	6
   TERMINATION_QUANTITY	6.03
   DT_MAX	1
   FLOW_RATE	75000.00
   K_S	0.20
   P_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_PRESSURE	0
   T_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_TEMPERATURE	0

   # ++++++++++++++++++++++++++++++++
   STAGE	5

   TERMINATION_ID	6
   TERMINATION_QUANTITY	1.10
   DT_MAX	1
   FLOW_RATE	30000.00
   K_S	0.20
   P_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_PRESSURE	0
   T_BOUNDARY_CONDITION	CAVERN

   BOUNDARY_TEMPERATURE	0

.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:

.. .. py:function:: lumache.get_random_ingredients(kind=None)

..    Return a list of random ingredients as strings.

..    :param kind: Optional "kind" of ingredients.
..    :type kind: list[str] or None
..    :return: The ingredients list.
..    :rtype: list[str]


..    Creating recipes
.. ----------------

.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:

.. .. py:function:: lumache.get_random_ingredients(kind=None)

..    Return a list of random ingredients as strings.

..    :param kind: Optional "kind" of ingredients.
..    :type kind: list[str] or None
..    :return: The ingredients list.
..    :rtype: list[str]


..    .. py:exception:: lumache.InvalidKindError

..    Raised if the kind is invalid.