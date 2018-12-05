from PyQt5.QtCore import QAbstractListModel, QModelIndex


class MissionsListModel(QAbstractListModel):
    def __init__(self):
        super(MissionsListModel, self).__init__()
        self.ListItemData = []

    def data(self, QModelIndex, role=None):
        pass

    def addItem(self, itemData):
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        del self.ListItemData[index]

    def getItem(self, index):
        if (index > -1) and (index < len(self.ListItemData)):
            return self.ListItemData[index]