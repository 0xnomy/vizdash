"use client";

import { useEffect, useState, useRef } from "react";
import dynamic from "next/dynamic";
import { Card } from "@/components/ui/Card";

// Dynamic import for No-SSR
const ForceGraph3D = dynamic(() => import("react-force-graph-3d"), { ssr: false });

export default function NetworkGraph() {
    const [data, setData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [hoverNode, setHoverNode] = useState<any>(null);
    const graphRef = useRef<any>(null);
    const [rotationSpeed, setRotationSpeed] = useState(0.5);

    useEffect(() => {
        fetch("/data/network.json")
            .then((res) => res.json())
            .then((data) => {
                setData(data);
                setLoading(false);
            })
            .catch((err) => console.error("Failed to load network data:", err));
    }, []);

    // Auto-rotation effect
    useEffect(() => {
        if (!graphRef.current) return;

        const interval = setInterval(() => {
            if (graphRef.current) {
                const angle = graphRef.current.cameraPosition().x;
                // Simple slow rotation if needed, but react-force-graph controls are better usually
            }
        }, 50);
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="text-center p-10 text-primary animate-pulse">Initializing Neural Link...</div>;

    return (
        <div className="h-[700px] w-full rounded-xl overflow-hidden border border-white/10 relative glass-card flex flex-col md:flex-row">
            <div className="flex-1 relative h-full">
                <ForceGraph3D
                    ref={graphRef}
                    graphData={data}
                    nodeLabel="" // Custom handling via hover

                    // Node Styling
                    nodeColor={(node: any) => {
                        const colors = ["#00F0FF", "#7000FF", "#FF0055", "#FFD700", "#00FF99"];
                        return hoverNode?.id === node.id ? "#FFFFFF" : (colors[node.group % colors.length] || "#00F0FF");
                    }}
                    nodeOpacity={0.8}
                    nodeResolution={24}
                    nodeVal={(node: any) => {
                        const base = (node.val || 1) * 3;
                        return hoverNode?.id === node.id ? base * 1.5 : base;
                    }}

                    // Link Styling
                    linkColor={() => "rgba(0, 240, 255, 0.15)"}
                    linkWidth={0.5}
                    linkDirectionalParticles={2}
                    linkDirectionalParticleWidth={2}
                    linkDirectionalParticleSpeed={0.005}
                    // linkDirectionalParticleColor={() => "#ffffff"}

                    // Environment
                    backgroundColor="#020205" // Very dark background
                    showNavInfo={false}

                    // Interaction
                    onNodeHover={(node: any) => {
                        setHoverNode(node || null);
                        document.body.style.cursor = node ? 'pointer' : 'default';
                    }}
                    onNodeClick={(node: any) => {
                        // Fly to node
                        const distance = 40;
                        const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

                        graphRef.current?.cameraPosition(
                            { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
                            node,
                            2000
                        );
                    }}
                />
            </div>

            {/* HUD / Side Panel - "Scientific" Data Display */}
            <div className="absolute right-0 top-0 bottom-0 w-80 bg-black/80 backdrop-blur-xl border-l border-white/10 p-6 flex flex-col pointer-events-none md:pointer-events-auto">
                <div className="mb-6 border-b border-white/10 pb-4">
                    <h3 className="text-primary font-bold text-lg tracking-widest font-mono">NET-ANALYZER</h3>
                    <div className="flex items-center gap-2 mt-2">
                        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
                        <span className="text-xs text-muted-foreground uppercase">Live Stream Active</span>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto">
                    {hoverNode ? (
                        <div className="space-y-6 animate-in slide-in-from-right duration-300">
                            <div>
                                <span className="text-xs text-muted-foreground uppercase block mb-1">Node ID</span>
                                <span className="text-2xl font-mono text-white">{hoverNode.id}</span>
                            </div>

                            <div>
                                <span className="text-xs text-muted-foreground uppercase block mb-1">Label</span>
                                <span className="text-lg font-bold text-primary">{hoverNode.label}</span>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                                    <span className="text-[10px] text-muted-foreground uppercase block">Degree</span>
                                    <span className="text-xl font-mono text-secondary">{hoverNode.val}</span>
                                </div>
                                <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                                    <span className="text-[10px] text-muted-foreground uppercase block">Centrality</span>
                                    <span className="text-xl font-mono text-pink-500">{(hoverNode.centrality || 0).toFixed(3)}</span>
                                </div>
                            </div>

                            <div className="bg-white/5 p-4 rounded-lg border border-white/5 mt-4">
                                <span className="text-[10px] text-muted-foreground uppercase block mb-2">Topology Analysis</span>
                                <div className="h-1 bg-white/10 w-full rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-primary to-secondary" style={{ width: `${Math.min(100, (hoverNode.val || 1) * 10)}%` }}></div>
                                </div>
                                <p className="text-xs text-muted-foreground mt-2">
                                    Node exhibits {(hoverNode.val || 0) > 4 ? "High" : "Moderate"} connectivity within the Ring25 substructure.
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
                            <div className="h-16 w-16 border-2 border-dashed border-white/20 rounded-full animate-spin-slow mb-4"></div>
                            <p className="text-sm font-mono text-muted-foreground">SCANNING NETWORK...</p>
                            <p className="text-xs text-muted-foreground mt-2">Hover over nodes to extract data</p>
                        </div>
                    )}
                </div>

                <div className="mt-auto border-t border-white/10 pt-4">
                    <div className="grid grid-cols-3 gap-2 text-center text-[10px] font-mono text-muted-foreground">
                        <div>
                            <span className="block text-white">25</span>
                            NODES
                        </div>
                        <div>
                            <span className="block text-white">50</span>
                            LINKS
                        </div>
                        <div>
                            <span className="block text-white">0.5</span>
                            CLUSTERING
                        </div>
                    </div>
                </div>
            </div>

            {/* Overlay UI */}
            <div className="absolute top-4 left-4 pointer-events-none">
                <div className="glass px-4 py-2 rounded-lg border border-white/10">
                    <p className="text-[10px] text-muted-foreground font-mono">VIEWPORT: 3D_FORCE</p>
                </div>
            </div>
        </div>
    );
}
