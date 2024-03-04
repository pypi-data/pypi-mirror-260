Installation
=======

1. Installation von Python 
------------

``tscw_module`` ist eine Python Bibliothek. Python ist eine interpretierte, objektorientierte Hochsprache mit dynamischer Semantik.
Die integrierten Datenstrukturen, dynamische Typisierung und Bindung machen Python attraktiv für schnelle Anwendungsentwicklung
und als Skript- oder Klebesprache. Die einfache Syntax betont Lesbarkeit und reduziert Wartungskosten.
Python unterstützt Module und Pakete für Programmmodule und Code-Wiederverwendung.
Der Python-Interpreter und die Standardbibliothek sind kostenlos und plattformunabhängig verfügbar und kann über
`www.python.org/downloads/ <https://www.python.org/downloads/>`_ heruntergeladen werden. 
WICHTIG: Es wird empfohlen, bei der Installation die Option ``"Add python.exe" to PATH`` zu wählen. 
Dabei wird die ausführbare Datei nach der Installation in die PATH-Variable aufgenommen Python kann direkt von der Windows Konsole aufgerufen werden mit dem Befehl ``python`` aufgerufen werden.
Alternattiv kann Python auch später manuell in die Umgebungsvariable PATH aufnehmen (Admin-Rechte erforderlich).
Als Quelltext-Editor empfiehlt sich ``Visual Studio Code`` von Microsoft (kostenlos), welcher über `code.visualstudio.com/download/ <https://code.visualstudio.com/download>`_ 
heruntergeladen werden kann.


2. Installation des Moduls
------------

Zu dem gwünschten Arbeitsordner in der Windowskonsole wechseln:

.. code-block:: shell 

    $ cd $deinPfad 

Erstellung einer virtuellen Umgebung mit anschließender Aktivierung:

.. code-block:: shell 
    
    $ python -m venv .tscw_env
    $ .tscw_env\Scripts\activate

Installieren des ``tscw_module``:

.. code-block:: shell 
    
    $ pip install tscw_module

Im VS Code mit ``Str + P`` den Interpreter aufrufen und ``.tscw_env`` auswählen.


.. note::
    Falls VS Code zukünftig das ``tscw_module`` nicht erkennen sollte, wird empfohlen, den Interpreter in VS Code zu überprüfen.
    Zum installieren weiterer Packages via ``pip install`` muss die virtuelle Umgebung im entsprechen Pfad mit dem Befehl ``.tscw_env\Scripts\activate`` aktiviert werden.
    Zum Deaktivieren kann der Befehl ``deactivate`` benutzt werden.

.. note::
    `https://pypi.org/project/tscw-module/ <https://pypi.org/project/tscw-module/>`_ 
    
    `https://test.pypi.org/project/tscw-module/1.0.0/ <https://test.pypi.org/project/tscw-module/1.0.0/>`_ 