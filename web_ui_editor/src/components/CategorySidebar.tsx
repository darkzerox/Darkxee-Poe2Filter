'use client'

import { 
  Coins, Shield, Gem, Map, Star, Plus, Copy, Trash2, 
  Zap, Crown, Scroll, Wrench, Key, Heart, Droplets, 
  Sparkles, Diamond, Circle, Square, Triangle, Cross
} from 'lucide-react'

interface CategorySidebarProps {
  categories: any
  setCategories: (categories: any) => void
  onAddRule: () => void
  onDuplicateRule: () => void
  onDeleteRule: () => void
  rules: any[]
  selectedRule: any
}

export default function CategorySidebar({ 
  categories, 
  setCategories, 
  onAddRule, 
  onDuplicateRule, 
  onDeleteRule,
  rules,
  selectedRule
}: CategorySidebarProps) {
  // All categories with icons
  const allCategories = [
    { key: 'currency', name: 'Currency', icon: Coins, color: 'text-yellow-400' },
    { key: 'mirror_tier', name: 'Mirror Tier', icon: Crown, color: 'text-purple-400' },
    { key: 'gacha', name: 'Gacha', icon: Sparkles, color: 'text-pink-400' },
    { key: 'crafting', name: 'Crafting', icon: Wrench, color: 'text-blue-400' },
    { key: 'gold', name: 'Gold', icon: Coins, color: 'text-yellow-300' },
    { key: 'uncut_gems', name: 'Uncut Gems', icon: Gem, color: 'text-cyan-400' },
    { key: 'scroll_of_wisdom', name: 'Scroll of Wisdom', icon: Scroll, color: 'text-gray-400' },
    { key: 'salvage', name: 'Salvage', icon: Trash2, color: 'text-red-400' },
    { key: 'amulets', name: 'Amulets', icon: Heart, color: 'text-pink-400' },
    { key: 'belts', name: 'Belts', color: 'text-green-400' },
    { key: 'jewel', name: 'Jewel', icon: Gem, color: 'text-purple-400' },
    { key: 'ring', name: 'Ring', icon: Circle, color: 'text-orange-400' },
    { key: 'key', name: 'Key', icon: Key, color: 'text-yellow-400' },
    { key: 'relics', name: 'Relics', icon: Star, color: 'text-indigo-400' },
    { key: 'rune', name: 'Rune', icon: Zap, color: 'text-blue-400' },
    { key: 'talisman', name: 'Talisman', icon: Diamond, color: 'text-purple-400' },
    { key: 'soul_core', name: 'Soul Core', icon: Heart, color: 'text-red-400' },
    { key: 'waystones', name: 'Waystones', icon: Map, color: 'text-teal-400' },
    { key: 'flasks', name: 'Flasks', icon: Droplets, color: 'text-green-400' },
    { key: 'charms', name: 'Charms', icon: Star, color: 'text-yellow-400' },
    { key: 'rarity_unique', name: 'Rarity Unique', icon: Crown, color: 'text-orange-400' },
    { key: 'rarity_rare', name: 'Rarity Rare', icon: Square, color: 'text-yellow-400' },
    { key: 'rarity_magic', name: 'Rarity Magic', icon: Triangle, color: 'text-blue-400' },
    { key: 'equipment', name: 'Equipment', icon: Shield, color: 'text-gray-400' },
    { key: 'general', name: 'General', icon: Circle, color: 'text-gray-300' }
  ]

  const handleCategoryClick = (categoryKey: string) => {
    const updatedCategories = { ...categories }
    Object.keys(updatedCategories).forEach(key => {
      updatedCategories[key].active = key === categoryKey
    })
    setCategories(updatedCategories)
  }

  // Count rules per category
  const getRuleCount = (categoryName: string) => {
    return rules.filter(rule => rule.category === categoryName).length
  }

  const getActiveRuleCount = (categoryName: string) => {
    return rules.filter(rule => rule.category === categoryName && rule.enabled).length
  }

  return (
    <div className="w-64 bg-gray-800/50 backdrop-blur-sm border-r border-gray-700/50 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-700/50">
        <h3 className="text-lg font-semibold text-white mb-2">Categories</h3>
        <p className="text-sm text-gray-400">Filter by category</p>
      </div>

      {/* Categories */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-1">
          {allCategories.map((category) => {
            const IconComponent = category.icon || Circle
            const ruleCount = getRuleCount(category.name)
            const activeCount = getActiveRuleCount(category.name)
            
            return (
              <button
                key={category.key}
                onClick={() => handleCategoryClick(category.key)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover-lift ${
                  categories[category.key]?.active
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                <div className="flex items-center">
                  <IconComponent className={`w-4 h-4 mr-3 ${category.color}`} />
                  <span>{category.name}</span>
                </div>
                <div className="flex items-center space-x-2">
                  {activeCount > 0 && (
                    <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                      {activeCount}
                    </span>
                  )}
                  <span className="text-xs text-gray-500">
                    {ruleCount}
                  </span>
                </div>
              </button>
            )
          })}
        </div>
      </div>

      {/* Tools */}
      <div className="p-4 border-t border-gray-700/50">
        <h3 className="text-sm font-medium text-gray-400 mb-3">Tools</h3>
        <div className="space-y-2">
          <button
            onClick={onAddRule}
            className="w-full flex items-center px-3 py-2 bg-green-600/20 text-green-400 rounded-lg text-sm font-medium hover:bg-green-600/30 transition-colors border border-green-500/30"
          >
            <Plus className="w-4 h-4 mr-3" />
            Add Rule
          </button>
          <button
            onClick={onDuplicateRule}
            disabled={!selectedRule}
            className="w-full flex items-center px-3 py-2 bg-blue-600/20 text-blue-400 rounded-lg text-sm font-medium hover:bg-blue-600/30 transition-colors border border-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Copy className="w-4 h-4 mr-3" />
            Duplicate
          </button>
          <button
            onClick={onDeleteRule}
            disabled={!selectedRule}
            className="w-full flex items-center px-3 py-2 bg-red-600/20 text-red-400 rounded-lg text-sm font-medium hover:bg-red-600/30 transition-colors border border-red-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Trash2 className="w-4 h-4 mr-3" />
            Delete
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="p-4 border-t border-gray-700/50">
        <h3 className="text-sm font-medium text-gray-400 mb-3">Statistics</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between text-gray-300">
            <span>Total Rules:</span>
            <span className="text-white font-medium">{rules.length}</span>
          </div>
          <div className="flex justify-between text-gray-300">
            <span>Active Rules:</span>
            <span className="text-green-400 font-medium">{rules.filter(r => r.enabled).length}</span>
          </div>
          <div className="flex justify-between text-gray-300">
            <span>Categories:</span>
            <span className="text-blue-400 font-medium">{allCategories.length}</span>
          </div>
          <div className="flex justify-between text-gray-300">
            <span>Selected:</span>
            <span className="text-purple-400 font-medium">{selectedRule ? '1' : '0'}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
