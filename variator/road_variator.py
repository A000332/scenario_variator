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
import settings


class Scenario(ScenarioGenerator):
    def __init__(self, settings):
        super().__init__()
        self.naming = "parameter"
        self.parameters["width"] = settings.width
        self.parameters["num_lane_left"] = settings.num_lane_left
        self.parameters["num_lane_right"] = settings.num_lane_right
        self.parameters["start_road_grad"] = settings.start_road_grad
        self.parameters["start_road_cant"] = settings.start_road_cant
        self.is_clothoid = settings.is_clothoid
        if(self.is_clothoid):
            self.parameters["mig_interval"] = settings.mig_interval
            self.parameters["curv"] = settings.curv
            self.parameters["third_road_height"] = settings.third_road_height
            self.parameters["third_road_grad"] = settings.third_road_grad
            self.parameters["third_road_cant"] = settings.third_road_cant

    def road(self, **kwargs):
        odr = xodr.OpenDrive("myroad")

        start_road = xodr.create_road(
            xodr.Line(50), 0, left_lanes=kwargs["num_lane_left"], right_lanes=kwargs["num_lane_right"], lane_width=kwargs["width"]
        )
        start_road.add_elevation(0, 0, kwargs["start_road_grad"], 0, 0)
        start_road.add_superelevation(0, 0, kwargs["start_road_cant"], 0, 0)

        odr.add_road(start_road)

        if(self.is_clothoid):
            second_road = xodr.create_road(
                xodr.Spiral(0.00001, kwargs["curv"], kwargs["mig_interval"]), 1, left_lanes=kwargs["num_lane_left"], right_lanes=kwargs["num_lane_right"], lane_width=kwargs["width"]
            )
            third_road = xodr.create_road(
                xodr.Arc(kwargs["curv"], 50), 2, left_lanes=kwargs["num_lane_left"], right_lanes=kwargs["num_lane_right"], lane_width=kwargs["width"]
            )
            third_road.add_elevation(0, kwargs["third_road_height"], kwargs["third_road_grad"], 0, 0)
            third_road.add_superelevation(0, 0, kwargs["third_road_cant"], 0, 0)

            odr.add_road(second_road)
            odr.add_road(third_road)
            start_road.add_successor(xodr.ElementType.road, 1, xodr.ContactPoint.start)
            second_road.add_predecessor(xodr.ElementType.road, 0, xodr.ContactPoint.end)
            second_road.add_successor(xodr.ElementType.road, 2, xodr.ContactPoint.start)
            third_road.add_predecessor(xodr.ElementType.road, 1, xodr.ContactPoint.end)

        # adjust roads and lanes
        odr.adjust_roads_and_lanes()

        # adjust the remaining elevations
        odr.adjust_elevations()

        # adjust the roadmarks
        odr.adjust_roadmarks()

        return odr


if __name__ == "__main__":
    sce = Scenario(settings)
    # Print the resulting xml
    # prettyprint(sce.road().get_element())

    # write the OpenDRIVE file as xosc using current script name
    sce.generate("variator_generated")

    # uncomment the following lines to display the scenario using esmini
    from scenariogeneration import esmini
    # esmini(sce,os.path.join('esmini'))
