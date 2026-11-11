import { Component, onMounted, onWillStart, onWillUnmount, onWillUpdateProps, signal, t, useProps } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { CogMenu } from "@web/search/cog_menu/cog_menu";
import { Layout } from "@web/search/layout";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { useSearchBarToggler } from "@web/search/search_bar/search_bar_toggler";
import { useSetupAction } from "@web/search/action_hook";
import { standardViewProps } from "@web/views/standard_view_props";

import { divIcon, latLngBounds, layerGroup, map, marker, tileLayer } from "../lib/leaflet/leaflet-src.esm.js";

const MAP_FIELDS = ["display_name", "code", "name", "latitude", "longitude", "city_id", "stage_id", "area_ha"];

export class MapController extends Component {
    static template = "hp_restoration.MapView";
    static components = { Layout, SearchBar, CogMenu };
    props = useProps({
        ...standardViewProps,
        archInfo: t.object(),
    });

    setup() {
        this.orm = useService("orm");
        this.rootRef = signal.ref();
        this.mapRef = signal.ref();
        this.located = signal(0);
        this.total = signal(0);
        this.records = [];
        useSetupAction({ rootRef: this.rootRef });
        this.searchBarToggler = useSearchBarToggler();
        onWillStart(() => this.loadRecords(this.props));
        onWillUpdateProps(async (nextProps) => {
            await this.loadRecords(nextProps);
            this.drawMarkers();
        });
        onMounted(() => this.initMap());
        onWillUnmount(() => {
            this.resizeObserver?.disconnect();
            this.leafletMap?.remove();
        });
    }

    get note() {
        if (!this.total()) {
            return String(_t("No sites match this search."));
        }
        return String(_t(
            "%s of %s sites have coordinates",
            this.located(),
            this.total(),
        ));
    }

    async loadRecords(props) {
        const { latitude, longitude } = props.archInfo;
        const rows = await this.orm.searchRead(props.resModel, props.domain, MAP_FIELDS, {
            context: props.context,
            limit: 10000,
        });
        this.records = rows.filter((row) => row[latitude] && row[longitude]);
        this.total.set(rows.length);
        this.located.set(this.records.length);
    }

    initMap() {
        const container = this.mapRef();
        this.leafletMap = map(container, { scrollWheelZoom: true });
        tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(this.leafletMap);
        this.markerLayer = layerGroup().addTo(this.leafletMap);
        this.leafletMap.setView([64.5, 26], 5);
        this.drawMarkers();
        this.resizeObserver = new ResizeObserver(() => this.leafletMap.invalidateSize());
        this.resizeObserver.observe(container);
    }

    drawMarkers() {
        if (!this.markerLayer) {
            return;
        }
        const { latitude, longitude } = this.props.archInfo;
        this.markerLayer.clearLayers();
        const groups = new Map();
        for (const record of this.records) {
            const key = `${record[latitude].toFixed(5)}:${record[longitude].toFixed(5)}`;
            if (!groups.has(key)) {
                groups.set(key, []);
            }
            groups.get(key).push(record);
        }
        const bounds = [];
        for (const sites of groups.values()) {
            const count = sites.length;
            const pin = marker([sites[0][latitude], sites[0][longitude]], {
                icon: divIcon({
                    className: "hp-map-pin",
                    html: count > 1 ? String(count) : "",
                    iconSize: count > 1 ? [22, 22] : [14, 14],
                    iconAnchor: count > 1 ? [11, 11] : [7, 7],
                }),
            });
            pin.bindPopup(this.popupElement(sites));
            pin.on("popupopen", (event) => {
                for (const button of event.popup.getElement().querySelectorAll(".hp-map-popup-name")) {
                    button.addEventListener("click", () => {
                        this.openRecord(Number(button.dataset.id));
                    });
                }
            });
            pin.addTo(this.markerLayer);
            bounds.push([sites[0][latitude], sites[0][longitude]]);
        }
        if (bounds.length) {
            this.leafletMap.fitBounds(latLngBounds(bounds), { padding: [40, 40], maxZoom: 11 });
        } else {
            this.leafletMap.setView([64.5, 26], 5);
        }
    }

    popupElement(sites) {
        const root = document.createElement("div");
        root.className = "hp-map-popup";
        for (const site of sites) {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "btn btn-link p-0 d-block text-start hp-map-popup-name";
            button.dataset.id = site.id;
            button.textContent = site.name || site.code || site.display_name;
            const meta = document.createElement("div");
            meta.className = "text-muted small mb-2";
            const bits = [site.code, site.city_id && site.city_id[1], site.stage_id && site.stage_id[1]].filter(Boolean);
            if (site.area_ha) {
                bits.push(`${site.area_ha.toFixed(2)} ha`);
            }
            meta.textContent = bits.join(" · ");
            root.append(button, meta);
        }
        return root;
    }

    openRecord(resId) {
        this.props.selectRecord?.(resId, { activeIds: this.records.map((record) => record.id) });
    }
}
