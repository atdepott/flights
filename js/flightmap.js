require(["esri/map", "esri/geometry/Extent",
    "esri/dijit/Popup","application/AirportData",
    "application/bootstrapmap","dojo/domReady!"],
    function (Map, Extent, Popup, AirportData, BootstrapMap) {

        var initExtent = new Extent({ "xmin": -14661233.521319188, "ymin": 2736416.020782302, "xmax": -6511211.817442723, "ymax": 6967969.906648534, "spatialReference": { "wkid": 102100 } });

        var map = BootstrapMap.create("mapDiv", {
            basemap: "topo",
            extent: initExtent,
            scrollWheelZoom: true
        });

        var mapLoader = map.on("load", function () {
            var airports = new AirportData(map, "origin-input", "busy", "legendDiv");
            //todo stop listening for map load
        });

        var popup = new Popup({}, "popupDiv");
        map.infoWindow = popup;

        $("#aboutLink").click(function () {
            $("#mapDiv").hide();
            $("#aboutDiv").show();
            $(this).parent().parent().find('.active').removeClass('active');
            $("#aboutLink").parent().addClass('active');
        });

        $("#mapLink").click(function () {
            $("#mapDiv").show();
            $("#aboutDiv").hide();
            $(this).parent().parent().find('.active').removeClass('active');
            $("#mapLink").parent().addClass('active');
        });

        $("#homeLink").click(function () {
            $("#mapDiv").show();
            $("#aboutDiv").hide();
            $(this).parent().parent().find('.active').removeClass('active');
            $("#mapLink").parent().addClass('active');
        });
                
    });

