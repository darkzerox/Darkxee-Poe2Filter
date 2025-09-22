'use client'

import { Filter, Download, Upload, Settings, Play } from 'lucide-react'

export default function SimpleTest() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative max-w-4xl mx-auto p-8">
        <h1 className="text-display text-gradient mb-8 text-center text-glow animate-fade-in">
          🎮 Modern UI Test Page
        </h1>
        
        {/* Test Icons */}
        <div className="grid grid-auto-fit gap-6 mb-12 animate-scale-in">
          <div className="card-glass p-6 text-center hover-lift group">
            <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-glow">
              <Filter className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-semibold">Filter Icon</p>
            <p className="text-gray-400 text-sm mt-1">Modern gradient background</p>
          </div>
          
          <div className="card-glass p-6 text-center hover-lift group">
            <div className="w-16 h-16 gradient-success rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-glow">
              <Download className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-semibold">Download Icon</p>
            <p className="text-gray-400 text-sm mt-1">Success gradient</p>
          </div>
          
          <div className="card-glass p-6 text-center hover-lift group">
            <div className="w-16 h-16 gradient-secondary rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-glow">
              <Upload className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-semibold">Upload Icon</p>
            <p className="text-gray-400 text-sm mt-1">Secondary gradient</p>
          </div>
          
          <div className="card-glass p-6 text-center hover-lift group">
            <div className="w-16 h-16 gradient-warning rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-glow">
              <Settings className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-semibold">Settings Icon</p>
            <p className="text-gray-400 text-sm mt-1">Warning gradient</p>
          </div>
          
          <div className="card-glass p-6 text-center hover-lift group">
            <div className="w-16 h-16 gradient-danger rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-glow">
              <Play className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-semibold">Play Icon</p>
            <p className="text-gray-400 text-sm mt-1">Danger gradient</p>
          </div>
        </div>

        {/* Test Colors */}
        <div className="grid grid-auto-fit gap-6 mb-12 animate-slide-in">
          <div className="card-glass p-6 text-center hover-lift">
            <div className="w-full h-20 gradient-primary rounded-xl mb-4 shadow-glow"></div>
            <p className="text-white font-semibold">Primary Gradient</p>
            <p className="text-gray-400 text-sm">Blue to Purple</p>
          </div>
          <div className="card-glass p-6 text-center hover-lift">
            <div className="w-full h-20 gradient-success rounded-xl mb-4 shadow-glow"></div>
            <p className="text-white font-semibold">Success Gradient</p>
            <p className="text-gray-400 text-sm">Teal to Green</p>
          </div>
          <div className="card-glass p-6 text-center hover-lift">
            <div className="w-full h-20 gradient-secondary rounded-xl mb-4 shadow-glow"></div>
            <p className="text-white font-semibold">Secondary Gradient</p>
            <p className="text-gray-400 text-sm">Pink to Red</p>
          </div>
          <div className="card-glass p-6 text-center hover-lift">
            <div className="w-full h-20 gradient-accent rounded-xl mb-4 shadow-glow"></div>
            <p className="text-white font-semibold">Accent Gradient</p>
            <p className="text-gray-400 text-sm">Cyan to Blue</p>
          </div>
        </div>

        {/* Test Buttons */}
        <div className="flex flex-wrap gap-6 justify-center mb-12 animate-fade-in">
          <button className="group btn-primary shadow-glow-lg hover-glow">
            <span className="group-hover:scale-110 transition-transform">Primary Button</span>
          </button>
          <button className="group btn-secondary hover-glow">
            <span className="group-hover:scale-110 transition-transform">Secondary Button</span>
          </button>
          <button className="group btn-outline hover-glow">
            <span className="group-hover:scale-110 transition-transform">Outline Button</span>
          </button>
          <button className="group btn-ghost hover-glow">
            <span className="group-hover:scale-110 transition-transform">Ghost Button</span>
          </button>
        </div>

        {/* Test Cards */}
        <div className="grid grid-auto-fit gap-6 mb-12">
          <div className="card-modern p-6 hover-lift">
            <h3 className="text-heading text-white mb-3">Modern Card</h3>
            <p className="text-body text-gray-300 mb-4">
              This is a modern card with glass effect and hover animations.
            </p>
            <div className="flex items-center text-blue-400 text-sm font-medium">
              <span>Learn more</span>
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
          
          <div className="card-glass p-6 hover-lift">
            <h3 className="text-heading text-white mb-3">Glass Card</h3>
            <p className="text-body text-gray-300 mb-4">
              This card uses the glass effect with backdrop blur and transparency.
            </p>
            <div className="flex items-center text-purple-400 text-sm font-medium">
              <span>Learn more</span>
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>

        {/* Test Inputs */}
        <div className="card-glass p-8 mb-12">
          <h3 className="text-heading text-white mb-6">Modern Inputs</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Text Input
              </label>
              <input
                type="text"
                placeholder="Enter text here..."
                className="input-modern focus-modern"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Select Input
              </label>
              <select className="input-modern focus-modern">
                <option>Option 1</option>
                <option>Option 2</option>
                <option>Option 3</option>
              </select>
            </div>
          </div>
        </div>

        {/* Status */}
        <div className="text-center animate-fade-in">
          <div className="inline-flex items-center space-x-3 bg-gradient-to-r from-green-500/20 to-emerald-500/20 px-6 py-4 rounded-2xl border border-green-500/30">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-green-400 font-semibold text-lg">All modern styles are working perfectly!</span>
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>
  )
}