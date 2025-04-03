"use client";

import React from "react";
import ChatInterface from "@/components/ChatInterface";

export default function AssessmentPage() {
  return (
    <main className="min-h-screen bg-gray-600">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            Communication Assessment
          </h1>
          <p className="text-lg text-gray-300">
            Speak or type to begin your assessment. Our AI will analyze your
            communication skills and provide detailed feedback.
          </p>
        </div>

        <div className="bg-black rounded-xl shadow-lg overflow-hidden border border-gray-800">
          <ChatInterface />
        </div>
      </div>
    </main>
  );
}
