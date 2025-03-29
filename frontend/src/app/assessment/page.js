"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Mic, Type, Play, Pause, Save, CheckCircle } from 'lucide-react';

// Text Correction Utility
const correctText = (input) => {
  if (!input) return '';
  
  // Basic correction rules
  let corrected = input
    // Capitalize first letter of the sentence
    .replace(/^([a-z])/, (match) => match.toUpperCase())
    
    // Capitalize 'I'
    .replace(/\bi\b/gi, 'I')
    
    // Add proper spacing after punctuation
    .replace(/([.,!?])(\S)/g, '$1 $2')
    
    // Remove extra spaces
    .replace(/\s+/g, ' ')
    .trim();
  
  // Simple grammar and common mistake corrections
  const corrections = [
    { wrong: /\bi am\b/gi, right: 'I am' },
    { wrong: /\bam fine\b/gi, right: 'am good' },
    { wrong: /\bis working good\b/gi, right: 'is working well' },
    { wrong: /\bwent in\b/gi, right: 'went to' },
  ];
  
  corrections.forEach(({ wrong, right }) => {
    corrected = corrected.replace(wrong, right);
  });

  // Add ending punctuation if missing
  if (!/[.!?]$/.test(corrected)) {
    corrected += '.';
  }

  return corrected;
};

export default function CompleteEnglishAssessmentPage() {
  // State management
  const [answerMode, setAnswerMode] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioRecording, setAudioRecording] = useState(null);
  const [textAnswer, setTextAnswer] = useState('');
  const [correctedText, setCorrectedText] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState({
    id: 1,
    text: "Describe a challenging situation you've faced at work or in your personal life and how you overcame it.",
    category: 'Problem-Solving Communication'
  });

  // Audio recording references
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Real-time text correction
  useEffect(() => {
    if (answerMode !== 'text') return;
    
    // Debounce correction to avoid constant re-rendering
    const timeoutId = setTimeout(() => {
      const corrected = correctText(textAnswer);
      setCorrectedText(corrected !== textAnswer ? corrected : '');
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [textAnswer, answerMode]);

  // Handle text input
  const handleTextInput = (e) => {
    setTextAnswer(e.target.value);
  };

  // Apply correction
  const applyCorrection = () => {
    setTextAnswer(correctedText);
    setCorrectedText('');
  };

  // Handle audio recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioRecording(URL.createObjectURL(audioBlob));
        audioChunksRef.current = [];
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Unable to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Handle answer mode selection
  const selectAnswerMode = (mode) => {
    setAnswerMode(mode);
    // Reset previous answers
    setTextAnswer('');
    setCorrectedText('');
    setAudioRecording(null);
  };

  // Save answer and proceed
  const saveAnswer = () => {
    // In a real application, this would send the answer to a backend
    console.log('Saving answer:', {
      questionId: currentQuestion.id,
      answerMode,
      textAnswer: answerMode === 'text' ? textAnswer : null,
      audioRecording: answerMode === 'audio' ? audioRecording : null
    });
    // TODO: Implement next question logic or submission
    alert('Answer saved! Proceeding to next question...');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
        {/* Question Section */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-gray-500">
              Question {currentQuestion.id}
            </span>
            <span className="text-sm text-blue-600">
              {currentQuestion.category}
            </span>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            {currentQuestion.text}
          </h2>
        </div>

        {/* Answer Mode Selection */}
        {!answerMode && (
          <div className="grid grid-cols-2 gap-4 mb-6">
            <button 
              onClick={() => selectAnswerMode('text')}
              className="flex items-center justify-center p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition"
            >
              <Type className="mr-2 text-blue-600" />
              <span className="font-semibold text-blue-600">Text Answer</span>
            </button>
            <button 
              onClick={() => selectAnswerMode('audio')}
              className="flex items-center justify-center p-4 border-2 border-green-500 rounded-lg hover:bg-green-50 transition"
            >
              <Mic className="mr-2 text-green-600" />
              <span className="font-semibold text-green-600">Audio Answer</span>
            </button>
          </div>
        )}

        {/* Text Answer Mode */}
        {answerMode === 'text' && (
          <div className="space-y-4">
            <textarea 
              className="w-full h-48 p-4 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
              placeholder="Type your answer here..."
              value={textAnswer}
              onChange={handleTextInput}
            />

            {/* Text Correction Suggestion */}
            {correctedText && correctedText !== textAnswer && (
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 flex items-center justify-between">
                <div>
                  <p className="text-blue-800 font-semibold">Suggested Correction:</p>
                  <p className="text-blue-700">{correctedText}</p>
                </div>
                <button 
                  onClick={applyCorrection}
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition flex items-center"
                >
                  <CheckCircle className="mr-2" />
                  Apply
                </button>
              </div>
            )}

            {/* Save Button for Text Mode */}
            {textAnswer.trim() !== '' && (
              <div className="text-center">
                <button 
                  onClick={saveAnswer}
                  className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition flex items-center mx-auto"
                >
                  <Save className="mr-2" />
                  Save Answer
                </button>
              </div>
            )}
          </div>
        )}

        {/* Audio Answer Mode */}
        {answerMode === 'audio' && (
          <div className="text-center">
            {!isRecording && !audioRecording && (
              <button 
                onClick={startRecording}
                className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition flex items-center mx-auto"
              >
                <Mic className="mr-2" />
                Start Recording
              </button>
            )}

            {isRecording && (
              <div className="flex flex-col items-center">
                <div className="animate-pulse text-red-500 mb-4">
                  Recording...
                </div>
                <button 
                  onClick={stopRecording}
                  className="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition flex items-center"
                >
                  <Pause className="mr-2" />
                  Stop Recording
                </button>
              </div>
            )}

            {audioRecording && (
              <div className="mt-4">
                <audio 
                  src={audioRecording} 
                  controls 
                  className="mx-auto mb-4"
                />
                <div className="flex justify-center space-x-4">
                  <button 
                    onClick={() => setAudioRecording(null)}
                    className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition"
                  >
                    Retake
                  </button>
                  <button 
                    onClick={saveAnswer}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition flex items-center"
                  >
                    <Save className="mr-2" />
                    Save Answer
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Mode Change Option */}
        {answerMode && (
          <div className="mt-4 text-center">
            <button 
              onClick={() => setAnswerMode(null)}
              className="text-blue-600 hover:underline"
            >
              Change Answer Mode
            </button>
          </div>
        )}
      </div>
    </div>
  );
}