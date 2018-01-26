var svg,
    margin,
    margin2,
    width,
    height,
    height2;

    var x,
        x2,
        y,
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
        var zoom
        
        $(function () 
        {
            $('#delayBetweenAdditions').val(0.1)
            data = JSON.parse($('#raw-data').val());
           
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

        area = d3.line()
            .x(function(d) { return x(new Date(d[0])); })
            .y(function(d) { return y(parseFloat(d[1])); });
        
         area2 = d3.line()
            .x(function(d) { return x2(new Date(d[0])); })
            .y(function(d) { return y2(parseFloat(d[1])); });

         parseDate = d3.timeParse("%b %Y");
       
        
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
        
    
          x.domain(d3.extent(data, function(d) { return new Date(d[0]); }));
    
          var min = parseFloat(d3.min(data, function(d) { return parseFloat(d[1]); }));
          var max = parseFloat(d3.max(data, function(d) { return parseFloat(d[1]); }));
          var addition = (max - min) / 10; 
          y.domain([min - addition, max + addition]);
          x2.domain(x.domain());
          y2.domain(y.domain());
        
        //   focus.append("path")
        //       .datum(data)
        //       .attr("class", "line")
        //       .attr("d", area);
        
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
            focus.select(".line").attr("d", area);
            focus.select(".axis--x").call(xAxis);
            svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
                .scale(width / (s[1] - s[0]))
                .translate(-s[0], 0));
            }
            
            function zoomed() {
            if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
            var t = d3.event.transform;
            x.domain(t.rescaleX(x2).domain());
            focus.select(".line").attr("d", area);
            focus.select(".axis--x").call(xAxis);
            context.select(".brush").call(brush.move, x.range().map(t.invertX, t));
            }

        });
        
                
        function runProcess() {
            
            focus.selectAll('.line').remove();
            context.selectAll('.line').remove();
            var delay = parseFloat($('#delayBetweenAdditions').val(), 10);

            svg.select('path.line').remove();

            var cnt = 1;
            var max_cnt = data.length;
            var interval = setInterval(function() {
                // Select the section we want to apply our changes to
                var svg = d3.select("svg").transition();
                focus.selectAll('.line').remove();
                context.selectAll('.line').remove();
                focus.append("path")
                .datum(data.slice(0, cnt))
                .attr("class", "line")
                .attr("d", area);
                context.append("path")
              .datum(data.slice(0, cnt))
              .attr("class", "line")
              .attr("d", area2);
                cnt = cnt + 1;
                if (cnt > max_cnt) {
                    cnt = 0;
                    clearInterval(interval)
                }
            }, delay * 1000)
        }
        