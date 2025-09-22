'use client'

import { useState, useEffect } from 'react'
import { Upload, Download, Save, Play, Settings, Filter, Eye, Trash2, Copy, Plus } from 'lucide-react'
import FilterEditor from '@/components/FilterEditor'
import RealtimePreview from '@/components/RealtimePreview'
import PropertiesPanel from '@/components/PropertiesPanel'
import CategorySidebar from '@/components/CategorySidebar'
import { ImportExportManager } from '@/lib/ImportExportManager'
import { FilterParser } from '@/lib/FilterParser'

export default function EditorPage() {
  const [activeTab, setActiveTab] = useState<'rules' | 'preview' | 'settings'>('rules')
  const [selectedRule, setSelectedRule] = useState<any>(null)
  const [currentFilter, setCurrentFilter] = useState<any>(null)
  const [rules, setRules] = useState<any[]>([])
  const [categories, setCategories] = useState({
    currency: { name: 'Currency', icon: 'Coins', active: true },
    equipment: { name: 'Equipment', icon: 'Shield', active: false },
    jewels: { name: 'Jewels', icon: 'Gem', active: false },
    maps: { name: 'Maps', icon: 'Map', active: false },
    special: { name: 'Special Items', icon: 'Star', active: false }
  })
  
  const [selectedCategory, setSelectedCategory] = useState('Currency')

  const [filterParser] = useState(() => new FilterParser())

  useEffect(() => {
    loadDefaultFilter()
  }, [])

  const loadDefaultFilter = async () => {
    try {
      const sampleFilter = await ImportExportManager.loadSampleFilter()
      setRules(sampleFilter.rules)
      setCurrentFilter(sampleFilter)
      setCategories({
        currency: { name: 'Currency', icon: 'Coins', active: true },
        equipment: { name: 'Equipment', icon: 'Shield', active: false },
        jewels: { name: 'Jewels', icon: 'Gem', active: false },
        maps: { name: 'Maps', icon: 'Map', active: false },
        special: { name: 'Special Items', icon: 'Star', active: false }
      })
    } catch (error) {
      console.error('Failed to load sample filter:', error)
      const defaultRules = generateDefaultRules()
      setRules(defaultRules)
      setCurrentFilter({
        name: 'DZX Filter',
        version: '1.0.0',
        description: 'Path of Exile 2 Filter',
        rules: defaultRules,
        categories: ['Currency', 'Equipment', 'General']
      })
    }
  }

  const generateDefaultRules = () => {
    return [
      {
        id: 'rule_001',
        show_hide: 'Show',
        conditions: [
          { type: 'Class', operator: '==', values: ['Currency'] }
        ],
        actions: [
          { type: 'SetTextColor', values: [255, 255, 255] },
          { type: 'SetFontSize', values: [32] },
          { type: 'CustomAlertSound', values: ['currency.mp3', 100] }
        ],
        comment: 'Default currency rule',
        enabled: true
      },
      {
        id: 'rule_002',
        show_hide: 'Show',
        conditions: [
          { type: 'Class', operator: '==', values: ['Currency'] },
          { type: 'BaseType', operator: '==', values: ['Mirror', 'Divine'] }
        ],
        actions: [
          { type: 'SetTextColor', values: [232, 231, 171] },
          { type: 'SetBorderColor', values: [232, 37, 97] },
          { type: 'SetBackgroundColor', values: [232, 37, 97] },
          { type: 'SetFontSize', values: [45] },
          { type: 'PlayEffect', values: ['Red'] },
          { type: 'MinimapIcon', values: [0, 'Red', 'Star'] },
          { type: 'CustomAlertSound', values: ['mirror.mp3', 100] }
        ],
        comment: 'High value currency',
        enabled: true
      }
    ]
  }

  const handleImport = async () => {
    try {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.filter,.json,.yaml'
      input.onchange = async (e: any) => {
        const file = e.target.files[0]
        if (file) {
          try {
            const result = await ImportExportManager.importFile(file)
            setCurrentFilter(result)
            setRules(result.rules || [])
            alert('Filter imported successfully!')
          } catch (error) {
            console.error('Import error:', error)
            alert(`Import failed: ${error}`)
          }
        }
      }
      input.click()
    } catch (error) {
      alert('Error importing filter: ' + (error as Error).message)
    }
  }

  const handleExport = async () => {
    try {
      ImportExportManager.exportFile(currentFilter, 'filter')
      alert('Filter exported successfully!')
    } catch (error) {
      alert('Error exporting filter: ' + (error as Error).message)
    }
  }

  const handleSave = () => {
    const filterData = {
      ...currentFilter,
      rules: rules,
      savedAt: new Date().toISOString()
    }
    localStorage.setItem('dzx_filter_editor', JSON.stringify(filterData))
    alert('Filter saved successfully!')
  }

  const handleAddRule = () => {
    const newRule = {
      id: 'rule_' + Date.now(),
      show_hide: 'Show',
      conditions: [
        { type: 'Class', operator: '==', values: ['Currency'] }
      ],
      actions: [
        { type: 'SetTextColor', values: [255, 255, 255] },
        { type: 'SetFontSize', values: [32] }
      ],
      comment: 'New Rule',
      enabled: true
    }
    setRules([...rules, newRule])
    setSelectedRule(newRule)
  }

  const handleDeleteRule = () => {
    if (selectedRule && confirm('Are you sure you want to delete this rule?')) {
      setRules(rules.filter(rule => rule.id !== selectedRule.id))
      setSelectedRule(null)
    }
  }

  const handleDuplicateRule = () => {
    if (selectedRule) {
      const duplicatedRule = {
        ...selectedRule,
        id: 'rule_' + Date.now(),
        comment: selectedRule.comment + ' (Copy)'
      }
      setRules([...rules, duplicatedRule])
      setSelectedRule(duplicatedRule)
    }
  }

  const handleCategoryChange = (categoryKey: string) => {
    const updatedCategories = { ...categories }
    Object.keys(updatedCategories).forEach(key => {
      updatedCategories[key].active = key === categoryKey
    })
    setCategories(updatedCategories)
    
    // Map category key to category name
    const categoryNameMap: { [key: string]: string } = {
      'currency': 'Currency',
      'mirror_tier': 'Mirror Tier',
      'gacha': 'Gacha',
      'crafting': 'Crafting',
      'gold': 'Gold',
      'uncut_gems': 'Uncut Gems',
      'scroll_of_wisdom': 'Scroll of Wisdom',
      'salvage': 'Salvage',
      'amulets': 'Amulets',
      'belts': 'Belts',
      'jewel': 'Jewel',
      'ring': 'Ring',
      'key': 'Key',
      'relics': 'Relics',
      'rune': 'Rune',
      'talisman': 'Talisman',
      'soul_core': 'Soul Core',
      'waystones': 'Waystones',
      'flasks': 'Flasks',
      'charms': 'Charms',
      'rarity_unique': 'Rarity Unique',
      'rarity_rare': 'Rarity Rare',
      'rarity_magic': 'Rarity Magic',
      'equipment': 'Equipment',
      'general': 'General'
    }
    
    setSelectedCategory(categoryNameMap[categoryKey] || 'All')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Header */}
      <header className="relative glass-dark border-b border-white/10">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 gradient-primary rounded-2xl flex items-center justify-center shadow-glow">
                  <Filter className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">DZX Filter Editor</h1>
                <p className="text-sm text-gray-400">Path of Exile 2</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleImport}
                className="group btn-primary hover-glow"
              >
                <Upload className="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
                Import
              </button>
              <button
                onClick={handleExport}
                className="group btn-secondary hover-glow"
              >
                <Download className="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
                Export
              </button>
              <button
                onClick={handleSave}
                className="group btn-ghost hover-glow"
              >
                <Save className="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
                Save
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-80px)]">
        {/* Sidebar */}
        <CategorySidebar 
          categories={categories}
          setCategories={handleCategoryChange}
          onAddRule={handleAddRule}
          onDuplicateRule={handleDuplicateRule}
          onDeleteRule={handleDeleteRule}
          rules={rules}
          selectedRule={selectedRule}
        />

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Tabs */}
          <div className="glass-dark border-b border-white/10">
            <div className="flex">
              <button
                onClick={() => setActiveTab('rules')}
                className={`tab-modern ${activeTab === 'rules' ? 'active' : ''}`}
              >
                <Filter className="w-4 h-4 mr-2" />
                Rules
              </button>
              <button
                onClick={() => setActiveTab('preview')}
                className={`tab-modern ${activeTab === 'preview' ? 'active' : ''}`}
              >
                <Eye className="w-4 h-4 mr-2" />
                Preview
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`tab-modern ${activeTab === 'settings' ? 'active' : ''}`}
              >
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="flex-1 flex">
            <div className="flex-1 p-6">
              {activeTab === 'rules' && (
                <FilterEditor
                  rules={rules}
                  selectedRule={selectedRule}
                  onSelectRule={setSelectedRule}
                  onUpdateRules={setRules}
                  selectedCategory={selectedCategory}
                />
              )}
              {activeTab === 'preview' && (
                <RealtimePreview
                  rules={rules}
                  currentFilter={currentFilter}
                />
              )}
              {activeTab === 'settings' && (
                <div className="space-y-6">
                  <div className="card-glass p-6">
                    <h3 className="text-heading text-white mb-4">General Settings</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Filter Name
                        </label>
                        <input
                          type="text"
                          value={currentFilter?.name || ''}
                          onChange={(e) => setCurrentFilter({...currentFilter, name: e.target.value})}
                          className="input-modern focus-modern"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Platform
                        </label>
                        <select
                          value={currentFilter?.platform || 'pc'}
                          onChange={(e) => setCurrentFilter({...currentFilter, platform: e.target.value})}
                          className="input-modern focus-modern"
                        >
                          <option value="pc">PC</option>
                          <option value="ps5">PS5</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Properties Panel */}
            {selectedRule && (
              <PropertiesPanel
                rule={selectedRule}
                onUpdateRule={(updatedRule) => {
                  setRules(rules.map(rule => 
                    rule.id === updatedRule.id ? updatedRule : rule
                  ))
                  setSelectedRule(updatedRule)
                }}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
