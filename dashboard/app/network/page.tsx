import NetworkGraph from "@/components/viz/NetworkGraph";

export default function NetworkPage() {
    return (
        <div className="space-y-4">
            <div className="flex flex-col space-y-2">
                <h2 className="text-3xl font-bold tracking-tight text-secondary">Network Topology</h2>
                <p className="text-muted-foreground">
                    3D Force-directed graph of the Ring25 network. Drag nodes to rearrange.
                </p>
            </div>
            <NetworkGraph />
        </div>
    );
}
