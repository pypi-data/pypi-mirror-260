# Copyright 2023-2024 Parker Owan.  All rights reserved.

import corolab


class CLProjectContainer:
    """Manages basic access to the corolab project objects"""

    def __init__(self):
        self._project = corolab.Project()
        self._viewer = corolab.WorkspaceViewer()

    def viewer(self) -> corolab.WorkspaceViewer:
        return self._viewer

    def project(self) -> corolab.Project:
        return self._project

    def newProject(self):
        self._project = corolab.Project()

    def rebuildViewer(self):
        self._viewer.setProject(self._project)
        self._viewer.render()
