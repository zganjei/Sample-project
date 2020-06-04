const data = {
    "nodes": [
        {
            "name": "Abc",
            "id": "1",
            "value": "1",
            "cvr": "123"
        },
        {
            "name": "Aaa",
            "id": "2",
            "value": "0.25",
            "cvr": "7445"
        },
        {
            "name": "JTY",
            "id": "3",
            "value": "0.25",
            "cvr": "24582"
        },
        {
            "name": "TTT",
            "id": "4",
            "value": "0.1",
            "cvr": "12351"
        },
        {
            "name": "MMM",
            "id": "5",
            "value": "0.15",
            "cvr": "783456"
        },
        {
            "name": "KLI",
            "id": "6",
            "value": "0.05"
        },
        {
            "name": "OTP",
            "id": "7",
            "value": "0.250"
        },
        {
            "name": "Tasqu",
            "id": "8",
            "value": "0.250"
        },
        {
            "name": "Mii",
            "id": "9",
            "value": "0.10"
        },
        {
            "name": "YrA",
            "id": "11",
            "value": "0.150",
            "cvr": "10096669"
        },
        {
            "name": "Tarb",
            "id": "10",
            "value": "0.1500"
        }
    ],
    "links": [
        {
            "source": "2",
            "target": "1",
            "text": "linkText"
        },
        {
            "source": "3",
            "target": "1",
            "text": "linkText"

        },
        {
            "source": "4",
            "target": "1",
            "text": "linkText"

        },
        {
            "source": "5",
            "target": "1",
            "text": "linkText"

        },
        {
            "source": "6",
            "target": "1",
            "text": "linkText"

        },
        {
            "source": "7",
            "target": "2",
            "text": "linkText"

        },
        {
            "source": "8",
            "target": "3",
            "text": "linkText"

        },
        {
            "source": "9",
            "target": "4",
            "text": "linkText"

        },
        {
            "source": "11",
            "target": "5",
            "text": "linkText"

        },
        {
            "source": "10",
            "target": "11",
            "text": "linkText"

        }
    ]
};

// Create somewhere to put the force directed graph
let svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

const rectWidth = 100;
const rectHeight = 60;
const minDistance = Math.sqrt(rectWidth * rectWidth + rectHeight * rectHeight);

// Set up the simulation and add forces
let simulation = d3.forceSimulation()
    .nodes(data.nodes);

let link_force = d3.forceLink(data.links)
    .id(function (d) {
        return d.id;
    }).distance(minDistance).strength(1);

let charge_force = d3.forceManyBody()
    .strength(-1100);

let center_force = d3.forceCenter(width / 2, height / 2);

simulation
    .force("charge_force", charge_force)
    .force("center_force", center_force)
    .force("links", link_force)
    .force('y', d3.forceY(height / 2).strength(0.10));


// Add tick instructions:
simulation.on("tick", tickActions);

// Add encompassing group for the zoom
let g = svg.append("g")
    .attr("class", "everything");

let div = g.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// Draw lines for the links
let link = g.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(data.links)
    .join("line")
    .attr("stroke-width", 2)
    .style("stroke", linkColour);

link.append("title")
    .text(function (d) {
        return d.text;
    });

let edgepaths = g.selectAll(".edgepath")
    .data(data.links)
    .enter()
    .append('path')
    .attr("class", "edgepath")
    .attr("fill-opacity", 0)
    .attr("stroke-opacity", 0)
    .attr("id", function (d, i) {
        return 'edgepath' + i
    })
    .style("pointer-events", "none");
// .attrs({
//     'class': 'edgepath',
//     'fill-opacity': 0,
//     'stroke-opacity': 0,
//     'id': function (d, i) {
//         return 'edgepath' + i
//     }
// })
// .style("pointer-events", "none");

let edgelabels = g.selectAll(".edgelabel")
    .data(data.links)
    .enter()
    .append('text')
    .style("pointer-events", "none")
    .attr("class", "edgelabel")
    .attr("id", function (d, i) {
        return 'edgelabel' + i
    })
    .attr("font-size", 10)
    .attr("fill", "black");
// .attrs({
//     'class': 'edgelabel',
//     'id': function (d, i) {
//         return 'edgelabel' + i
//     },
//     'font-size': 10,
//     'fill': '#aaa'
// });

edgelabels.append('textPath')
    .attr('xlink:href', function (d, i) {
        return '#edgepath' + i
    })
    .style("text-anchor", "middle")
    .style("pointer-events", "none")
    .attr("startOffset", "50%")
    .text(function (d) {
        return d.text
    });

// Draw rects and texts for the nodes
let nodes = g.append("g")
    .attr("class", "nodes");

let node = nodes.selectAll("node")
    .data(data.nodes)
    .join("g");

node
    .on("mouseover", function (d) {
        d3.select(this).select("rect").style("fill", "red");
        div.transition()
            .duration(200)
            .style("opacity", .9);
        div.html("asdasd")
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
    })
    .on("mouseout", function (d) {
        d3.select(this).select("rect").style("fill", rectColour);
        div.transition()
            .duration(500)
            .style("opacity", 0);
    });


let rect = node.append("rect")
    .attr("x", -rectWidth / 2)
    .attr("y", -rectHeight / 2)
    .attr("width", rectWidth)
    .attr("height", rectHeight)
    .attr("fill", rectColour);

let textName = node.append("text")
    .text(function (d) {
        return d.name;
    })
    .attr("y", -15)
    .style("text-anchor", "middle");

let textCvr = node.append("text")
    .text(function (d) {
        return d.cvr;
    })
    .attr("y", 0)
    .style("text-anchor", "middle");

let textOwned = node.append("text")
    .text(function (d) {
        return (parseFloat(d.value) * 100).toFixed(2) + "%";
    })
    .attr("y", 15)
    .style("text-anchor", "middle");

node.attr("transform", function (d) {
    return "translate(" + d.x + "," + d.y + ")"
});

// Add drag capabilities
var drag_handler = d3.drag()
    .on("start", drag_start)
    .on("drag", drag_drag)
    .on("end", drag_end);

drag_handler(node);

// Add zoom capabilities
let zoom_handler = d3.zoom()
    .on("zoom", zoom_actions);

zoom_handler(svg);

/** Functions **/

function rectColour(d) {
    if (d.person) {
        return "blue";
    } else {
        return "pink";
    }
}

// Function to choose the line colour and thickness
function linkColour(d) {
    return "black";
}

// Drag functions
function drag_start(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

// Make sure you can't drag the rect outside the box
function drag_drag(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function drag_end(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// Zoom functions
function zoom_actions() {
    g.attr("transform", d3.event.transform)
}

function tickActions() {
    // update node positions each tick of the simulation
    node.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")"
    });
    // update link positions
    link
        .attr("x1", function (d) {
            return d.source.x;
        })
        .attr("y1", function (d) {
            return d.source.y;
        })
        .attr("x2", function (d) {
            return d.target.x;
        })
        .attr("y2", function (d) {
            return d.target.y;
        });

    edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
    });

    edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
            var bbox = this.getBBox();

            rx = bbox.x + bbox.width / 2;
            ry = bbox.y + bbox.height / 2;
            return 'rotate(180 ' + rx + ' ' + ry + ')';
        }
        else {
            return 'rotate(0)';
        }
    });
}
