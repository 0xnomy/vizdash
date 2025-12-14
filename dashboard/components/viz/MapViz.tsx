"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

// Dynamically import the inner component with SSR disabled
const MapInner = dynamic(() => import("./MapInner"), {
    ssr: false,
    loading: () => <div className="text-center p-10 text-primary animate-pulse">Loading Map Engine...</div>
});

export default function MapViz() {
    const [geoData, setGeoData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        console.log("Fetching map data...");
        fetch("/data/cities.json")
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then((data) => {
                console.log("Map data loaded:", data);
                setGeoData(data);
            })
            .catch((err) => {
                console.error("Failed to load map data:", err);
                setError(err.message);
            });
    }, []);

    if (error) {
        return (
            <div className="h-[600px] w-full flex items-center justify-center border border-red-500/50 rounded-xl bg-red-950/20">
                <div className="text-center text-red-500">
                    <p className="font-bold">Error Loading Map Data</p>
                    <p className="text-sm">{error}</p>
                </div>
            </div>
        );
    }

    if (!geoData) return <div className="h-[600px] w-full flex items-center justify-center border border-white/10 rounded-xl glass-card text-primary animate-pulse">Initializing Geospatial Uplink...</div>;

    return (
        <div className="h-[600px] w-full rounded-xl overflow-hidden border border-white/10 glass-card relative z-0">
            <MapInner data={geoData} />
        </div>
    );
}
