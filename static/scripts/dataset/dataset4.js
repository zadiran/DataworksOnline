      
    function minimum(array) {
        var minval = array[0];
        array.map(function(v, i, a) {
            if (!v && v!=0)
            {
                return minval;
            }
            if (v < minval || (!minval && minval !== 0)) {
                minval = v; 
            }
        })
        return minval;
    }
    function maximum(array) {
        var maxval = array[0];
        array.map(function(v) {
            if (!v && v!==0)
            {
                return;
            }
            if (v > maxval || (!maxval && maxval !== 0)) {
                maxval = v; 
            }
        })
        return maxval;
    }
        


          var svg ,
            margin ,
            margin2,
            width ,
            height ,
            height2;

        var x ,
            x2,
            y ,
            y2;
        
        var xAxis ,
            xAxis2,
            yAxis ;

        var area 
        var area2 
        var parseDate 
        var context
        var focus
        var brush 
        var data
        var saved_forecast = []
        var zoom

        var real_big, real_small
        var forecast_big, forecast_small
        var confidence_upper_big, confidence_upper_small
        var confidence_lower_big, confidence_lower_small
        var outlier_big, outlier_small
        var confidence_area_big, confidence_area_small
        
        var circles, circles_small

        var routines = []

        var minlen
        var maxlen
        var cleanTempDataUrl 
        var dataUrl
        var fileId

        $(function () 
        {
            minlen = parseInt($('#min-len').val());
            maxlen = parseInt($('#max-len').val());
            cleanTempDataUrl = $('#clean-temp-data-url').val();
            dataUrl = $('#data-url').val();
            fileId = $('#file-id').val();

            $('#delayBetweenAdditionsForecast').val(1)
            $('#forecastHorizon').val(5)

         svg = d3.select("svg")
            margin = {top: 20, right: 20, bottom: 110, left: 40}
            margin2 = {top: 430, right: 20, bottom: 30, left: 40}
            width = +svg.attr("width") - margin.left - margin.right
            height = +svg.attr("height") - margin.top - margin.bottom
            height2 = +svg.attr("height") - margin2.top - margin2.bottom;

         x = d3.scaleTime().range([0, width])
            x2 = d3.scaleTime().range([0, width])
            y = d3.scaleLinear().range([height, 0])
            y2 = d3.scaleLinear().range([height2, 0]);
        
         xAxis = d3.axisBottom(x)
            xAxis2 = d3.axisBottom(x2)
            yAxis = d3.axisLeft(y);

        // area = d3.line()
        //     .x(function(d) { return x(new Date(d[0])); })
        //     .y(function(d) { return y(parseFloat(d[1])); });
        
        //  area2 = d3.line()
        //     .x(function(d) { return x2(new Date(d[0])); })
        //     .y(function(d) { return y2(parseFloat(d[1])); });
         
         real_big = d3.line()
            .defined(function(d) {  return !!d.real; })
            .x(function(d) { return x(new Date(d.timestamp))})
            .y(function(d) { return y(d.real)})

         real_small = d3.line()
            .defined(function(d) { return !!d.real;})
            .x(function(d) { return x2(new Date(d.timestamp))})
            .y(function(d) { return y2(d.real)})
         //parseDate = d3.timeParse("%b %Y");
       
        forecast_big = d3.line()
            .defined(function(d) { return !!d.forecast; })
            .x(function(d) { return x(new Date(d.timestamp))})
            .y(function(d) { return y(parseFloat(d.forecast))})
            
        forecast_small = d3.line()
            .defined(function(d) { return !!d.forecast; })
            .x(function(d) { return x2(new Date(d.timestamp))})
            .y(function(d) { return y2(parseFloat(d.forecast))})
        
        confidence_upper_big = d3.line()
            .defined(function(d) { return !!d.ci_u})
            .x(function(d) { return x(new Date(d.timestamp))})
            .y(function(d) { return y(d.ci_u)})

        confidence_upper_small = d3.line()
            .defined(function(d) { return !!d.ci_u})
            .x(function(d) { return x2(new Date(d.timestamp))})
            .y(function(d) { return y2(d.ci_u)})

        confidence_lower_big = d3.line()
            .defined(function(d) { return  !!d.ci_l })
            .x(function(d) { return x(new Date(d.timestamp)) })
            .y(function(d) { return y(d.ci_l) })
            
        confidence_lower_small = d3.line()
            .defined(function(d) { return  !!d.ci_l })
            .x(function(d) { return x2(new Date(d.timestamp)) })
            .y(function(d) { return y2(d.ci_l) })

        confidence_area_big = d3.area()
            .defined(function(d) {return !!d.ci_l && !!d.ci_u;})
            .x(function(d) { return x(new Date(d.timestamp)); })
            .y0(function(d) { return y(d.ci_u); })
            .y1(function(d) { return y(d.ci_l); });

        confidence_area_small = d3.area()
        .defined(function(d) {return !!d.ci_l && !!d.ci_u;})
        .x(function(d) { return x2(new Date(d.timestamp)); })
        .y0(function(d) { return y2(d.ci_u); })
        .y1(function(d) { return y2(d.ci_l); });

        outlier_big = d3.line()
            .defined(function(d) { return !!d.outlier })
            .x(function(d) { return x(new Date(d.timestamp)) })
            .y(function(d) { return y(d.outlier) })

        outlier_small = d3.line()
            .defined(function(d) { return !!d.outlier })
            .x(function(d) { return x2(new Date(d.timestamp)) })
            .y(function(d) { return y2(d.outlier) })

         brush = d3.brushX()
            .extent([[0, 0], [width, height2]])
            .on("brush end", brushed); 
        
         zoom = d3.zoom()
            .scaleExtent([1, Infinity])
            .translateExtent([[0, 0], [width, height]])
            .extent([[0, 0], [width, height]])
            .on("zoom", zoomed);
        
        
        svg.append("defs").append("clipPath")
            .attr("id", "clip")
          .append("rect")
            .attr("width", width)
            .attr("height", height);
        
        focus = svg.append("g")
            .attr("class", "focus")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        context = svg.append("g")
            .attr("class", "context")
            .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");
        
    
        
          focus.append("g")
              .attr("class", "axis axis--x")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);
        
          focus.append("g")
              .attr("class", "axis axis--y")
              .call(yAxis);
        
        //   context.append("path")
        //       .datum(data)
        //       .attr("class", "line")
        //       .attr("d", area2);
        
          context.append("g")
              .attr("class", "axis axis--x")
              .attr("transform", "translate(0," + height2 + ")")
              .call(xAxis2);
        
          context.append("g")
              .attr("class", "brush")
              .call(brush)
              .call(brush.move, x.range());
        
          svg.append("rect")
              .attr("class", "zoom")
              .attr("width", width)
              .attr("height", height)
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
              .call(zoom);
    
            function brushed() {
                if (d3.event.sourceEvent && d3.event.sourceEvent.type === "zoom") return; // ignore brush-by-zoom
                
                var s = d3.event.selection || x2.range();
                x.domain(s.map(x2.invert, x2));
                focus.select(".line").attr("d", real_big);
                focus.select(".line-forecast").attr("d", forecast_big);
                focus.select(".line-old-forecast").attr("d", forecast_big);
                focus.select(".line-confidence-lower").attr("d", confidence_lower_big);
                focus.select(".line-confidence-upper").attr("d", confidence_upper_big);
                focus.select('.confidence-area').attr('d', confidence_area_big);
                //focus.select('.line-outlier').attr('d', outlier_big);
                // focus.selectAll("dot")
                // .attr("transform", transform);

                focus.selectAll(".dot")
                .attr("cx", function(d) { return x(new Date(d.timestamp)); })
                .attr("cy", function(d) { return y(d.outlier); });

                focus.select(".axis--x").call(xAxis);
                //     svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
                //         .scale(width / (s[1] - s[0]))
                //         .translate(-s[0], 0));
             }
            
            function zoomed() {
                if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
                var t = d3.event.transform;
                x.domain(t.rescaleX(x2).domain());

                focus.select(".line").attr("d", real_big);
                focus.select(".line-forecast").attr("d", forecast_big);
                focus.select(".line-old-forecast").attr("d", forecast_big);
                focus.select(".line-confidence-lower").attr("d", confidence_lower_big);
                focus.select(".line-confidence-upper").attr("d", confidence_upper_big);
                focus.select('.confidence-area').attr('d', confidence_area_big)
                
                var new_yScale = d3.event.transform.rescaleX(x2);
                circles.attr("cx", function(d) { return new_yScale(new Date(d.timestamp)); });

                focus.select(".axis--x").call(xAxis);
                context.select(".brush").call(brush.move, x.range().map(t.invertX, t));
            }

        });
        
        function stopAllRoutines() {
            routines.map(function(v, i, a) {
                clearTimeout(v);
            })
            routines = []
        }
                
        function runProcess() {
            
            stopAllRoutines();
            saved_forecast = []
            
            focus.selectAll('.line').remove();
            focus.selectAll('.line-forecast').remove();
            focus.selectAll('.line-old-forecast').remove();
            focus.selectAll('.line-confidence-lower').remove();
            focus.selectAll('.line-confidence-upper').remove();
            focus.selectAll('circle').remove();
            focus.selectAll('.line-old-forecast').remove();

            context.selectAll('.line').remove();
            context.selectAll('.line-forecast').remove();
            context.selectAll('.line-old-forecast').remove();
            context.selectAll('.line-confidence-lower').remove();
            context.selectAll('.line-confidence-upper').remove();
            context.selectAll('.line-outlier').remove();

             var delay = parseFloat($('#delayBetweenAdditionsForecast').val(), 10);
        //     //getData('{{ model.file.id }}', maxlen);
        //     svg.select('path.line').remove();
            
        //   x.domain(d3.extent(data, function(d) { return new Date(d.timestamp); }));
    
        //   var min = parseFloat(d3.min(data, function(d) { 
        //       return minimum([d.ci_l,d.real, d.forecast,  d.ci_u]); 
        //     }));
        //   var max = parseFloat(d3.max(data, function(d) { 
        //       //console.log(d.ci_l)
        //       return maximum([d.real, d.forecast, d.ci_l, d.ci_u]); 
        //     }));
        //   console.log('min ' + min)
        //   console.log('max '+ max)
        //   var addition = (max - min) / 10; 
        //   y.domain([min - addition ,max + addition]);
        //   console.log([min - addition ,max + addition])

        //   focus.selectAll('.axis--y').call(yAxis);
        //   focus.selectAll('.axis--x').call(xAxis);

        //   x2.domain(x.domain());
        // //   y2.domain(y.domain());
        // var i = minlen;
        // var interval = setInterval(function() {
        //     drawStep(i);
        //     i = i + 1;
        //     if (i >= maxlen) {
        //         clearinterval(interval);
        //     }
        // }, delay * 1000);
        var j = minlen;
        for (var i = minlen; i <= maxlen; i++)  {
                 var del =( i - minlen) * delay * 1000;
             var timeout = setTimeout(function() {
                 var k = parseInt(j);
                 j++;
                 drawStep(k);
             },del);
             routines.push(timeout)
        }
        finish();
    }
        
    function getData(id, i) {
        $.ajax({
            method: 'GET',
            async: false,
            cache: true,
            data: { 
                dataset: id,
                horizon: $('#forecastHorizon').val(),
                count: i,
                forecast_model: $('#forecastModel').find(':selected').val(),
                outlier_detector: $('#outlierDetection').find(':selected').val()
            },
            url: dataUrl,
            success: function(loaded) {
                data = loaded;
            //    alert(loaded)
             //   console.log(loaded);
            },
            error: function() {
                stopAllRoutines();
                alert('Error happened while data from server was retrieved. Please try to reload page in a while')
            }
        })
    }
    var hard_stop;
    function drawStep(j) {
        getData(fileId, j);
        var k = 0;
        while (!data[k].forecast) {
            k = k + 1;
        }
        saved_forecast.push(data[k + 1]);
        doRoutine(j);
    }

    function finish() {
        $.ajax({
            method: 'GET',
            url: cleanTempDataUrl
        }) 
    }

    function doRoutine(j) {
        focus.selectAll('.line').remove();
            focus.selectAll('.line-forecast').remove();
            focus.selectAll('.line-old-forecast').remove();
            focus.selectAll('.line-confidence-lower').remove();
            focus.selectAll('.line-confidence-upper').remove();
            focus.selectAll('.confidence-area').remove();
            focus.selectAll('circle').remove();

            context.selectAll('.line').remove();
            context.selectAll('.line-forecast').remove();
            context.selectAll('.line-old-forecast').remove();
            context.selectAll('.line-confidence-lower').remove();
            context.selectAll('.line-confidence-upper').remove();
            context.selectAll('.confidence-area').remove();
            context.selectAll('.line-outlier').remove();

            //var delay = parseFloat($('#delayBetweenAdditionsForecast').val(), 10);
           // getData('{{ model.file.id }}');
            svg.select('path.line').remove();
            
          x.domain(d3.extent(data, function(d) { return new Date(d.timestamp); }));
          //x.domain(d3.extent(data.slice(j-minlen, data.length), function(d) { return new Date(d.timestamp); }));
    
          var mins = data.map(function(v,i,a) {
              return minimum([v.ci_l,v.real, v.forecast,  v.ci_u]);
          })
          var min =  minimum(mins)
          var max = parseFloat(d3.max(data, function(d) { 
              //console.log(d.ci_l)
              return maximum([d.real, d.forecast, d.ci_l, d.ci_u]); 
            }));
          console.log('min ' + min)
          console.log('max '+ max)
          var addition = (max - min) / 10; 
          y.domain([min - addition ,max + addition]);
          console.log([min - addition ,max + addition])

          focus.selectAll('.axis--y').call(yAxis);
          focus.selectAll('.axis--x').call(xAxis);

          x2.domain(x.domain());
          y2.domain(y.domain());
          
        // Select the section we want to apply our changes to
        focus.selectAll('.line').remove();
        focus.selectAll('.line-forecast').remove();
        focus.selectAll('.line-old-forecast').remove();
        focus.selectAll('.line-confidence-lower').remove();
        focus.selectAll('.line-confidence-upper').remove();
        focus.selectAll('.confidence-area').remove();
        svg.selectAll('.circles').remove();
        
        context.selectAll('.line').remove();
        context.selectAll('.line-forecast').remove();
        context.selectAll('.line-old-forecast').remove();
        context.selectAll('.line-confidence-lower').remove();
        context.selectAll('.line-confidence-upper').remove();
        context.selectAll('.confidence-area').remove();

        focus.append('path')
        .datum(data)
        .attr('class', 'line-confidence-upper')
        .attr('d', confidence_upper_big);
        
        context.append('path')
        .datum(data)
        .attr('class', 'line-confidence-upper')
        .attr('d', confidence_upper_small);
        
        focus.append('path')
        .datum(data)
        .attr('class', 'line-confidence-lower')
        .attr('d', confidence_lower_big);
        
        context.append('path')
        .datum(data)
        .attr('class', 'line-confidence-lower')
        .attr('d', confidence_lower_small);

        context.append('path')
        .datum(data)
        .attr('class', 'line')
        .attr('d', real_small);

        focus.append('path')
        .datum(data)
        .attr('class', 'confidence-area')
        .attr('d', confidence_area_big)

        context.append('path')
        .datum(data)
        .attr('class', 'confidence-area')
        .attr('d', confidence_area_small)
        
        focus.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", real_big);
        
        focus.append("path")
        .datum(data)
        .attr("class", "line-forecast")
        .attr("d", forecast_big);

        focus.append('path')
        .datum(saved_forecast.slice(0, saved_forecast.length - 1))
        .attr('class', 'line-old-forecast')
        .attr('d', forecast_big);

        context.append("path")
        .datum(data)
        .attr("class", "line-forecast")
        .attr("d", forecast_small);

        context.append("path")
        .datum(saved_forecast.slice(0, saved_forecast.length - 1))
        .attr("class", "line-old-forecast")
        .attr("d", forecast_small);

        circles_data = []
        for (var i = 0; i < data.length; i++) { 
            if (data[i].outlier || data[i].outlier === 0) {
                circles_data.push(data[i])
            }
        }
        circles = focus.append("g")
            .attr("class", "circles")
            //.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .selectAll("circle")
            .data(circles_data)
            .enter()
            .append("circle")
            .attr('class', 'dot')
            .attr("r", 6)
            .attr("cx", function(d) { return x(new Date(d.timestamp)); })
            .attr("cy", function(d) { return y(d.outlier); });
        
            circles_small = context.append("g")
            .attr("class", "circles")
            //.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .selectAll("circle")
            .data(circles_data)
            .enter()
            .append("circle")
            .attr('class', 'dot')
            .attr("r", 3)
            .attr("cx", function(d) { return x2(new Date(d.timestamp)); })
            .attr("cy", function(d) { return y2(d.outlier); });
    }