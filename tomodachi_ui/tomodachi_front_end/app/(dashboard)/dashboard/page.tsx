import PredictionForm from "@/components/predictionForm";

export default function Dashboard() {
    return (
        <section className="max-w-4xl mx-auto p-4 sm:p-6 md:p-8">
            <h1 className="text-center font-bold text-2xl">Try predict some <span className="font-italic text-gray-500">Power Output</span></h1>
            <div className="bg-white shadow rounded-lg p-4 sm:p-6 md:p-8">
                <PredictionForm />
            </div>
        </section>
    );
}