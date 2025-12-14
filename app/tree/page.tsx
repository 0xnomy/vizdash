import SunburstTree from "@/components/viz/SunburstTree";

export default function TreePage() {
    return (
        <div className="space-y-4">
            <div className="flex flex-col space-y-2">
                <h2 className="text-3xl font-bold tracking-tight text-primary">Tree of Life</h2>
                <p className="text-muted-foreground">
                    Interactive hierarchical visualization of species evolution. Click segments to zoom.
                </p>
            </div>
            <SunburstTree />
        </div>
    );
}
