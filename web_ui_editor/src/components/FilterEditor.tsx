'use client'

import { useState, useEffect } from 'react'
import { Filter, Play, Edit, Trash2, Copy, Plus, Eye, EyeOff } from 'lucide-react'
import { FilterRule, FilterCondition, FilterAction } from '@/lib/FilterParser'

interface FilterEditorProps {
  rules: FilterRule[]
  selectedRule: FilterRule | null
  onSelectRule: (rule: FilterRule) => void
  onUpdateRules: (rules: FilterRule[]) => void
  selectedCategory?: string
}

export default function FilterEditor({ rules, selectedRule, onSelectRule, onUpdateRules, selectedCategory: propSelectedCategory }: FilterEditorProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [showDisabled, setShowDisabled] = useState(true)

  // Categories based on config.json
  const predefinedCategories = [
    'All',
    'Currency',
    'Mirror Tier',
    'Gacha',
    'Crafting',
    'Gold',
    'Uncut Gems',
    'Scroll of Wisdom',
    'Salvage',
    'Amulets',
    'Belts',
    'Jewel',
    'Ring',
    'Key',
    'Relics',
    'Rune',
    'Talisman',
    'Soul Core',
    'Waystones',
    'Flasks',
    'Charms',
    'Rarity Unique',
    'Rarity Rare',
    'Rarity Magic',
    'Equipment',
    'General'
  ]
  
  const categories = [...predefinedCategories, ...Array.from(new Set(rules.map(rule => rule.category).filter(cat => !predefinedCategories.includes(cat))))]
  
  // Use prop category if provided, otherwise use local state
  const currentCategory = propSelectedCategory || selectedCategory

  const filteredRules = rules.filter(rule => {
    const matchesSearch = rule.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         rule.category.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = currentCategory === 'All' || rule.category === currentCategory
    const matchesVisibility = showDisabled || rule.enabled
    
    return matchesSearch && matchesCategory && matchesVisibility
  })

  const handleToggleRule = (ruleId: string) => {
    const updatedRules = rules.map(rule => 
      rule.id === ruleId ? { ...rule, enabled: !rule.enabled } : rule
    )
    onUpdateRules(updatedRules)
  }

  const handleDeleteRule = (ruleId: string) => {
    if (confirm('Are you sure you want to delete this rule?')) {
      const updatedRules = rules.filter(rule => rule.id !== ruleId)
      onUpdateRules(updatedRules)
    }
  }

  const handleDuplicateRule = (rule: FilterRule) => {
    const duplicatedRule = {
      ...rule,
      id: `rule_${Date.now()}`,
      name: `${rule.name} (Copy)`,
      priority: rules.length + 1
    }
    onUpdateRules([...rules, duplicatedRule])
  }

  const handleAddRule = () => {
    const newRule: FilterRule = {
      id: `rule_${Date.now()}`,
      name: 'New Rule',
      enabled: true,
      conditions: [],
      actions: [{ type: 'Show', values: [] }],
      category: selectedCategory === 'All' ? 'General' : selectedCategory,
      priority: rules.length + 1
    }
    onUpdateRules([...rules, newRule])
    onSelectRule(newRule)
  }

  const getRuleIcon = (rule: FilterRule) => {
    const showAction = rule.actions.find(action => action.type === 'Show')
    return showAction ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />
  }

  const getRuleColor = (rule: FilterRule) => {
    const textColorAction = rule.actions.find(action => action.type === 'SetTextColor')
    if (textColorAction && textColorAction.values.length >= 3) {
      const [r, g, b] = textColorAction.values as number[]
      return `rgb(${r}, ${g}, ${b})`
    }
    return '#ffffff'
  }

  const getRuleSound = (rule: FilterRule) => {
    const soundAction = rule.actions.find(action => action.type === 'CustomAlertSound')
    if (soundAction && soundAction.values.length > 0) {
      return soundAction.values[0] as string
    }
    return null
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="card-glass p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-heading text-white">Filter Rules</h2>
          <button
            onClick={handleAddRule}
            className="group btn-primary hover-glow"
          >
            <Plus className="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
            Add Rule
          </button>
        </div>

        {/* Search and Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Search Rules
            </label>
            <input
              type="text"
              placeholder="Search by name or category..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-modern focus-modern"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Category
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input-modern focus-modern"
            >
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <label className="flex items-center space-x-2 text-sm text-gray-300">
              <input
                type="checkbox"
                checked={showDisabled}
                onChange={(e) => setShowDisabled(e.target.checked)}
                className="rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-blue-500"
              />
              <span>Show disabled rules</span>
            </label>
          </div>
        </div>
      </div>

      {/* Rules List */}
      <div className="flex-1 overflow-y-auto space-y-3">
        {filteredRules.length === 0 ? (
          <div className="card-glass p-8 text-center">
            <Filter className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">No Rules Found</h3>
            <p className="text-gray-400 mb-4">
              {searchTerm || selectedCategory !== 'All' 
                ? 'Try adjusting your search or filter criteria'
                : 'Create your first filter rule to get started'
              }
            </p>
            {!searchTerm && selectedCategory === 'All' && (
              <button
                onClick={handleAddRule}
                className="btn-primary"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add First Rule
              </button>
            )}
          </div>
        ) : (
          filteredRules.map(rule => (
            <div
              key={rule.id}
              className={`card-modern p-4 cursor-pointer transition-all duration-200 hover-lift ${
                selectedRule?.id === rule.id 
                  ? 'border-blue-500 bg-blue-500/10' 
                  : 'border-gray-700/50'
              } ${!rule.enabled ? 'opacity-60' : ''}`}
              onClick={() => onSelectRule(rule)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    {getRuleIcon(rule)}
                    <span 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: getRuleColor(rule) }}
                    />
                    {getRuleSound(rule) && (
                      <span className="text-xs text-gray-400">🔊</span>
                    )}
                  </div>
                  
                  <div>
                    <h3 className="font-semibold text-white">{rule.name}</h3>
                    <div className="flex items-center space-x-2 text-sm text-gray-400">
                      <span className="px-2 py-1 bg-gray-700 rounded text-xs">
                        {rule.category}
                      </span>
                      <span>Priority: {rule.priority}</span>
                      <span>•</span>
                      <span>{rule.conditions.length} conditions</span>
                      <span>•</span>
                      <span>{rule.actions.length} actions</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleToggleRule(rule.id)
                    }}
                    className={`p-2 rounded-lg transition-colors ${
                      rule.enabled 
                        ? 'text-green-400 hover:bg-green-500/20' 
                        : 'text-gray-400 hover:bg-gray-600'
                    }`}
                    title={rule.enabled ? 'Disable rule' : 'Enable rule'}
                  >
                    {rule.enabled ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDuplicateRule(rule)
                    }}
                    className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                    title="Duplicate rule"
                  >
                    <Copy className="w-4 h-4" />
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDeleteRule(rule.id)
                    }}
                    className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                    title="Delete rule"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Rule Preview */}
              <div className="mt-3 pt-3 border-t border-gray-700/50">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">Conditions:</span>
                    <div className="mt-1 space-y-1">
                      {rule.conditions.slice(0, 3).map((condition, index) => (
                        <div key={index} className="text-gray-300">
                          {condition.type} {condition.operator || ''} {condition.value}
                        </div>
                      ))}
                      {rule.conditions.length > 3 && (
                        <div className="text-gray-500">
                          +{rule.conditions.length - 3} more...
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-gray-400">Actions:</span>
                    <div className="mt-1 space-y-1">
                      {rule.actions.slice(0, 3).map((action, index) => (
                        <div key={index} className="text-gray-300">
                          {action.type} {action.values.join(' ')}
                        </div>
                      ))}
                      {rule.actions.length > 3 && (
                        <div className="text-gray-500">
                          +{rule.actions.length - 3} more...
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div className="card-glass p-4 mt-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-gradient">{rules.length}</div>
            <div className="text-sm text-gray-400">Total Rules</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gradient">{rules.filter(r => r.enabled).length}</div>
            <div className="text-sm text-gray-400">Enabled</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gradient">{categories.length - 1}</div>
            <div className="text-sm text-gray-400">Categories</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gradient">{filteredRules.length}</div>
            <div className="text-sm text-gray-400">Filtered</div>
          </div>
        </div>
      </div>
    </div>
  )
}