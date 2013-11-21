/*jslint browser: true*/
/*global $, jQuery, IOS, L, map*/

IOS.ns('l.edigeo.map');

IOS.l.edigeo.map.lieudits = (function () {
    'use strict';
    var config = {
        url: '/layers/edigeo/lieudit',
        property: 'gb_ident'
    },
    get = function geojson() {
        var layer = L.geoJson('', {
            style: function () {

                return {weight: 1, opacity: 0.4, color: '#F4EFA8'};
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
        get: get
    };
}());
