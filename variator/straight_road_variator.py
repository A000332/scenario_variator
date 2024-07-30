"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.

    Example showing how to create two separate roads (that are not linked), hence adjust_roads_and_lanes will not be able to set the geometries without a similar approach.

    Some features used:

    - PlanView


"""

from scenariogeneration import xodr, prettyprint, ScenarioGenerator
import numpy as np
import os
import settings


class Scenario(ScenarioGenerator):
    def __init__(self, width, num_lane_left, num_lane_right):
        super().__init__()
        self.naming = "parameter"
        self.parameters["width"] = width
        self.parameters["num_lane_left"] = num_lane_left
        self.parameters["num_lane_right"] = num_lane_right

    def road(self, **kwargs):
        odr = xodr.OpenDrive("myroad")

        # ---------------- Road 1
        planview = xodr.PlanView(0, 0, 0)

        # create some geometries and add to the planview
        planview.add_geometry(xodr.Line(100))

        # create a solid roadmark
        rm = xodr.RoadMark(xodr.RoadMarkType.solid, 0.2)

        # create centerlane
        centerlane_1 = xodr.Lane(a=2)
        centerlane_1.add_roadmark(rm)
        lanesec_1 = xodr.LaneSection(0, centerlane_1)

        # add a driving lane
        for i in range(kwargs["num_lane_left"]):
            lane = xodr.Lane(a=kwargs["width"])
            lane.add_roadmark(rm)
            lanesec_1.add_left_lane(lane)

        for i in range(kwargs["num_lane_right"]):
            lane = xodr.Lane(a=kwargs["width"])
            lane.add_roadmark(rm)
            lanesec_1.add_right_lane(lane)

        ## finalize the road
        lanes_1 = xodr.Lanes()
        lanes_1.add_lanesection(lanesec_1)

        road = xodr.Road(1, planview, lanes_1)

        odr.add_road(road)

        # ------------------ Finalize
        odr.adjust_roads_and_lanes()

        return odr


if __name__ == "__main__":
    sce = Scenario(settings.width, settings.num_lane_left, settings.num_lane_right)
    # Print the resulting xml
    # prettyprint(sce.road().get_element())

    # write the OpenDRIVE file as xosc using current script name
    sce.generate("variator_generated")

    # uncomment the following lines to display the scenario using esmini
    from scenariogeneration import esmini
    # esmini(sce,os.path.join('esmini'))
