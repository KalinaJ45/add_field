# -*- coding: utf-8 -*-

from qgis.core import QgsField, NULL
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QVariant


class Worker(QObject):
    """ Worker for to assigning objects of the selected shapefile layer to individual objects of the second layer, within which these objects are located.
    """
    finished = pyqtSignal()  # create a pyqtSignal for when task is finished
    progress = pyqtSignal(int)
    error = pyqtSignal()

    def __init__(self, first_layer, first_temporary_layer, second_temporary_layer, name_of_new_field, name_of_selected_field):
        """Constructor.

        Args:
            first_layer (QgsVectorLayer): first selected vector layer.
            first_temporary_layer (QgsVectorLayer): firdt created temporary vector layer.
            second_temporary_layer QgsVectorLayer): second temporary vector layer.
            name_of_new_field (str): name of first layer created field.
            name_of_selected_field (str): name of second layer selected field.
        """
        QObject.__init__(self)
        self.first_layer = first_layer
        self.first_temporary_layer = first_temporary_layer
        self.second_temporary_layer = second_temporary_layer
        self.name_of_new_field = name_of_new_field
        self.name_of_selected_field = name_of_selected_field

    def run(self):
        """Runs worker.
        """
        self.progress.emit(0)  # reset progressbar
        vpr = self.first_layer.dataProvider()
        vpr.addAttributes([QgsField(self.name_of_new_field, QVariant.String)])
        self.first_layer.updateFields()
        objects_of_first_temporary_layer = [
            obiect for obiect in self.first_temporary_layer.getFeatures()]
        objects_of_second_temporary_layer = [
            obiect for obiect in self.second_temporary_layer.getFeatures()]
        objects_of_first_layer = [
            obiect for obiect in self.first_layer.getFeatures()]
        self.first_layer.startEditing()
        try:
            for i, object_of_first_temporary_layer in enumerate(objects_of_first_temporary_layer):
                for j, object_of_second_temporary_layer in enumerate(objects_of_second_temporary_layer):
                    if object_of_second_temporary_layer.geometry().intersects(object_of_first_temporary_layer.geometry()):
                        if object_of_second_temporary_layer.geometry().contains(object_of_first_temporary_layer.geometry()):
                            objects_of_first_layer[object_of_first_temporary_layer.id(
                            )-1][self.name_of_new_field] = object_of_second_temporary_layer[self.name_of_selected_field]
                        elif objects_of_first_layer[object_of_first_temporary_layer.id()-1][self.name_of_new_field] == NULL:
                            objects_of_first_layer[object_of_first_temporary_layer.id(
                            )-1][self.name_of_new_field] = object_of_second_temporary_layer[self.name_of_selected_field]
                        else:
                            objects_of_first_layer[object_of_first_temporary_layer.id()-1][self.name_of_new_field] = str(
                                objects_of_first_layer[object_of_first_temporary_layer.id()-1][self.name_of_new_field])+" / " + str(object_of_second_temporary_layer[self.name_of_selected_field])
                        self.first_layer.updateFeature(
                            objects_of_first_layer[object_of_first_temporary_layer.id()-1])
                self.progress.emit(
                    round((i+1)*(100/self.first_temporary_layer.featureCount())))
        except:
            self.error.emit()
        self.finished.emit()
