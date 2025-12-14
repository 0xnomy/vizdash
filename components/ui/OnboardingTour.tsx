"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronRight, ChevronLeft, Info } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { cn } from "@/lib/utils";

const tourSteps = [
    {
        title: "Welcome, Dr. Farah Saeed",
        content: (
            <div className="space-y-4">
                <p className="text-lg">
                    Welcome to the <strong>Visualize Anything</strong> Dashboard.
                </p>
                <p className="text-muted-foreground">
                    This is the interactive companion to the Data Visualization assignment for GIKI.
                    While the report covers the theory, this dashboard allows you to <strong>explore the results dynamically</strong>.
                </p>
                <p className="text-sm text-primary/80 italic">
                    "Let me guide you through the datasets and visualizations implemented in this project."
                </p>
            </div>
        )
    },
    {
        title: "Interactive Guide",
        content: (
            <div className="space-y-4">
                <p>
                    Unlike static plots, every visualization here is <strong>live</strong>.
                </p>
                <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
                    <li><strong>Zoom & Pan:</strong> Use your mouse/trackpad to navigate 3D spaces and maps.</li>
                    <li><strong>Click to Expand:</strong> Drill down into data hierarchies.</li>
                    <li><strong>Hover for Details:</strong> Reveal hidden metrics like population or centrality.</li>
                </ul>
                <p className="mt-4 text-sm bg-white/5 p-3 rounded border border-white/10">
                    The results here may look different from the report because they are rendered in real-time!
                </p>
            </div>
        )
    },
    {
        title: "1. Tree of Life Dataset",
        content: (
            <div className="space-y-3">
                <div className="bg-primary/10 text-primary px-2 py-1 rounded text-xs w-fit">Phylogenetic Tree</div>
                <p className="text-sm">
                    A large-scale phylogenetic tree with <strong>~36,000 biological species</strong>.
                </p>
                <div className="text-xs text-muted-foreground space-y-2 border-t border-white/10 pt-2">
                    <p><strong>Source:</strong> <a href="https://www.kaggle.com/datasets/konivat/tree-of-life/data" target="_blank" className="underline hover:text-primary">Tree of Life Web Project</a></p>
                    <p><strong>Structure:</strong> Life → Domain → Kingdom → ... → Species</p>
                    <p><strong>Visualization:</strong> We use a <strong>Zoomable Sunburst</strong>. Click arcs to dive deeper into the taxonomy.</p>
                </div>
            </div>
        )
    },
    {
        title: "2. Graph / Network Dataset",
        content: (
            <div className="space-y-3">
                <div className="bg-secondary/10 text-secondary px-2 py-1 rounded text-xs w-fit">Social & Economic Networks</div>
                <p className="text-sm">
                    Based on the <strong>Ring25</strong> and <strong>Social Exchange</strong> datasets. It represents relationships between entities using nodes and edges.
                </p>
                <div className="text-xs text-muted-foreground space-y-2 border-t border-white/10 pt-2">
                    <p><strong>Source:</strong> <a href="https://www.kaggle.com/datasets/mateuscco/toy-network-datasets" target="_blank" className="underline hover:text-primary">Stanford (Matthew Jackson et al.)</a></p>
                    <p><strong>Metrics:</strong> Degree Centrality, Clustering Coefficient.</p>
                    <p><strong>Visualization:</strong> An interactive <strong>3D Force-Directed Graph</strong>. Nodes glow based on importance. Use the HUD to analyze connectivity.</p>
                </div>
            </div>
        )
    },
    {
        title: "3. World Cities Database",
        content: (
            <div className="space-y-3">
                <div className="bg-pink-500/10 text-pink-500 px-2 py-1 rounded text-xs w-fit">Geospatial Dataset</div>
                <p className="text-sm">
                    Contains information on <strong>48,000+ cities</strong> (Filtered to major cities for this web demo).
                </p>
                <div className="text-xs text-muted-foreground space-y-2 border-t border-white/10 pt-2">
                    <p><strong>Source:</strong> <a href="https://www.kaggle.com/datasets/juanmah/world-cities" target="_blank" className="underline hover:text-primary">SimpleMaps – World Cities Database</a></p>
                    <p><strong>Attributes:</strong> Population, Coordinates, Capital Status.</p>
                    <p><strong>Visualization:</strong> A dark-mode <strong>Interactive Map</strong>. Capitals are highlighted in Neon Red. Markers scale with population.</p>
                </div>
            </div>
        )
    },
    {
        title: "Ready to Explore?",
        content: (
            <div className="space-y-4 text-center">
                <p className="text-lg">
                    You are now ready to explore the <strong>Visualize Anything</strong> dashboard.
                </p>
                <div className="flex justify-center">
                    <div className="h-16 w-16 bg-gradient-to-tr from-primary to-secondary rounded-full animate-pulse blur-xl absolute opacity-20"></div>
                    <Info className="h-12 w-12 text-primary relative z-10" />
                </div>
                <p className="text-muted-foreground">
                    Click "Finish" to enter the dashboard.
                </p>
            </div>
        )
    }
];

export function OnboardingTour() {
    const [isOpen, setIsOpen] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);

    useEffect(() => {
        // Check local storage to see if tour has been shown
        const hasSeenTour = localStorage.getItem("hasSeenOnboarding_v2");
        if (!hasSeenTour) {
            // Small delay for effect
            setTimeout(() => setIsOpen(true), 1000);
        }
    }, []);

    const handleNext = () => {
        if (currentStep < tourSteps.length - 1) {
            setCurrentStep(prev => prev + 1);
        } else {
            handleClose();
        }
    };

    const handlePrev = () => {
        if (currentStep > 0) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleClose = () => {
        setIsOpen(false);
        localStorage.setItem("hasSeenOnboarding_v2", "true");
    };

    const handleReset = () => {
        setCurrentStep(0);
        setIsOpen(true);
    };

    // Expose reset trigger via window for testing (optional)
    useEffect(() => {
        (window as any).resetTour = handleReset;
    }, []);

    if (!isOpen) return (
        <button
            onClick={handleReset}
            className="fixed bottom-4 right-4 z-50 p-2 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-colors text-xs text-muted-foreground flex items-center gap-2"
        >
            <Info className="w-4 h-4" /> Relive Tour
        </button>
    );

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="w-full max-w-lg"
            >
                <Card className="border-primary/20 bg-[#0A0A12]/95 shadow-2xl shadow-primary/10">
                    {/* Header */}
                    <div className="p-6 border-b border-white/10 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                            <span className="text-xs font-mono text-primary uppercase tracking-widest">Guide System</span>
                        </div>
                        <button onClick={handleClose} className="text-muted-foreground hover:text-white transition-colors">
                            <X className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Content */}
                    <div className="p-8 min-h-[300px] flex flex-col">
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={currentStep}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.2 }}
                                className="flex-1"
                            >
                                <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
                                    {tourSteps[currentStep].title}
                                </h2>
                                <div className="text-muted-foreground leading-relaxed">
                                    {tourSteps[currentStep].content}
                                </div>
                            </motion.div>
                        </AnimatePresence>
                    </div>

                    {/* Footer / Controls */}
                    <div className="p-6 border-t border-white/10 flex justify-between items-center bg-white/5">
                        <div className="flex gap-1">
                            {tourSteps.map((_, idx) => (
                                <div
                                    key={idx}
                                    className={cn(
                                        "h-1.5 rounded-full transition-all duration-300",
                                        idx === currentStep ? "w-6 bg-primary" : "w-1.5 bg-white/20"
                                    )}
                                />
                            ))}
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={handlePrev}
                                disabled={currentStep === 0}
                                className={cn(
                                    "px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                                    currentStep === 0 ? "text-muted-foreground/50 cursor-not-allowed" : "text-white hover:bg-white/10"
                                )}
                            >
                                Back
                            </button>
                            <button
                                onClick={handleNext}
                                className="px-6 py-2 rounded-lg bg-primary hover:bg-primary/90 text-black font-bold text-sm transition-all flex items-center gap-2 group"
                            >
                                {currentStep === tourSteps.length - 1 ? "Finish" : "Next"}
                                {currentStep !== tourSteps.length - 1 && <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />}
                            </button>
                        </div>
                    </div>
                </Card>
            </motion.div>
        </div>
    );
}
