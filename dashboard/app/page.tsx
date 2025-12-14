import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import Link from "next/link";
import { ArrowRight, Network, Trees, Map as MapIcon, Database } from "lucide-react";

import { OnboardingTour } from "@/components/ui/OnboardingTour";

export default function Home() {
  return (
    <div className="space-y-8">
      <OnboardingTour />
      <div className="flex flex-col space-y-2">
        <h2 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent w-fit">
          Visualize Anything
        </h2>
        <p className="text-muted-foreground text-lg">
          Course Assignment: <strong>Data Visualization</strong> | Instructor: <strong>Dr. Farah Saeed (GIKI)</strong>
        </p>
        <p className="text-muted-foreground">
          Explore complex datasets through interactive visualizations.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Tree Card */}
        <Link href="/tree" className="group">
          <Card className="h-full transition-all group-hover:border-primary/50 group-hover:shadow-[0_0_30px_rgba(0,240,255,0.1)]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Tree of Life</CardTitle>
              <Trees className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">35,960</div>
              <p className="text-xs text-muted-foreground">Phylogenetic Nodes</p>
              <div className="mt-4 flex items-center text-sm text-primary opacity-0 -translate-x-2 transition-all group-hover:opacity-100 group-hover:translate-x-0">
                Data Exploration <ArrowRight className="ml-2 h-4 w-4" />
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Network Card */}
        <Link href="/network" className="group">
          <Card className="h-full transition-all group-hover:border-secondary/50 group-hover:shadow-[0_0_30px_rgba(112,0,255,0.1)]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Network Graph</CardTitle>
              <Network className="h-4 w-4 text-muted-foreground group-hover:text-secondary transition-colors" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Ring25</div>
              <p className="text-xs text-muted-foreground">Topology Analysis</p>
              <div className="mt-4 flex items-center text-sm text-secondary opacity-0 -translate-x-2 transition-all group-hover:opacity-100 group-hover:translate-x-0">
                Visualize Connections <ArrowRight className="ml-2 h-4 w-4" />
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Map Card */}
        <Link href="/map" className="group">
          <Card className="h-full transition-all group-hover:border-pink-500/50 group-hover:shadow-[0_0_30px_rgba(255,0,85,0.1)]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">World Cities</CardTitle>
              <MapIcon className="h-4 w-4 text-muted-foreground group-hover:text-pink-500 transition-colors" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">New York</div>
              <p className="text-xs text-muted-foreground">Geospatial Distribution</p>
              <div className="mt-4 flex items-center text-sm text-pink-500 opacity-0 -translate-x-2 transition-all group-hover:opacity-100 group-hover:translate-x-0">
                View Global Map <ArrowRight className="ml-2 h-4 w-4" />
              </div>
            </CardContent>
          </Card>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>System Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm text-muted-foreground">Datasets Loaded</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm text-muted-foreground">Visualization Engine Ready</span>
            </div>
            <div className="flex items-center space-x-2">
              <Database className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Source: CSV/Net/GeoJSON</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
