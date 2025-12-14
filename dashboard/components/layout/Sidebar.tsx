"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    Network,
    Trees,
    Map as MapIcon,
    Home,
    Menu,
    X
} from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const navItems = [
    { href: "/", label: "Overview", icon: Home },
    { href: "/tree", label: "Tree of Life", icon: Trees },
    { href: "/network", label: "Network Graph", icon: Network },
    { href: "/map", label: "World Map", icon: MapIcon },
];

export function Sidebar() {
    const pathname = usePathname();
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            {/* Mobile Toggle */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="fixed top-4 right-4 z-50 p-2 md:hidden bg-background/80 backdrop-blur-md rounded-md border border-border"
            >
                {isOpen ? <X /> : <Menu />}
            </button>

            {/* Sidebar Container */}
            <aside className={cn(
                "fixed inset-y-0 left-0 z-40 w-64 transform transition-transform duration-300 ease-in-out md:translate-x-0 bg-background/50 backdrop-blur-xl border-r border-border/50",
                isOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="flex h-full flex-col px-3 py-4 md:px-2">
                    <div className="mb-10 flex items-center justify-center px-2 py-4">
                        <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent text-center leading-tight">
                            VISUALIZE<br /><span className="text-foreground">ANYTHING</span>
                        </h1>
                    </div>

                    <nav className="flex-1 space-y-2">
                        {navItems.map((item) => {
                            const Icon = item.icon;
                            const isActive = pathname === item.href;

                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setIsOpen(false)}
                                    className={cn(
                                        "group flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition-all duration-200",
                                        isActive
                                            ? "bg-primary/10 text-primary shadow-[0_0_20px_rgba(0,240,255,0.15)] border border-primary/20"
                                            : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
                                    )}
                                >
                                    <Icon className={cn("h-5 w-5 transition-transform group-hover:scale-110", isActive ? "text-primary" : "text-muted-foreground group-hover:text-primary")} />
                                    {item.label}
                                    {isActive && (
                                        <motion.div
                                            layoutId="active-nav"
                                            className="absolute left-0 w-1 h-8 bg-primary rounded-r-full"
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                        />
                                    )}
                                </Link>
                            );
                        })}
                    </nav>

                    <div className="mt-auto px-4 py-6 border-t border-border/50">
                        <p className="text-xs text-center text-muted-foreground">
                            Data Visualization<br />
                            Dr. Farah Saeed<br />
                            GIKI
                        </p>
                    </div>
                </div>
            </aside>
        </>
    );
}
