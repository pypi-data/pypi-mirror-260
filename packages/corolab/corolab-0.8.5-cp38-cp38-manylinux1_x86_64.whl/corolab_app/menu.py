# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtWidgets import QMainWindow

TAB_BAR_HEIGHT = 70

from corolab_app.actions import CLActions

# TODO: Remove the little box
# See: https://doc.qt.io/qt-6/stylesheet-examples.html#customizing-qmenu
MENU_BAR_STYLE_SHEET = """
    QMenu::icon:checked {
        border: none;
        background: none;
    }

    QMenu::icon:unchecked {
        border: none;
        background: none;
    }
"""


class CLMenuBar:

    def __init__(self, window: QMainWindow, actions: CLActions):
        menu_bar = window.menuBar()
        menu_bar.setNativeMenuBar(True)
        menu_bar.setStyleSheet(MENU_BAR_STYLE_SHEET)

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(actions.new_action)
        file_menu.addAction(actions.open_action)
        file_menu.addSeparator()
        templates = file_menu.addMenu("Open Template")
        for template_action in actions.open_templates:
            templates.addAction(template_action)
        file_menu.addSeparator()
        file_menu.addAction(actions.save_action)
        file_menu.addAction(actions.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(actions.quit_action)

        edit_menu = menu_bar.addMenu("Edit")
        robots = edit_menu.addMenu("Robot")
        # TODO: Add support to create CustomRobot
        robots.addAction(actions.add_franka_panda_robot)
        robots.addAction(actions.add_ur3e_robot)
        robots.addAction(actions.add_ur5e_robot)
        robots.addAction(actions.add_ur10e_robot)
        effectors = edit_menu.addMenu("Effector")
        effectors.addAction(actions.add_tool_frame)
        effectors.addAction(actions.add_robotiq_2f85)
        effectors.addAction(actions.add_franka_hand)
        items = edit_menu.addMenu("Item")
        items.addAction(actions.add_task_region)
        items.addAction(actions.add_custom_item)
        items.addAction(actions.add_desk)
        cameras = edit_menu.addMenu("Camera")
        cameras.addAction(actions.add_visual_marker)
        cameras.addAction(actions.add_realsense_d435i)
        cameras.addAction(actions.add_realsense_d405)
        edit_menu.addSeparator()
        for key, value in actions.add_behaviors.items():
            behaviors = edit_menu.addMenu(key)
            for action in value:
                behaviors.addAction(action)
        edit_menu.addSeparator()
        variables = edit_menu.addMenu("Variable")
        for action in actions.add_variables:
            variables.addAction(action)

        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(actions.view_logging_bar_action)
        view_menu.addAction(actions.view_project_tree_action)
        view_menu.addAction(actions.view_property_table_action)
        view_menu.addSeparator()
        view_menu.addAction(actions.reset_viewer_action)
        view_menu.addAction(actions.save_screenshot_action)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(actions.help_tutorials_action)
        help_menu.addSeparator()
        help_menu.addAction(actions.about_action)
        # TODO: Need to add YouTube Channel
        # TODO: Seperator
        # TODO: Need to add Report Issue
        # TODO: Need to add Check for Software Update
        # TODO: Seperator
        # TODO: Need to add License
