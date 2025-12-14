import MapViz from "@/components/viz/MapViz";

export default function MapPage() {
    return (
        <div className="space-y-4">
            <div className="flex flex-col space-y-2">
                <h2 className="text-3xl font-bold tracking-tight text-pink-500">Global Demographics</h2>
                <p className="text-muted-foreground">
                    Geospatial distribution of major world cities.
                </p>
            </div>
            <MapViz />
        </div>
    );
}
