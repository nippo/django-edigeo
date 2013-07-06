/*jslint browser: true*/
/*global $, jQuery, IOS, L, map*/

IOS.ns('l.edigeo.map');

IOS.l.edigeo.map.lieudits = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/lieudit',
            property: 'gb_ident'
        },
        get = function geojson(bbox) {
            var layer = L.geoJson('', {
                    style: function (feature) {

                        return {weight: 1, opacity: 0.4, color: '#F4EFA8'};
                    }
                }),
                legend;
            $.getJSON(config.url + '?bbox=' + bbox, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: get
    };
}());

IOS.l.edigeo.map.parcels = (function () {
    'use strict';
    var config = {
            url: '/layers/edigeo/parcel',
            infos_container: '#infos'
        },
        get = function geojson(bbox) {
            var layer,
                legend;
            layer = L.geoJson('', {
                style: function (feature) {

                    return {weight: 1, opacity: 0.4, color: '#F4EFA8'};
                },
                onEachFeature: function onEachFeature(feature, layer) {
                    if (feature.properties && feature.properties.idu) {
                        $(layer).on('click mouseover', function (e) {
                            $(config.infos_container).html(feature.properties.idu + ' ' + feature.properties.supf);
                        });
                    }
                }
            });

            $.getJSON(config.url + '?bbox=' + bbox, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: get
    };
}());
