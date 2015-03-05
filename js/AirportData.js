define([
      "dojo/_base/declare",
	  "esri/map", "esri/graphic", "esri/InfoTemplate",
      "esri/graphicsUtils",
      "esri/SpatialReference", "esri/geometry/Point",
      "esri/symbols/SimpleMarkerSymbol", "esri/symbols/SimpleLineSymbol", "esri/symbols/SimpleFillSymbol",
      "esri/Color"
], function (
      declare,
	  Map, Graphic, InfoTemplate,
      graphicsUtils,
      SpatialReference, Point,
      SimpleMarkerSymbol, SimpleLineSymbol, SimpleFillSymbol,
      Color
    ) {

    var airportsCSVLocation = "data/Airports_3.csv";

    var sr = new SpatialReference(4326);


    red = new Color([255, 0, 0])
    orange = new Color([235, 100, 16])
    yellow = new Color([255, 255, 0])
    green = new Color([61, 138, 62])
    cyan = new Color([0, 255, 255])
    gray = new Color([96, 96, 96])


    var defaultPointSymbol = new SimpleMarkerSymbol(
        SimpleMarkerSymbol.STYLE_CIRCLE,
        12,
        new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
            gray, 3),
        gray);

    var selectedPointSymbol = new SimpleMarkerSymbol(
            SimpleMarkerSymbol.STYLE_CIRCLE,
            12,
            new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
                cyan, 3),
            cyan);

    var redSymbol = new SimpleMarkerSymbol(
            SimpleMarkerSymbol.STYLE_CIRCLE,
            12,
            new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
                red, 3),
            red);

    var orangeSymbol = new SimpleMarkerSymbol(
        SimpleMarkerSymbol.STYLE_CIRCLE,
        12,
        new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
            orange, 3),
        orange);

    var yellowSymbol = new SimpleMarkerSymbol(
        SimpleMarkerSymbol.STYLE_CIRCLE,
        12,
        new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
            yellow, 3),
        yellow);

    var greenSymbol = new SimpleMarkerSymbol(
        SimpleMarkerSymbol.STYLE_CIRCLE,
        12,
        new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
            green, 3),
        green);

    var classes = { 
        class_selected: {symbol: selectedPointSymbol, label: "Selected origin"},
        class_under_2_hrs: { symbol: greenSymbol, label: "Under 2 hours" },
        class_2_to_4_hrs: { symbol: yellowSymbol, label: "2 to 4 hours" },
        class_4_to_6_hrs: { symbol: orangeSymbol, label: "4 to 6 hours" },
        class_over_6_hrs: { symbol: redSymbol, label: "Over 6 hours" },
        class_default: {symbol: defaultPointSymbol, label: "Default"}
    }

    var infoTemplateTitle ="${CITY_NAME}";
    var infoTemplateContent = "<tr>Airport Code: <td>${ORIGIN}</td></tr>";

    return declare(null, {
        constructor: function (_map, _selectBox, _busy, _legend) {
            this.airports = {};
            this.map = _map;
            var self = this;

            $.ajax({
                type: "GET",
                url: airportsCSVLocation,
                dataType: "text",
                success: function (data) {
                    var airportrows = $.csv.toObjects(data);
                    var options = [];
                    $.each(airportrows, function (idx, row) {
                        var graphic = rowToGraphic(row);
                        _map.graphics.add(graphic);
                        self.airports[row.ORIGIN] = graphic;

                        var option = rowToOption(row);
                        options.push(option);
                    });

                    //$("#" + _selectBox).autocomplete({
                    //    source: options,
                    //    minLength: 2,
                    //    delay: 0,
                    //    change: function (event, ui) {
                    //        console.log("CHANGE!")
                    //        if (typeof ui != null) {
                    //            console.log(_busy)
                    //            $("#" + _busy).show();
                    //            var code = ui.item.value;
                    //            $.each(self.airports, function (idx, graphic) {
                    //                updateGraphic(graphic, code);
                    //            });
                    //            $("#" + _busy).hide();
                    //        }
                    //    }
                    //});

                    $("#" + _selectBox).append(options);
                }
            });

            $("#" + _selectBox).change(function () {
                var code = $("#" + _selectBox).val();
                var selectedGraphic;
                $.each(self.airports, function (idx, graphic) {
                    if (code == graphic.attributes.ORIGIN) {
                        selectedGraphic = graphic;
                    }
                    updateGraphic(graphic, code);
                });
                _map.centerAt(selectedGraphic.geometry)
            });

            var legendDiv = $("#" + _legend);
            var legendTable = $("<table/>").appendTo(legendDiv);
            $.each(classes, function (idx, classobj) {
                var row = $("<tr/>").appendTo(legendTable);

                //var colorCell = $("<td />").text(classobj.symbol.color.toString()).appendTo(row);
                var colorCell = $("<td />").appendTo(row);
                colorCell.addClass("legendImageCell");
                var canvas = $("<canvas/>").attr("width", 20).attr("height", 20).appendTo(colorCell);
                var ctx = canvas[0].getContext("2d");
                ctx.fillStyle = classobj.symbol.color.toHex();
                ctx.beginPath();
                ctx.arc(10, 10, 10, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();

                
                var labelCell = $("<td />").text(classobj.label).appendTo(row);
                labelCell.addClass("legendLabelCell");
            });
        }
    });

    function rowToGraphic(row) {
        var geometry = new Point(row.LONG, row.LAT, sr);
        var graphic = new Graphic(geometry, defaultPointSymbol, row, new InfoTemplate(infoTemplateTitle, infoTemplateContent));
        return graphic;
    }

    function rowToOption(row) {
        return $("<option/>").attr({ 'value': row.ORIGIN }).text(row.CITY_NAME + ' (' + row.ORIGIN + ')');
        //return { label: row.CITY_NAME + ' (' + row.ORIGIN + ')', value: row.ORIGIN }
    }

    function updateGraphic(graphic, code) {
        var isClose = false;
        var infoTemplate;

        if (graphic.attributes.ORIGIN == code) {
            isClose = true;
            reassignGraphicClass(graphic, 'class_selected')
            infoTemplate = new InfoTemplate(infoTemplateTitle, infoTemplateContent)
        } else if (graphic.attributes[code] > 360) {
            reassignGraphicClass(graphic, 'class_over_6_hrs')
            infoTemplate = new InfoTemplate(infoTemplateTitle, "<tr>Airport Code: <td>${ORIGIN}</td></tr><br/><tr>Travel minutes: <td>${" + code + ":NumberFormat(places:0)}</td></tr>");
        } else if (graphic.attributes[code] > 240) {
            reassignGraphicClass(graphic, 'class_4_to_6_hrs')
            infoTemplate = new InfoTemplate(infoTemplateTitle, "<tr>Airport Code: <td>${ORIGIN}</td></tr><br/><tr>Travel minutes: <td>${" + code + ":NumberFormat(places:0)}</td></tr>");
        } else if (graphic.attributes[code] > 120) {
            reassignGraphicClass(graphic, 'class_2_to_4_hrs')
            infoTemplate = new InfoTemplate(infoTemplateTitle, "<tr>Airport Code: <td>${ORIGIN}</td></tr><br/><tr>Travel minutes: <td>${" + code + ":NumberFormat(places:0)}</td></tr>");
        } else if (graphic.attributes[code] > 0) {
            isClose = true;
            reassignGraphicClass(graphic, 'class_under_2_hrs')
            infoTemplate = new InfoTemplate(infoTemplateTitle, "<tr>Airport Code: <td>${ORIGIN}</td></tr><br/><tr>Travel minutes: <td>${" + code + ":NumberFormat(places:0)}</td></tr>");
        } else {
            reassignGraphicClass(graphic, 'class_default')
            infoTemplate = new InfoTemplate(infoTemplateTitle, infoTemplateContent)
        }

        graphic.setInfoTemplate(infoTemplate);
        return isClose;
    }

    function reassignGraphicClass(graphic, label) {
        graphic.setSymbol(classes[label].symbol);
    }
    
});