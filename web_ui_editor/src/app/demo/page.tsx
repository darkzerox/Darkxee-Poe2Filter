'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, Play, Upload, Download, Filter, Settings, Eye } from 'lucide-react'

export default function DemoPage() {
  const [activeDemo, setActiveDemo] = useState<'import' | 'edit' | 'preview' | 'export'>('import')

  const demoSections = [
    {
      id: 'import',
      title: 'Import Filter',
      icon: Upload,
      description: 'Import existing .filter files from Path of Exile 2',
      content: (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Supported Formats</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-700 rounded p-4 text-center">
                <div className="text-2xl mb-2">📄</div>
                <div className="text-white font-medium">.filter</div>
                <div className="text-gray-400 text-sm">Native POE2 format</div>
              </div>
              <div className="bg-gray-700 rounded p-4 text-center">
                <div className="text-2xl mb-2">📋</div>
                <div className="text-white font-medium">.json</div>
                <div className="text-gray-400 text-sm">Structured data</div>
              </div>
              <div className="bg-gray-700 rounded p-4 text-center">
                <div className="text-2xl mb-2">📝</div>
                <div className="text-white font-medium">.yaml</div>
                <div className="text-gray-400 text-sm">Human readable</div>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">How to Import</h3>
            <ol className="space-y-3 text-gray-300">
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">1</span>
                Click the "Import" button in the editor
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">2</span>
                Select your .filter file from your computer
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">3</span>
                The filter will be parsed and loaded into the editor
              </li>
            </ol>
          </div>
        </div>
      )
    },
    {
      id: 'edit',
      title: 'Edit Rules',
      icon: Settings,
      description: 'Modify colors, sounds, and visual effects',
      content: (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Visual Editing</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-md font-medium text-blue-400 mb-3">Colors</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-red-500 rounded border border-gray-600"></div>
                    <span className="text-gray-300">Text Color</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-yellow-500 rounded border border-gray-600"></div>
                    <span className="text-gray-300">Border Color</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 rounded border border-gray-600"></div>
                    <span className="text-gray-300">Background Color</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="text-md font-medium text-purple-400 mb-3">Effects</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gray-600 rounded flex items-center justify-center">
                      <span className="text-white text-sm">A</span>
                    </div>
                    <span className="text-gray-300">Font Size</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gray-600 rounded flex items-center justify-center">
                      <span className="text-red-400">★</span>
                    </div>
                    <span className="text-gray-300">Minimap Icon</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gray-600 rounded flex items-center justify-center">
                      <span className="text-blue-400">🔊</span>
                    </div>
                    <span className="text-gray-300">Alert Sound</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Rule Management</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between bg-gray-700 rounded p-3">
                <span className="text-white">Add New Rule</span>
                <span className="text-green-400 text-sm">✓ Available</span>
              </div>
              <div className="flex items-center justify-between bg-gray-700 rounded p-3">
                <span className="text-white">Duplicate Rule</span>
                <span className="text-green-400 text-sm">✓ Available</span>
              </div>
              <div className="flex items-center justify-between bg-gray-700 rounded p-3">
                <span className="text-white">Delete Rule</span>
                <span className="text-green-400 text-sm">✓ Available</span>
              </div>
              <div className="flex items-center justify-between bg-gray-700 rounded p-3">
                <span className="text-white">Enable/Disable Rule</span>
                <span className="text-green-400 text-sm">✓ Available</span>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'preview',
      title: 'Realtime Preview',
      icon: Eye,
      description: 'See changes instantly with live preview',
      content: (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Preview Features</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-md font-medium text-green-400 mb-3">Visual Preview</h4>
                <div className="space-y-2">
                  <div className="bg-gray-700 rounded p-3 flex items-center justify-between">
                    <span className="text-white">Chaos Orb</span>
                    <div className="w-4 h-4 bg-red-500 rounded"></div>
                  </div>
                  <div className="bg-gray-700 rounded p-3 flex items-center justify-between">
                    <span className="text-white">Divine Orb</span>
                    <div className="w-4 h-4 bg-yellow-500 rounded"></div>
                  </div>
                  <div className="bg-gray-700 rounded p-3 flex items-center justify-between">
                    <span className="text-white">Mirror of Kalandra</span>
                    <div className="w-4 h-4 bg-purple-500 rounded"></div>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="text-md font-medium text-blue-400 mb-3">Sound Testing</h4>
                <div className="space-y-2">
                  <button className="w-full bg-gray-700 rounded p-3 text-left hover:bg-gray-600 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-white">Test Currency Sound</span>
                      <span className="text-gray-400">🔊</span>
                    </div>
                  </button>
                  <button className="w-full bg-gray-700 rounded p-3 text-left hover:bg-gray-600 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-white">Test Unique Sound</span>
                      <span className="text-gray-400">🔊</span>
                    </div>
                  </button>
                  <button className="w-full bg-gray-700 rounded p-3 text-left hover:bg-gray-600 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-white">Test All Sounds</span>
                      <span className="text-gray-400">▶️</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Statistics</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-white">8</div>
                <div className="text-sm text-gray-400">Total Items</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-400">6</div>
                <div className="text-sm text-gray-400">Visible</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-red-400">2</div>
                <div className="text-sm text-gray-400">Hidden</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-blue-400">12</div>
                <div className="text-sm text-gray-400">Active Rules</div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'export',
      title: 'Export Filter',
      icon: Download,
      description: 'Export your customized filter for use in-game',
      content: (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Export Options</h3>
            <div className="space-y-4">
              <div className="bg-gray-700 rounded p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-md font-medium text-white">Path of Exile 2 Format</h4>
                  <span className="text-green-400 text-sm">Recommended</span>
                </div>
                <p className="text-gray-400 text-sm mb-3">
                  Export as .filter file ready to use in Path of Exile 2
                </p>
                <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                  Download .filter
                </button>
              </div>
              <div className="bg-gray-700 rounded p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-md font-medium text-white">JSON Format</h4>
                  <span className="text-gray-400 text-sm">Backup</span>
                </div>
                <p className="text-gray-400 text-sm mb-3">
                  Export as JSON for backup or sharing with other tools
                </p>
                <button className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors">
                  Download .json
                </button>
              </div>
              <div className="bg-gray-700 rounded p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-md font-medium text-white">YAML Format</h4>
                  <span className="text-gray-400 text-sm">Human Readable</span>
                </div>
                <p className="text-gray-400 text-sm mb-3">
                  Export as YAML for easy reading and manual editing
                </p>
                <button className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors">
                  Download .yaml
                </button>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Installation Instructions</h3>
            <ol className="space-y-3 text-gray-300">
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">1</span>
                Download your customized .filter file
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">2</span>
                Copy the file to your Path of Exile 2 filter directory
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">3</span>
                Select the filter in-game from the filter menu
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">4</span>
                Enjoy your customized loot filtering experience!
              </li>
            </ol>
          </div>
        </div>
      )
    }
  ]

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link 
                href="/"
                className="flex items-center text-gray-400 hover:text-white transition-colors"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Link>
              <div className="w-px h-6 bg-gray-600"></div>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Filter className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">DZX Filter Editor Demo</h1>
                  <p className="text-sm text-gray-400">Interactive demonstration</p>
                </div>
              </div>
            </div>
            <Link 
              href="/editor"
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Play className="w-4 h-4 mr-2" />
              Try Editor
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Demo Navigation */}
        <div className="mb-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {demoSections.map((section) => {
              const IconComponent = section.icon
              return (
                <button
                  key={section.id}
                  onClick={() => setActiveDemo(section.id as any)}
                  className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                    activeDemo === section.id
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-gray-700 bg-gray-800 hover:border-gray-600'
                  }`}
                >
                  <div className="flex items-center space-x-3 mb-2">
                    <IconComponent className={`w-5 h-5 ${
                      activeDemo === section.id ? 'text-blue-400' : 'text-gray-400'
                    }`} />
                    <h3 className={`font-semibold ${
                      activeDemo === section.id ? 'text-blue-400' : 'text-white'
                    }`}>
                      {section.title}
                    </h3>
                  </div>
                  <p className="text-sm text-gray-400 text-left">
                    {section.description}
                  </p>
                </button>
              )
            })}
          </div>
        </div>

        {/* Demo Content */}
        <div className="bg-gray-800 rounded-lg border border-gray-700">
          <div className="p-6">
            {demoSections.find(section => section.id === activeDemo)?.content}
          </div>
        </div>

        {/* Call to Action */}
        <div className="mt-8 text-center">
          <div className="bg-gradient-to-r from-blue-500/20 to-purple-600/20 rounded-lg p-8 border border-blue-500/30">
            <h2 className="text-2xl font-bold text-white mb-4">
              Ready to create your own filter?
            </h2>
            <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
              Experience the full power of the DZX Filter Editor with real-time editing, 
              visual customization, and instant preview capabilities.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/editor"
                className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                <Filter className="w-5 h-5 mr-2" />
                Open Filter Editor
              </Link>
              <Link 
                href="/"
                className="inline-flex items-center px-8 py-4 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-600 transition-all duration-200 border border-gray-600"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
