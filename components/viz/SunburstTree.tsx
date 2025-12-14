"use client";

import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

export default function SunburstTree() {
    const svgRef = useRef<SVGSVGElement>(null);
    const wrapperRef = useRef<HTMLDivElement>(null);
    const [data, setData] = useState<any>(null);

    // Custom interface for animation properties
    interface MyHierarchyNode extends d3.HierarchyRectangularNode<any> {
        current?: any;
        target?: any;
    }

    useEffect(() => {
        fetch("/data/tree.json")
            .then((res) => res.json())
            .then((data) => setData(data));
    }, []);

    useEffect(() => {
        if (!data || !svgRef.current || !wrapperRef.current) return;

        // Clear previous
        d3.select(svgRef.current).selectAll("*").remove();

        const width = wrapperRef.current.clientWidth;
        const height = wrapperRef.current.clientHeight;
        const radius = Math.min(width, height) / 6;

        const color = d3.scaleOrdinal(d3.schemeSpectral[11]);

        const hierarchy = d3.hierarchy(data)
            .sum(d => d.value ?? 0)
            .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));

        const root = d3.partition()
            .size([2 * Math.PI, hierarchy.height + 1])
            (hierarchy);

        root.each((d: MyHierarchyNode) => d.current = d);

        const arc = d3.arc<any>()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

        const svg = d3.select(svgRef.current)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .style("font", "10px sans-serif");

        const path = svg.append("g")
            .selectAll("path")
            .data(root.descendants().slice(1))
            .join("path")
            .attr("fill", (d: MyHierarchyNode) => {
                while (d.depth > 1) d = d.parent as MyHierarchyNode;
                return color(d.data.name);
            })
            .attr("fill-opacity", (d: MyHierarchyNode) => arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0)
            .attr("pointer-events", (d: MyHierarchyNode) => arcVisible(d.current) ? "auto" : "none")
            .attr("d", (d: MyHierarchyNode) => arc(d.current));

        path.filter((d: MyHierarchyNode) => !!d.children)
            .style("cursor", "pointer")
            .on("click", clicked);

        path.append("title")
            .text((d: MyHierarchyNode) => `${d.data.name}\n${(d.value ?? 0).toLocaleString()}`);

        const label = svg.append("g")
            .attr("pointer-events", "none")
            .attr("text-anchor", "middle")
            .style("user-select", "none")
            .selectAll("text")
            .data(root.descendants().slice(1))
            .join("text")
            .attr("dy", "0.35em")
            .attr("fill-opacity", (d: MyHierarchyNode) => +labelVisible(d.current))
            .attr("transform", (d: MyHierarchyNode) => labelTransform(d.current))
            .text((d: MyHierarchyNode) => d.data.name)
            .style("fill", "white")
            .style("font-size", "12px");

        const parent = svg.append("circle")
            .datum(root)
            .attr("r", radius)
            .attr("fill", "none")
            .attr("pointer-events", "all")
            .on("click", clicked);

        function clicked(event: any, p: any) {
            parent.datum(p.parent || root);

            root.each((d: MyHierarchyNode) => d.target = {
                x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                y0: Math.max(0, d.y0 - p.depth),
                y1: Math.max(0, d.y1 - p.depth)
            });

            const t = svg.transition().duration(750);

            path.transition(t as any)
                .tween("data", (d: MyHierarchyNode) => {
                    const i = d3.interpolate(d.current, d.target);
                    return t => d.current = i(t);
                })
                .filter(function (d: MyHierarchyNode) {
                    return !!(+((this as unknown as Element).getAttribute("fill-opacity") || 0) || arcVisible(d.target));
                })
                .attr("fill-opacity", (d: MyHierarchyNode) => arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0)
                .attr("pointer-events", (d: MyHierarchyNode) => arcVisible(d.target) ? "auto" : "none")
                .attrTween("d", (d: MyHierarchyNode) => () => arc(d.current as any) || "");

            label.filter(function (d: MyHierarchyNode) {
                return !!(+((this as unknown as Element).getAttribute("fill-opacity") || 0) || labelVisible(d.target));
            }).transition(t as any)
                .attr("fill-opacity", (d: MyHierarchyNode) => +labelVisible(d.target))
                .attrTween("transform", (d: MyHierarchyNode) => () => labelTransform(d.current));
        }

        function arcVisible(d: any) {
            return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
        }

        function labelVisible(d: any) {
            return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
        }

        function labelTransform(d: any) {
            const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
            const y = (d.y0 + d.y1) / 2 * radius;
            return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
        }

        return () => {
            // Cleanup
        };
    }, [data]);

    if (!data) return <div className="text-center p-10 text-primary animate-pulse">Initializing Bio-Sequence...</div>;

    return (
        <div ref={wrapperRef} className="h-[700px] w-full glass-card rounded-xl overflow-hidden flex items-center justify-center relative">
            <div className="absolute top-4 right-4 bg-black/40 px-3 py-1 rounded-full text-xs text-muted-foreground border border-white/10 pointer-events-none">
                Click center to zoom out
            </div>
            <svg ref={svgRef} className="w-full h-full" />
        </div>
    );
}
