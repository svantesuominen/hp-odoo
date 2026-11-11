export class MapArchParser {
    parse(xmlDoc) {
        return {
            latitude: xmlDoc.getAttribute("latitude") || "latitude",
            longitude: xmlDoc.getAttribute("longitude") || "longitude",
        };
    }
}
