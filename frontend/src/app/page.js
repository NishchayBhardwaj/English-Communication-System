import React from 'react';
// import { CheckIcon, GlobeAltIcon, RocketLaunchIcon } from 'lucide-react';
import { CheckIcon, GlobeIcon, RocketIcon } from 'lucide-react';

export default function EnglishAssessmentLandingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">
                EnglishPro Assessment
              </h1>
            </div>
            <div className="flex space-x-4">
              <a href="#features" className="text-gray-700 hover:text-blue-600">Features</a>
              <a href="#pricing" className="text-gray-700 hover:text-blue-600">Pricing</a>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">
                Start Assessment
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative pt-16 pb-32 bg-gradient-to-r from-blue-500 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-extrabold text-white sm:text-5xl">
            Unlock Your English Communication Potential
          </h2>
          <p className="mt-4 max-w-3xl mx-auto text-xl text-blue-100">
            Comprehensive assessment to identify your strengths and areas for improvement in English communication
          </p>
          <div className="mt-10 flex justify-center space-x-4">
            <button className="bg-white text-blue-600 px-6 py-3 rounded-md font-semibold hover:bg-blue-50 transition">
              Take Free Assessment
            </button>
            <button className="bg-transparent border-2 border-white text-white px-6 py-3 rounded-md hover:bg-white hover:text-blue-600 transition">
              Learn More
            </button>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-3xl font-bold text-gray-800">
              Comprehensive Communication Assessment
            </h3>
            <p className="mt-4 text-xl text-gray-600">
              Evaluate your English skills across multiple dimensions
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
            {/* Feature 1 */}
            <div className="bg-gray-50 p-6 rounded-lg shadow-md text-center">
              <GlobeIcon className="mx-auto h-12 w-12 text-blue-600" />
              <h4 className="mt-4 text-xl font-semibold text-gray-800">
                Global Standard Evaluation
              </h4>
              <p className="mt-2 text-gray-600">
                Benchmarked against international communication standards
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-gray-50 p-6 rounded-lg shadow-md text-center">
              <RocketIcon className="mx-auto h-12 w-12 text-blue-600" />
              <h4 className="mt-4 text-xl font-semibold text-gray-800">
                Personalized Learning Path
              </h4>
              <p className="mt-2 text-gray-600">
                Tailored recommendations to improve your communication skills
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-gray-50 p-6 rounded-lg shadow-md text-center">
              <CheckIcon className="mx-auto h-12 w-12 text-blue-600" />
              <h4 className="mt-4 text-xl font-semibold text-gray-800">
                Comprehensive Skill Analysis
              </h4>
              <p className="mt-2 text-gray-600">
                Deep insights into speaking, writing, listening, and reading
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold">EnglishPro Assessment</h2>
            <p className="mt-2 text-gray-400">
              © 2024 All Rights Reserved
            </p>
          </div>
          <div className="flex space-x-4">
            <a href="#" className="text-gray-300 hover:text-white">Privacy</a>
            <a href="#" className="text-gray-300 hover:text-white">Terms</a>
            <a href="#" className="text-gray-300 hover:text-white">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
