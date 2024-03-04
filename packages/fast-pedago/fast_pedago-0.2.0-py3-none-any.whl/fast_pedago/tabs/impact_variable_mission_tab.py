# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago.tabs.impact_variable_inputs_tab import (
    FLIGHT_DATA_FILE_SUFFIX,
)
from fast_pedago.dropdowns import get_select_multiple_sizing_process_dropdown
from fast_pedago.buttons import get_multiple_process_selection_info_button


class ImpactVariableMissionTab(widgets.VBox):
    def __init__(self, working_directory_path: str, **kwargs):

        super().__init__(**kwargs)

        self.working_directory_path = working_directory_path
        self.sizing_process_to_display = []

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = (
            get_select_multiple_sizing_process_dropdown()
        )
        self.info_button = get_multiple_process_selection_info_button()

        self.selection_and_info_box = widgets.HBox()
        self.selection_and_info_box.children = [
            self.output_file_selection_widget,
            self.info_button,
        ]

        self.selection_and_info_box.layout = widgets.Layout(
            width="98%",
            height="6%",
            justify_content="space-between",
            align_items="flex-start",
        )

        self.output_display = widgets.Output()

        def display_graph(change):

            # First check if there are any sizing process to add to the display of if we need to
            # clear them
            if change["new"] == "None":
                self.sizing_process_to_display = []

            elif change["new"] not in self.sizing_process_to_display:
                self.sizing_process_to_display.append(change["new"])

            with self.output_display:

                clear_output()

                mission_viewer = oad.MissionViewer()

                for sizing_process_to_add in self.sizing_process_to_display:

                    path_to_output_folder = pth.join(
                        self.working_directory_path, "outputs"
                    )
                    path_to_flight_data_file = pth.join(
                        path_to_output_folder,
                        sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                    )

                    mission_viewer.add_mission(
                        path_to_flight_data_file, sizing_process_to_add
                    )

                if self.sizing_process_to_display:

                    mission_viewer.display()

        self.output_file_selection_widget.observe(display_graph, names="value")

        self.children = [self.selection_and_info_box, self.output_display]
