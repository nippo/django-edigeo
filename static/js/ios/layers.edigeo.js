IOS.ns('layers');

IOS.layers.edigeo = (function() {

    function getLayer() {
        var LieuditLayer = new OpenLayers.Layer.Vector(
            'Lieudits',
            {
                maxResolution: 10,
                strategies: [new OpenLayers.Strategy.BBOX()],
                protocol: new OpenLayers.Protocol.HTTP({
                    url: '/layers/edigeo/lieudits',
                    params: {},
                    format: new OpenLayers.Format.GeoJSON()
                }),
                visibility: true
            }
        );
        var LieuditLayer_style = new OpenLayers.Style({
            graphicOpacity : 1,
            strokeColor    : "#EEE979", // line
            fillColor      : "#EEE979",
            pointRadius    : 5,
            strokeWidth    : 0.3,
            strokeLinecap  : "butt",
            label          : "${gb_ident}",
            fontColor      : "#666",
            fillOpacity    : 0,
            fontSize       : 11
        });

        var LieuditLayer_style_selected = new OpenLayers.Style({
            fillOpacity    : 0.3,
            graphicOpacity : 1,
            strokeColor    : "#EEE979",
            fillColor      : "#EEE979",
            pointRadius    : 5,
            strokeWidth    : 0.8,
            strokeLinecap  : "butt"
        });

        var LieuditLayer_style_style = new OpenLayers.StyleMap({
            'default': LieuditLayer_style,
            'selected': LieuditLayer_style_selected,
        });

        LieuditLayer.styleMap = LieuditLayer_style;

        return LieuditLayer;
    };

    return {
        getLayer: getLayer
    };
})();
