/*jslint browser: true*/
/*global $, jQuery, IOS, L*/

IOS.ns('l.edigeo.map');

IOS.l.edigeo.map.lieudits = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/lieudit',
            property: 'gb_indent'
        },
        geojson = function geojson() {
            var layer = L.geoJson('', {
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

IOS.l.edigeo.map.parcelles = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/parcelle',
            property: 'gb_indent'
        },
        geojson = function geojson() {
            var layer = L.geoJson('', {
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
