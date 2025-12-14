"use client";

import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useEffect } from "react";

// Fix for default markers
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface MapInnerProps {
    data: any;
}

export default function MapInner({ data }: MapInnerProps) {
    if (!data) return null;

    return (
        <MapContainer
            center={[20, 0]}
            zoom={2}
            scrollWheelZoom={true}
            style={{ height: "100%", width: "100%", background: "#05050A" }}
        >
            <TileLayer
                attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />

            {data.features.map((feature: any, index: number) => {
                const { coordinates } = feature.geometry;
                const { city, country, population, capital } = feature.properties;

                const radius = Math.max(3, Math.log10(population || 1) * 2);
                const color = capital === 'primary' ? '#FF0055' : '#00F0FF';

                return (
                    <CircleMarker
                        key={index}
                        center={[coordinates[1], coordinates[0]]}
                        pathOptions={{
                            color: color,
                            fillColor: color,
                            fillOpacity: 0.6,
                            weight: 0
                        }}
                        radius={radius}
                    >
                        <Popup className="glass-popup">
                            <div className="p-2 min-w-[150px]">
                                <h3 className="font-bold text-black text-lg">{city}</h3>
                                <p className="text-xs text-black uppercase tracking-wider">{country}</p>
                                <div className="mt-2 h-0.5 w-full bg-black/10"></div>
                                <p className="text-sm font-mono text-black mt-2">POP: {population.toLocaleString()}</p>
                            </div>
                        </Popup>
                    </CircleMarker>
                );
            })}
        </MapContainer>
    );
}
