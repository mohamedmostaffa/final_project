import { useNavigate } from "react-router-dom";
import { FileSearch, Plus, ShieldCheck } from "lucide-react";
import Sidebar from "../components/Sidebar";

export default function History() {
    const navigate = useNavigate();

    const history =
        JSON.parse(localStorage.getItem("truthlens-history")) || [];

    return (
        <div className="relative flex min-h-screen bg-[#08111F] overflow-hidden">
            <div className="absolute top-[-300px] left-[350px] w-[700px] h-[700px] rounded-full bg-blue-700 opacity-20 blur-[180px]" />
            <div className="absolute bottom-[-250px] right-[-100px] w-[500px] h-[500px] rounded-full bg-cyan-500 opacity-10 blur-[150px]" />

            <Sidebar />

            <main className="flex-1 relative z-10 overflow-auto px-12 pb-12 pt-2">
                <div className="py-10 flex items-start justify-between gap-6">
                    <div>
                        <p className="text-blue-400 text-sm font-semibold uppercase tracking-widest mb-2">Archive</p>
                        <h1 className="text-5xl font-bold text-white">History</h1>
                        <p className="text-gray-400 mt-3 text-lg">Review previous investigations and their verdicts.</p>
                    </div>

                    <button
                        onClick={() => navigate("/investigate")}
                        className="mt-2 flex items-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 px-5 py-3 rounded-2xl text-white font-semibold shadow-lg shadow-blue-500/30 transition-all"
                    >
                        <Plus size={18} />
                        New Investigation
                    </button>
                </div>

                {history.length === 0 ? (
                    <div className="flex flex-col items-center justify-center mt-32 text-center">
                        <div className="w-20 h-20 rounded-full bg-blue-500/10 flex items-center justify-center mb-6">
                            <FileSearch size={36} className="text-blue-400" />
                        </div>
                        <h2 className="text-white text-2xl font-bold">No investigations yet</h2>
                        <p className="text-gray-400 mt-3">Run your first fact-check to start building history.</p>
                    </div>
                ) : (
                    <div className="space-y-5">
                        {history.map((item, index) => (
                            <div
                                key={index}
                                className="rounded-3xl bg-[#101B31] border border-[#22324B] p-6 shadow-xl"
                            >
                                <div className="flex items-start justify-between gap-6">
                                    <div>
                                        <p className="text-gray-500 text-xs mb-2">
                                            {item.date ? new Date(item.date).toLocaleString() : "Saved investigation"}
                                        </p>
                                        <h3 className="text-white text-xl leading-relaxed">
                                            {item.claim}
                                        </h3>
                                    </div>

                                    <div className="flex items-center gap-2 text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded-full px-3 py-1.5 flex-shrink-0">
                                        <ShieldCheck size={15} />
                                        <span className="text-sm font-semibold">{item.verdict}</span>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4 mt-5">
                                    <span className="text-green-400 text-sm font-semibold">
                                        {item.confidence}% confidence
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
