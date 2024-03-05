# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtCore import Qt, QPoint
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QHeaderView, QMenu, QAction

import corolab

from corolab_app.container import CLProjectContainer
from corolab_app.editor.table import CLPropertyTable


class CLProjectTree(QTreeView):

    def __init__(self, container: CLProjectContainer, table: CLPropertyTable):
        super(CLProjectTree, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self._container = container
        self._table = table
        self.setStyleSheet("""
            QHeaderView::section {
                padding: 5px;                               
                height: 12px;                                
                border: none;
                background-color: rgb(219, 220, 232);
                font: bold 11px;
                color: rgb(42, 44, 46);
                border-top: 1px solid rgb(250, 250, 250);
                border-bottom: 1px solid rgb(250, 250, 250);
                border-right: none;
                border-left: 2px solid rgb(250, 250, 250);
            }

            QWidget {
                font: 12px;
                color: rgb(42, 44, 46);
            }
        """)
        self._model = QStandardItemModel()
        self.setModel(self._model)
        self.updateProjectTreeContent()
        self._active_item = None

        self.clicked.connect(self.handleSelection)
        self.customContextMenuRequested.connect(self.handleCustomContextMenu)

    def updateProjectTreeContent(self):
        self._model.clear()
        self._model.setColumnCount(2)
        self._model.setHorizontalHeaderLabels(["Item", "Type"])
        root_item = self._model.invisibleRootItem()

        # Build the workspace
        workspace_item = QStandardItem("Workspace")
        workspace_item.setColumnCount(2)
        root_item.appendRow(workspace_item)
        workspace = self._container.project().workspace()
        for key in workspace.getRobots():
            node = workspace.getRobot(key)
            self.addNode(workspace_item, node)
        for key in workspace.getEffectors():
            node = workspace.getEffector(key)
            self.addNode(workspace_item, node)
        for key in workspace.getItems():
            node = workspace.getItem(key)
            self.addNode(workspace_item, node)
        for key in workspace.getCameras():
            node = workspace.getCamera(key)
            self.addNode(workspace_item, node)
        for key in workspace.getFiducials():
            node = workspace.getFiducial(key)
            self.addNode(workspace_item, node)
        for key in workspace.getTaskRegions():
            node = workspace.getTaskRegion(key)
            self.addNode(workspace_item, node)

        # Build the behaviors
        behaviors_item = QStandardItem("Behaviors")
        behaviors_item.setColumnCount(2)
        root_item.appendRow(behaviors_item)
        for behavior in self._container.project().programs().values():
            self.addBehavior(behaviors_item, behavior)

        # Build the variables
        variables_item = QStandardItem("Variables")
        variables_item.setColumnCount(2)
        root_item.appendRow(variables_item)
        variables = self._container.project().variables()
        for variable in variables.getVariables().values():
            self.addVariable(variables_item, variable)

        # Build the models
        # models_items = QStandardItem("Models")
        # models_items.setColumnCount(2)
        # root_item.appendRow(models_items)

        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.expandAll()

    def addNode(self, parent: QStandardItem, node: corolab.Node):
        item_name = CLProjectItem(text=node.name(), item=node)
        item_type = CLProjectItem(text=node.type(), item=node)
        # self.setIcon(item=item_name)
        for child in node._getChildren():
            self.addNode(item_name, node=child)
        parent.appendRow([item_name, item_type])

    def addBehavior(self, parent: QStandardItem, behavior: corolab.Behavior):
        item_name = CLProjectItem(text=behavior.name(), item=behavior)
        item_type = CLProjectItem(text=behavior.type(), item=behavior)
        # self.setIcon(item=item_name)
        for child in behavior._behaviors():
            self.addBehavior(item_name, behavior=child)
        parent.appendRow([item_name, item_type])

    def addVariable(self, parent: QStandardItem, variable: corolab.Variable):
        item_name = CLProjectItem(text=variable.name(), item=variable)
        item_type = CLProjectItem(text=variable.type(), item=variable)
        parent.appendRow([item_name, item_type])

    def handleSelection(self, index: int):
        tree_item = self._model.itemFromIndex(index)
        if self._active_item and isinstance(self._active_item, corolab.Node):
            self._active_item.showBoundingBox(show=False)
        if type(tree_item) == CLProjectItem:
            self._active_item = tree_item.item()
            if isinstance(self._active_item, corolab.Node):
                self._active_item.showBoundingBox(show=True)
            self._table.populate(item=self._active_item)
        else:
            self._table.reset()
        self._container.viewer().render()

    def handleCustomContextMenu(self, point: QPoint):
        index = self.indexAt(point)
        if not index.isValid():
            return
        tree_item = self._model.itemFromIndex(index)
        context_menu = CLContextMenu(tree_item=tree_item)
        context_menu.exec_(self.viewport().mapToGlobal(point))
        self._container.rebuildViewer()
        self.updateProjectTreeContent()
        self._table.reset()


class CLProjectItem(QStandardItem):

    def __init__(self, text: str, item: corolab.WithProperties):
        super().__init__()
        self._item = item
        self.setEditable(False)
        self.setText(text)

    def item(self) -> corolab.WithProperties:
        return self._item

    def type(self) -> str:
        return self._item.type()


class CLContextMenu(QMenu):

    def __init__(self, tree_item: CLProjectItem):
        super().__init__()
        self.setStyleSheet("""
            QMenu {
                background-color: rgb(250, 250, 250);
                color: rgb(42, 44, 46);
                border: 1px rgb(228, 229, 241);
                margin: 0px;
                width: 120px;
            }

            QMenu::item {
                background-color: transparent;
            }

            QMenu::item:selected {
                background-color: rgb(186, 219, 245);
            }
            """)

        if type(tree_item) != CLProjectItem:
            return

        item = tree_item.item()

        if isinstance(item, corolab.Variable):
            # self.addAction("Rename")
            self.addAction(self._createDeleteAction(item=item))

        elif isinstance(tree_item.item(), corolab.Behavior):
            # self.addAction("Rename")
            self.addAction(self._createDeleteAction(item=item))
            # self.addAction("Change Parent")
            self.addAction(self._createMoveUpAction(behavior=item))
            self.addAction(self._createMoveDownAction(behavior=item))

        elif isinstance(tree_item.item(), corolab.Node):
            # self.addAction("Rename")
            self.addAction(self._createDeleteAction(item=item))
            # self.addAction("Change Parent")

    # This isn't quite right, WithProperties doesn't have a delete() routine
    def _createDeleteAction(self, item: corolab.WithProperties) -> QAction:
        action = QAction("Delete", parent=self)
        action.triggered.connect(item.delete)
        return action

    def _createMoveUpAction(self, behavior: corolab.Behavior) -> QAction:
        action = QAction("Move Up", parent=self)
        action.triggered.connect(behavior.moveUp)
        return action

    def _createMoveDownAction(self, behavior: corolab.Behavior) -> QAction:
        action = QAction("Move Down", parent=self)
        action.triggered.connect(behavior.moveDown)
        return action
