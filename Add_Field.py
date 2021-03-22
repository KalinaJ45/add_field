# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Add_Field
                                 A QGIS plugin
 ffff
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-20
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Kalina Juszczyk
        email                : kalina.juszczyk@wp.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import *
from PyQt5.QtCore import QVariant, QFileInfo
from os import path
from xlrd import open_workbook
from os import path

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Add_Field_dialog import Add_FieldDialog
import os.path


class Add_Field:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Add_Field_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Add_Field')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Add_Field', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Add_Field/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Add_Field'),
                action)
            self.iface.removeToolBarIcon(action)




    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = Add_FieldDialog()

        selectedLayer1=None
        selectedLayer2=None

       
        def clearForm():
            self.dlg.selectLayerGroupBox.setEnabled(True)
            self.dlg.inputBtn1.setEnabled(True)
            self.dlg.inputBtn2.setEnabled(False)
            self.dlg.nameFile1.clear()
            self.dlg.nameFile2.clear()
            self.dlg.addFieldGroupBox.setEnabled(False)
            self.dlg.nameNewField.clear()
            self.dlg.fieldComboBox.clear()

        clearForm()

        def selectLayer1():
            global selectedLayer1
            selectedShapefile = QFileDialog.getOpenFileName(None, "Wybierz plik shp", "", "Shapefile (*.shp)")

            if len(selectedShapefile[0])==0:
                msg=QMessageBox.critical(None,"Wybierz plik shapefile",'Nie wybrano pliku shapefile!')
            else:
                self.dlg.nameFile1.setText(selectedShapefile[0])
                selectedLayer1 = QgsVectorLayer(selectedShapefile[0], "Wybrana warstwa1", "ogr")
                crs = QgsCoordinateReferenceSystem('EPSG:2180')
                selectedLayer1.setCrs(crs)
                QgsProject.instance().addMapLayers([selectedLayer1])
                self.dlg.inputBtn1.setEnabled(False)
                self.dlg.inputBtn2.setEnabled(True)

            

        def selectLayer2():
            global selectedLayer2
            selectedShapefile = QFileDialog.getOpenFileName(None, "Wybierz plik shp", "", "Shapefile (*.shp)")
            if len(selectedShapefile[0])==0:
                msg=QMessageBox.critical(None,"Wybierz plik shapefile",'Nie wybrano pliku shapefile!')
            else:
                self.dlg.nameFile2.setText(selectedShapefile[0])
                selectedLayer2 = QgsVectorLayer(selectedShapefile[0], "Wybrana warstwa2", "ogr")
                crs = QgsCoordinateReferenceSystem('EPSG:2180')
                selectedLayer2.setCrs(crs)
                QgsProject.instance().addMapLayers([selectedLayer2])
                self.dlg.selectLayerGroupBox.setEnabled(False)
                self.dlg.addFieldGroupBox.setEnabled(True)
                self.dlg.myProgressBar.setEnabled(False)
                fields =  selectedLayer2.fields()
                fieldnames = [field.name() for field in fields]
                self.dlg.fieldComboBox.addItems(fieldnames)
                self.dlg.fieldComboBox.setCurrentIndex(-1)
               

        def allocate(layer1,layer2,nameField1,nameField2, start, step, stop):
            self.dlg.myProgressBar.setValue(start)
            layer1.isValid()
            vpr = layer1.dataProvider()
            vpr.addAttributes([QgsField(nameField1, QVariant.String)])
            layer1.updateFields()
            feats_L = [ feat for feat in layer2.getFeatures() ]
            feats_SL = [ feat for feat in layer1.getFeatures() ]
            layer1.startEditing()
            
            for i, feat in enumerate(feats_L):
                for j, feat2 in enumerate(feats_SL):
                    if feat.geometry().intersects(feat2.geometry()):
                        if feat.geometry().contains(feat2.geometry()):
                            feat2[nameField1]=feat[nameField2]
                        elif feat2[nameField1]==NULL:
                            feat2[nameField1]=feat[nameField2]
                        else:
                            feat2[nameField1]= str(feat2[nameField1])+" / "+ str(feat[nameField2])    
                    
                        layer1.updateFeature(feat2)
                
                self.dlg.myProgressBar.setValue(start+(i+1)*(100/step))
            
            self.dlg.myProgressBar.setValue(stop)
            clearForm()
               
        def deleteField():
            global selectedLayer1
            fields = selectedLayer1.fields()
            fieldnames = [field.name() for field in fields]
            selectedLayer1.deleteAttribute((len(fieldnames)-1))

        def allocate_field():
            if self.dlg.nameNewField.text()!="" and self.dlg.fieldComboBox.currentIndex()!=-1:
                self.dlg.myProgressBar.setEnabled(True)
                global selectedLayer1
                global selectedLayer2
                feats_count = selectedLayer2.featureCount()
            
                allocate(selectedLayer1,selectedLayer2,self.dlg.nameNewField.text(),self.dlg.fieldComboBox.currentText(), 0, feats_count,100)
    
                msg = QMessageBox.question(None, 'Zakończ edycję', 'Czy zapisać zmiany w warstwie?', QMessageBox.Yes | QMessageBox.No| QMessageBox.Cancel)
                    
                if msg == QMessageBox.Yes:
                    selectedLayer1.commitChanges()
                    
                if msg == QMessageBox.No:
                    deleteField()                    
                    selectedLayer1.commitChanges() 
                    selectedLayer1.rollBack()  
                    
                self.dlg.myProgressBar.setValue(0)
                self.dlg.myProgressBar.setEnabled(False)
                self.dlg.addFieldGroupBox.setEnabled(False)

           
            elif self.dlg.nameNewField.text()=="":
                msg=QMessageBox.critical(None,"Nadaj nazwę pola",'Nie nadano nazwy nowemu polu!') 
            elif self.dlg.fieldComboBox.currentIndex()==-1:
                msg=QMessageBox.critical(None,"Wybierz pole z listy",'Nie wybrano pola z listy!')
            
             
        

        def close():
            #clearForm()
            self.dlg.close()
          
        self.dlg.allocateObjectsBtn.clicked.connect(allocate_field)
        self.dlg.inputBtn1.clicked.connect(selectLayer1)
        self.dlg.inputBtn2.clicked.connect(selectLayer2)
        self.dlg.closeBtn.clicked.connect(close)
        self.dlg.clearBtn.clicked.connect(clearForm)

        # show the dialog 
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
