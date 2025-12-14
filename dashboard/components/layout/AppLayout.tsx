import { Sidebar } from "./Sidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex min-h-screen flex-col md:flex-row">
            <Sidebar />
            <main className="flex-1 md:ml-64 min-h-screen p-4 md:p-8 overflow-x-hidden">
                <div className="mx-auto max-w-7xl animate-in fade-in zoom-in duration-500">
                    {children}
                </div>
            </main>
        </div>
    );
}
