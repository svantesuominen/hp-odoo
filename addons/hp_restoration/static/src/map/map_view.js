import { registry } from "@web/core/registry";

import { MapArchParser } from "./map_arch_parser";
import { MapController } from "./map_controller";

export const mapView = {
    type: "map",
    ArchParser: MapArchParser,
    Controller: MapController,
    searchMenuTypes: ["filter", "groupBy", "favorite"],

    props(genericProps, view) {
        return {
            ...genericProps,
            archInfo: new view.ArchParser().parse(genericProps.arch),
        };
    },
};

registry.category("views").add("map", mapView);
