"use client";

// import React, { useState } from 'react';
// import {
//   LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
//   PieChart, Pie, Cell
// } from 'recharts';
// import {
//   ChevronUp, ChevronDown, User, BookOpen, Trophy, Clock, Calendar, ArrowRight,
//   Activity, BookOpen as Book, Mic, Type, HelpCircle, Settings
// } from 'lucide-react';

// export default function EnglishAssessmentDashboard() {
//   const [activeSidebar, setActiveSidebar] = useState(true);

//   // Sample data
//   const progressData = [
//     { name: 'Week 1', speaking: 65, writing: 70, listening: 80, reading: 75 },
//     { name: 'Week 2', speaking: 68, writing: 72, listening: 81, reading: 77 },
//     { name: 'Week 3', speaking: 70, writing: 75, listening: 83, reading: 80 },
//     { name: 'Week 4', speaking: 75, writing: 78, listening: 85, reading: 83 },
//     { name: 'Week 5', speaking: 78, writing: 80, listening: 86, reading: 85 },
//     { name: 'Week 6', speaking: 80, writing: 82, listening: 88, reading: 87 },
//   ];

//   const skillBreakdownData = [
//     { name: 'Speaking', value: 78, color: '#4f46e5' },
//     { name: 'Writing', value: 80, color: '#f97316' },
//     { name: 'Listening', value: 88, color: '#10b981' },
//     { name: 'Reading', value: 87, color: '#7c3aed' },
//   ];

//   const COLORS = ['#4f46e5', '#f97316', '#10b981', '#7c3aed'];

//   const upcomingAssessments = [
//     { id: 1, title: 'Business Communication', date: 'Tomorrow, 10:00 AM', type: 'Speaking', difficulty: 'Advanced' },
//     { id: 2, title: 'Academic Writing', date: 'Mar 31, 2:30 PM', type: 'Writing', difficulty: 'Intermediate' },
//     { id: 3, title: 'Presentation Skills', date: 'Apr 3, 11:00 AM', type: 'Speaking', difficulty: 'Advanced' },
//   ];

//   const recentAssessments = [
//     { id: 1, title: 'Job Interview Practice', score: 85, date: 'Mar 27, 2025', improvement: '+3%' },
//     { id: 2, title: 'Email Writing', score: 92, date: 'Mar 25, 2025', improvement: '+5%' },
//     { id: 3, title: 'Listening Comprehension', score: 88, date: 'Mar 22, 2025', improvement: '+2%' },
//   ];

//   return (
//     <div className="flex h-screen bg-gray-100">
//       {/* Sidebar */}
//       <div className={`bg-indigo-800 text-white ${activeSidebar ? 'w-64' : 'w-20'} transition-all duration-300 flex flex-col`}>
//         <div className="p-4 flex items-center justify-between">
//           {activeSidebar && <h1 className="text-xl font-bold">EnglishPro</h1>}
//           <button
//             className="p-2 rounded-full hover:bg-indigo-700"
//             onClick={() => setActiveSidebar(!activeSidebar)}
//           >
//             {activeSidebar ? <ChevronUp /> : <ChevronDown />}
//           </button>
//         </div>

//         <nav className="flex-1 py-4">
//           <ul className="space-y-2">
//             <li>
//               <a href="#" className="flex items-center p-4 bg-indigo-900 text-white hover:bg-indigo-700">
//                 <Activity className="w-5 h-5" />
//                 {activeSidebar && <span className="ml-3">Dashboard</span>}
//               </a>
//             </li>
//             <li>
//               <a href="#" className="flex items-center p-4 text-indigo-200 hover:bg-indigo-700">
//                 <Book className="w-5 h-5" />
//                 {activeSidebar && <span className="ml-3">Assessments</span>}
//               </a>
//             </li>
//             <li>
//               <a href="#" className="flex items-center p-4 text-indigo-200 hover:bg-indigo-700">
//                 <Mic className="w-5 h-5" />
//                 {activeSidebar && <span className="ml-3">Speaking</span>}
//               </a>
//             </li>
//             <li>
//               <a href="#" className="flex items-center p-4 text-indigo-200 hover:bg-indigo-700">
//                 <Type className="w-5 h-5" />
//                 {activeSidebar && <span className="ml-3">Writing</span>}
//               </a>
//             </li>
//             <li>
//               <a href="#" className="flex items-center p-4 text-indigo-200 hover:bg-indigo-700">
//                 <Trophy className="w-5 h-5" />
//                 {activeSidebar && <span className="ml-3">Progress</span>}
//               </a>
//             </li>
//           </ul>
//         </nav>

//         <div className="p-4 border-t border-indigo-700">
//           <div className="flex items-center">
//             <User className="w-8 h-8 rounded-full bg-indigo-600 p-1" />
//             {activeSidebar && <span className="ml-3">John Davis</span>}
//           </div>
//           {activeSidebar && (
//             <div className="mt-2">
//               <p className="text-xs text-indigo-300">Advanced Level • Plan: Pro</p>
//             </div>
//           )}
//         </div>
//       </div>

//       {/* Main Content */}
//       <div className="flex-1 overflow-y-auto">
//         {/* Header */}
//         <header className="bg-white shadow-sm">
//           <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
//             <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>

//             <div className="flex items-center space-x-4">
//               <button className="p-2 text-gray-500 hover:text-gray-700">
//                 <HelpCircle className="w-5 h-5" />
//               </button>
//               <button className="p-2 text-gray-500 hover:text-gray-700">
//                 <Settings className="w-5 h-5" />
//               </button>
//             </div>
//           </div>
//         </header>

//         {/* Dashboard Content */}
//         <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
//           {/* Score Summary */}
//           <div className="grid grid-cols-1 gap-6 md:grid-cols-4 mb-6">
//             <div className="bg-white overflow-hidden shadow rounded-lg">
//               <div className="px-4 py-5 sm:p-6">
//                 <div className="flex items-center">
//                   <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
//                     <Trophy className="h-6 w-6 text-white" />
//                   </div>
//                   <div className="ml-5 w-0 flex-1">
//                     <dl>
//                       <dt className="text-sm font-medium text-gray-500">Overall Score</dt>
//                       <dd>
//                         <div className="text-lg font-medium text-gray-900">83/100</div>
//                       </dd>
//                     </dl>
//                   </div>
//                 </div>
//               </div>
//             </div>

//             <div className="bg-white overflow-hidden shadow rounded-lg">
//               <div className="px-4 py-5 sm:p-6">
//                 <div className="flex items-center">
//                   <div className="flex-shrink-0 bg-orange-500 rounded-md p-3">
//                     <BookOpen className="h-6 w-6 text-white" />
//                   </div>
//                   <div className="ml-5 w-0 flex-1">
//                     <dl>
//                       <dt className="text-sm font-medium text-gray-500">Completed Assessments</dt>
//                       <dd>
//                         <div className="text-lg font-medium text-gray-900">24</div>
//                       </dd>
//                     </dl>
//                   </div>
//                 </div>
//               </div>
//             </div>

//             <div className="bg-white overflow-hidden shadow rounded-lg">
//               <div className="px-4 py-5 sm:p-6">
//                 <div className="flex items-center">
//                   <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
//                     <Clock className="h-6 w-6 text-white" />
//                   </div>
//                   <div className="ml-5 w-0 flex-1">
//                     <dl>
//                       <dt className="text-sm font-medium text-gray-500">Time Spent</dt>
//                       <dd>
//                         <div className="text-lg font-medium text-gray-900">42 hrs</div>
//                       </dd>
//                     </dl>
//                   </div>
//                 </div>
//               </div>
//             </div>

//             <div className="bg-white overflow-hidden shadow rounded-lg">
//               <div className="px-4 py-5 sm:p-6">
//                 <div className="flex items-center">
//                   <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
//                     <Calendar className="h-6 w-6 text-white" />
//                   </div>
//                   <div className="ml-5 w-0 flex-1">
//                     <dl>
//                       <dt className="text-sm font-medium text-gray-500">Study Streak</dt>
//                       <dd>
//                         <div className="text-lg font-medium text-gray-900">16 days</div>
//                       </dd>
//                     </dl>
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>

//           {/* Charts Section */}
//           <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
//             {/* Progress Chart */}
//             <div className="bg-white shadow rounded-lg lg:col-span-2">
//               <div className="p-6">
//                 <h3 className="text-lg font-medium text-gray-900">Skill Progress</h3>
//                 <div className="mt-2 h-64">
//                   <ResponsiveContainer width="100%" height="100%">
//                     <LineChart
//                       data={progressData}
//                       margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
//                     >
//                       <CartesianGrid strokeDasharray="3 3" />
//                       <XAxis dataKey="name" />
//                       <YAxis domain={[40, 100]} />
//                       <Tooltip />
//                       <Legend />
//                       <Line type="monotone" dataKey="speaking" stroke="#4f46e5" activeDot={{ r: 8 }} />
//                       <Line type="monotone" dataKey="writing" stroke="#f97316" />
//                       <Line type="monotone" dataKey="listening" stroke="#10b981" />
//                       <Line type="monotone" dataKey="reading" stroke="#7c3aed" />
//                     </LineChart>
//                   </ResponsiveContainer>
//                 </div>
//               </div>
//             </div>

//             {/* Skill Breakdown */}
//             <div className="bg-white shadow rounded-lg">
//               <div className="p-6">
//                 <h3 className="text-lg font-medium text-gray-900">Skill Breakdown</h3>
//                 <div className="mt-2 h-64 flex items-center justify-center">
//                   <ResponsiveContainer width="100%" height="100%">
//                     <PieChart>
//                       <Pie
//                         data={skillBreakdownData}
//                         cx="50%"
//                         cy="50%"
//                         labelLine={false}
//                         outerRadius={80}
//                         fill="#8884d8"
//                         dataKey="value"
//                         label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
//                       >
//                         {skillBreakdownData.map((entry, index) => (
//                           <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                         ))}
//                       </Pie>
//                       <Tooltip />
//                     </PieChart>
//                   </ResponsiveContainer>
//                 </div>
//               </div>
//             </div>
//           </div>

//           {/* Bottom Section */}
//           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//             {/* Upcoming Assessments */}
//             <div className="bg-white shadow rounded-lg overflow-hidden">
//               <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
//                 <h3 className="text-lg font-medium text-gray-900">Upcoming Assessments</h3>
//                 <button className="text-indigo-600 hover:text-indigo-900 text-sm font-medium flex items-center">
//                   View All <ArrowRight className="ml-1 w-4 h-4" />
//                 </button>
//               </div>
//               <div className="overflow-hidden">
//                 <ul className="divide-y divide-gray-200">
//                   {upcomingAssessments.map((assessment) => (
//                     <li key={assessment.id} className="px-6 py-4 hover:bg-gray-50">
//                       <div className="flex items-center justify-between">
//                         <div>
//                           <h4 className="text-sm font-medium text-gray-900">{assessment.title}</h4>
//                           <p className="text-sm text-gray-500">{assessment.date}</p>
//                         </div>
//                         <div className="flex flex-col items-end">
//                           <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">{assessment.type}</span>
//                           <span className="mt-1 text-xs text-gray-500">{assessment.difficulty}</span>
//                         </div>
//                       </div>
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             </div>

//             {/* Recent Results */}
//             <div className="bg-white shadow rounded-lg overflow-hidden">
//               <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
//                 <h3 className="text-lg font-medium text-gray-900">Recent Results</h3>
//                 <button className="text-indigo-600 hover:text-indigo-900 text-sm font-medium flex items-center">
//                   View All <ArrowRight className="ml-1 w-4 h-4" />
//                 </button>
//               </div>
//               <div className="overflow-hidden">
//                 <ul className="divide-y divide-gray-200">
//                   {recentAssessments.map((assessment) => (
//                     <li key={assessment.id} className="px-6 py-4 hover:bg-gray-50">
//                       <div className="flex items-center justify-between">
//                         <div>
//                           <h4 className="text-sm font-medium text-gray-900">{assessment.title}</h4>
//                           <p className="text-sm text-gray-500">{assessment.date}</p>
//                         </div>
//                         <div className="flex flex-col items-end">
//                           <span className={`text-base font-medium ${assessment.score >= 90 ? 'text-green-600' : assessment.score >= 80 ? 'text-blue-600' : 'text-orange-600'}`}>
//                             {assessment.score}/100
//                           </span>
//                           <span className="text-xs text-green-500">{assessment.improvement}</span>
//                         </div>
//                       </div>
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             </div>
//           </div>
//         </main>
//       </div>
//     </div>
//   );
// }

// DashboardPage.js
import React, { useState } from "react";
import Link from "next/link";
import {
  BookOpen,
  Mic,
  Calendar,
  Award,
  Clock,
  ArrowUpRight,
  TrendingUp,
  CheckCircle,
} from "lucide-react";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState("overview");

  // Mock data
  //   const upcomingAssessments = [
  //     { id: 1, type: 'Writing', topic: 'Business Communication', date: 'April 2, 2025', time: '10:00 AM' },
  //     { id: 2, type: 'Speaking', topic: 'Presentation Skills', date: 'April 5, 2025', time: '2:30 PM' },
  //   ];

  const recentAssessments = [
    {
      id: 1,
      type: "Writing",
      topic: "Assessment 1",
      score: 87,
      date: "March 25, 2025",
    },
    {
      id: 2,
      type: "Speaking",
      topic: "Assessment 1",
      score: 92,
      date: "March 22, 2025",
    },
    {
      id: 3,
      type: "Writing",
      topic: "Assessment 1",
      score: 78,
      date: "March 18, 2025",
    },
  ];

  const skillMetrics = [
    { skill: "Grammar Accuracy", score: 82 },
    { skill: "Vocabulary Range", score: 75 },
    { skill: "Speaking Fluency", score: 85 },
    { skill: "Pronunciation", score: 88 },
    { skill: "Writing Coherence", score: 79 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">EnglishAssess</h1>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <button className="flex items-center text-gray-700 focus:outline-none">
                <span className="mr-2">Test User</span>
                <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-medium">
                  TU
                </div>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">
                Welcome back, User!
              </h2>
              <p className="text-gray-600 mt-1">
                Continue improving your English communication skills
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Link href="/assessments/writing">
                <button className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                  <BookOpen className="h-4 w-4 mr-2" />
                  Start Assessment
                </button>
              </Link>
              {/* <Link href="/assessments/speaking">
                <button className="inline-flex items-center px-4 py-2 bg-indigo-100 text-indigo-600 rounded-md hover:bg-indigo-200">
                  <Mic className="h-4 w-4 mr-2" />
                  Start Speaking Assessment
                </button>
              </Link> */}
            </div>
          </div>

          {/* Progress Overview */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center">
                <div className="bg-green-100 p-2 rounded-md">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                </div>
                <div className="ml-3">
                  <p className="text-gray-500 text-sm">Overall Progress</p>
                  <p className="font-semibold text-gray-800">85/100</p>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center">
                <div className="bg-blue-100 p-2 rounded-md">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                </div>
                <div className="ml-3">
                  <p className="text-gray-500 text-sm">Writing Score</p>
                  <p className="font-semibold text-gray-800">82/100</p>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center">
                <div className="bg-purple-100 p-2 rounded-md">
                  <Mic className="h-5 w-5 text-purple-600" />
                </div>
                <div className="ml-3">
                  <p className="text-gray-500 text-sm">Speaking Score</p>
                  <p className="font-semibold text-gray-800">88/100</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab("overview")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "overview"
                  ? "border-indigo-500 text-indigo-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab("writing")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "writing"
                  ? "border-indigo-500 text-indigo-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Writing Assessments
            </button>
            <button
              onClick={() => setActiveTab("speaking")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "speaking"
                  ? "border-indigo-500 text-indigo-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Speaking Assessments
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Upcoming Assessments */}
            <div className="lg:col-span-2">
              {/* <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-5 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-800">Upcoming Assessments</h3>
                </div>
                <div className="p-6">
                  {upcomingAssessments.length > 0 ? (
                    <div className="space-y-4">
                      {upcomingAssessments.map((assessment) => (
                        <div key={assessment.id} className="flex items-center justify-between p-4 border border-gray-100 rounded-lg hover:bg-gray-50">
                          <div className="flex items-center">
                            {assessment.type === 'Writing' ? (
                              <div className="bg-blue-100 p-2 rounded-md">
                                <BookOpen className="h-5 w-5 text-blue-600" />
                              </div>
                            ) : (
                              <div className="bg-purple-100 p-2 rounded-md">
                                <Mic className="h-5 w-5 text-purple-600" />
                              </div>
                            )}
                            <div className="ml-4">
                              <p className="font-medium text-gray-800">{assessment.topic}</p>
                              <div className="flex items-center text-sm text-gray-500 mt-1">
                                <Calendar className="h-4 w-4 mr-1" />
                                {assessment.date} • <Clock className="h-4 w-4 mx-1" /> {assessment.time}
                              </div>
                            </div>
                          </div>
                          <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm flex items-center">
                            Prepare <ArrowUpRight className="h-4 w-4 ml-1" />
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-gray-500">No upcoming assessments</p>
                      <button className="mt-2 text-indigo-600 hover:text-indigo-800 font-medium">
                        Schedule an assessment
                      </button>
                    </div>
                  )}
                </div>
              </div> */}

              {/* Recent Assessments */}
              <div className="bg-white rounded-lg shadow mt-6">
                <div className="px-6 py-5 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-800">
                    Recent Assessments
                  </h3>
                </div>
                <div className="p-6">
                  {recentAssessments.map((assessment) => (
                    <div
                      key={assessment.id}
                      className="flex items-center justify-between p-4 border-b border-gray-100 last:border-b-0"
                    >
                      <div className="flex items-center">
                        {assessment.type === "Writing" ? (
                          <div className="bg-blue-100 p-2 rounded-md">
                            <BookOpen className="h-5 w-5 text-blue-600" />
                          </div>
                        ) : (
                          <div className="bg-purple-100 p-2 rounded-md">
                            <Mic className="h-5 w-5 text-purple-600" />
                          </div>
                        )}
                        <div className="ml-4">
                          <p className="font-medium text-gray-800">
                            {assessment.topic}
                          </p>
                          <p className="text-sm text-gray-500 mt-1">
                            {assessment.date}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <div
                          className={`flex items-center justify-center h-10 w-10 rounded-full ${
                            assessment.score >= 90
                              ? "bg-green-100 text-green-800"
                              : assessment.score >= 80
                              ? "bg-blue-100 text-blue-800"
                              : assessment.score >= 70
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          <span className="font-medium text-sm">
                            {assessment.score}
                          </span>
                        </div>
                        <button className="ml-4 text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                          View Details
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Skills Analysis */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-5 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-800">
                  Skills Analysis
                </h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {skillMetrics.map((skill) => (
                    <div key={skill.skill}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">
                          {skill.skill}
                        </span>
                        <span className="text-sm font-medium text-gray-700">
                          {skill.score}/100
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                          className={`h-2.5 rounded-full ${
                            skill.score >= 90
                              ? "bg-green-500"
                              : skill.score >= 80
                              ? "bg-blue-500"
                              : skill.score >= 70
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                          style={{ width: `${skill.score}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-6">
                  <h4 className="font-medium text-gray-800 mb-3">
                    Recommended Focus Areas
                  </h4>
                  <ul className="space-y-2">
                    <li className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 mr-2 text-indigo-500" />
                      Practice complex grammatical structures
                    </li>
                    <li className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 mr-2 text-indigo-500" />
                      Expand academic vocabulary usage
                    </li>
                    <li className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 mr-2 text-indigo-500" />
                      Improve paragraph organization in writing
                    </li>
                  </ul>
                </div>

                <Link href="/progress">
                  <button className="w-full mt-6 inline-flex items-center justify-center px-4 py-2 border border-indigo-600 text-indigo-600 rounded-md hover:bg-indigo-50">
                    View Full Analysis
                  </button>
                </Link>
              </div>
            </div>
          </div>
        )}

        {activeTab === "writing" && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-medium text-gray-800">
                Writing Assessments
              </h3>
              <Link href="/assessments/writing">
                <button className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                  <BookOpen className="h-4 w-4 mr-2" />
                  New Assessment
                </button>
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">Email Writing</h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Business Communication
                  </p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Write a professional email to a client explaining a project
                    delay.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">Essay Writing</h4>
                  <p className="text-sm text-gray-500 mt-1">Academic English</p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Write a persuasive essay on the impact of technology on
                    education.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">Report Writing</h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Professional English
                  </p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Write a detailed report analyzing quarterly sales
                    performance.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "speaking" && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-medium text-gray-800">
                Speaking Assessments
              </h3>
              <Link href="/assessments/speaking">
                <button className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                  <Mic className="h-4 w-4 mr-2" />
                  New Assessment
                </button>
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">
                    Interview Practice
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Professional Communication
                  </p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Practice answering common job interview questions with
                    clarity and confidence.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">
                    Presentation Skills
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">Public Speaking</p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Deliver a 5-minute presentation on a topic of your choice
                    with clear structure.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="p-4 border-b border-gray-200">
                  <h4 className="font-medium text-gray-800">
                    Pronunciation Practice
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">Spoken English</p>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-600 mb-4">
                    Practice challenging English sounds and receive detailed
                    feedback.
                  </p>
                  <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                    Start Assessment
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
