/*jslint browser: true*/
/*global $, jQuery, IOS, L, map*/

IOS.ns('l.edigeo.map');

IOS.l.edigeo.map.lieudits = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/lieudit',
            property: 'gb_ident'
        },
        geojson = function geojson() {
            var layer = L.geoJson('', {
                    style: function (feature) {

                        return {weight: 1, opacity: 0.4, color: '#F4EFA8'};
                    },
                    onEachFeature: function onEachFeature(feature, layer) {
                        if (feature.properties && feature.properties[config.property]) {
                            layer.bindPopup(feature.properties[config.property]);
                        }
                    }
                }),
                legend;
            $.getJSON(config.url, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: geojson
    };
}());

IOS.l.edigeo.map.parcels = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/parcel'
        },
        geojson = function geojson() {
            var layer,
                legend;
            layer = L.geoJson('', {
                style: function (feature) {

                    return {weight: 1, opacity: 0.4, color: '#F4EFA8'};
                },
                onEachFeature: function onEachFeature(feature, layer) {
                    if (feature.properties && feature.properties.idu) {
                        layer.bindPopup(feature.properties.idu + ' ' + feature.properties.supf);
                    }
                },
                filter: function (feature, layer) {

                    return map.getBounds().contains(L.geoJson(feature).getBounds());
                }
            });

            $.getJSON(config.url, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: geojson
    };
}());
