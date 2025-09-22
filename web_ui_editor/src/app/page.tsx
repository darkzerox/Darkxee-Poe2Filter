'use client'

import Link from 'next/link'
import { Filter, Download, Upload, Settings, Play, Sparkles, Zap, Shield, Star } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      {/* Header */}
      <header className="relative glass-dark border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4 animate-slide-in">
              <div className="relative">
                <div className="w-14 h-14 gradient-primary rounded-2xl flex items-center justify-center shadow-glow">
                  <Filter className="w-7 h-7 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">DZX Filter Editor</h1>
                <p className="text-gray-400 text-sm">Path of Exile 2</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 animate-slide-in">
              <div className="flex items-center space-x-2 bg-blue-500/10 px-4 py-2 rounded-full border border-blue-500/20">
                <Sparkles className="w-4 h-4 text-blue-400" />
                <span className="text-blue-400 text-sm font-medium">v1.0.0</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative max-w-7xl mx-auto px-6 lg:px-8 py-16">
        <div className="text-center mb-20 animate-fade-in">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500/20 to-purple-600/20 px-6 py-3 rounded-full border border-blue-500/30 mb-8">
            <Zap className="w-5 h-5 text-blue-400" />
            <span className="text-blue-400 font-semibold">Next-Generation Filter Editor</span>
          </div>
          
          <h2 className="text-display text-gradient mb-6 text-glow">
            🎮 Advanced Filter Editor
          </h2>
          <p className="text-xl text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed">
            Create, customize, and manage Path of Exile 2 item filters with our powerful web interface.
            Import existing filters, edit rules visually, and export optimized filters for your gameplay.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link 
              href="/editor"
              className="group btn-primary shadow-glow-lg hover-glow"
            >
              <Filter className="w-5 h-5 mr-2 group-hover:rotate-12 transition-transform" />
              Open Filter Editor
            </Link>
            <Link 
              href="/demo"
              className="group btn-outline hover-glow"
            >
              <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
              View Demo
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-auto-fit gap-8 mb-20">
          <div className="card-glass p-8 hover-lift group">
            <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Upload className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-heading text-white mb-4">Import & Export</h3>
            <p className="text-body text-gray-300">
              Import existing .filter files and export your customized filters for use in Path of Exile 2.
            </p>
            <div className="mt-4 flex items-center text-blue-400 text-sm font-medium">
              <span>Learn more</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>

          <div className="card-glass p-8 hover-lift group">
            <div className="w-16 h-16 gradient-secondary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Settings className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-heading text-white mb-4">Visual Editor</h3>
            <p className="text-body text-gray-300">
              Edit colors, fonts, sounds, and icons with an intuitive visual interface. No coding required.
            </p>
            <div className="mt-4 flex items-center text-purple-400 text-sm font-medium">
              <span>Learn more</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>

          <div className="card-glass p-8 hover-lift group">
            <div className="w-16 h-16 gradient-accent rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Play className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-heading text-white mb-4">Realtime Preview</h3>
            <p className="text-body text-gray-300">
              See your changes instantly with our realtime preview system. Test sounds and visual effects.
            </p>
            <div className="mt-4 flex items-center text-cyan-400 text-sm font-medium">
              <span>Learn more</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>

        {/* Quick Start */}
        <div className="card-glass p-10 mb-20">
          <div className="text-center mb-10">
            <h3 className="text-heading text-white mb-4">🚀 Quick Start</h3>
            <p className="text-body text-gray-300 max-w-2xl mx-auto">
              Get started with DZX Filter Editor in minutes. Follow these simple steps to create your first custom filter.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-10">
            <div className="space-modern-sm">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 gradient-primary rounded-xl flex items-center justify-center mr-4">
                  <span className="text-white font-bold">1</span>
                </div>
                <h4 className="text-subheading text-blue-400">For New Users</h4>
              </div>
              <div className="space-y-4 pl-14">
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Click "Open Filter Editor" to start</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Import an existing .filter file or start from scratch</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Customize colors, sounds, and rules visually</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Export your customized filter and use it in-game</span>
                </div>
              </div>
            </div>
            
            <div className="space-modern-sm">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 gradient-secondary rounded-xl flex items-center justify-center mr-4">
                  <Star className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-subheading text-purple-400">For Experienced Users</h4>
              </div>
              <div className="space-y-4 pl-14">
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Advanced rule management and bulk editing</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Category-based organization system</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Backup and restore functionality</span>
                </div>
                <div className="flex items-start">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-4 flex-shrink-0"></div>
                  <span className="text-gray-300">Performance optimization tools</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
          <div className="card-modern p-6 text-center">
            <div className="text-3xl font-bold text-gradient mb-2">1000+</div>
            <div className="text-caption">Active Users</div>
          </div>
          <div className="card-modern p-6 text-center">
            <div className="text-3xl font-bold text-gradient mb-2">50+</div>
            <div className="text-caption">Filter Templates</div>
          </div>
          <div className="card-modern p-6 text-center">
            <div className="text-3xl font-bold text-gradient mb-2">99.9%</div>
            <div className="text-caption">Uptime</div>
          </div>
          <div className="card-modern p-6 text-center">
            <div className="text-3xl font-bold text-gradient mb-2">24/7</div>
            <div className="text-caption">Support</div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative glass-dark border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Shield className="w-5 h-5 text-green-400" />
              <span className="text-green-400 font-semibold">Made with ❤️ for the Path of Exile 2 Community</span>
            </div>
            <p className="text-caption">
              Powered by Next.js • Deployed on Vercel • Built with TypeScript
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}