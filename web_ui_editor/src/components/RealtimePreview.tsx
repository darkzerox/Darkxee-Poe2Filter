'use client'

import { useState, useEffect } from 'react'
import { Eye, Volume2, Image, Zap, RefreshCw } from 'lucide-react'
import { FilterRule } from '@/lib/FilterParser'

interface RealtimePreviewProps {
  rules: FilterRule[]
  selectedRule: FilterRule | null
}

interface PreviewItem {
  id: string
  name: string
  type: string
  rarity: string
  level: number
  category: string
}

export default function RealtimePreview({ rules, selectedRule }: RealtimePreviewProps) {
  const [previewItems, setPreviewItems] = useState<PreviewItem[]>([])
  const [isPlaying, setIsPlaying] = useState(false)
  const [selectedItem, setSelectedItem] = useState<PreviewItem | null>(null)

  // Sample items for preview
  const sampleItems: PreviewItem[] = [
    { id: '1', name: 'Mirror of Kalandra', type: 'Currency', rarity: 'Unique', level: 1, category: 'Currency' },
    { id: '2', name: 'Divine Orb', type: 'Currency', rarity: 'Currency', level: 1, category: 'Currency' },
    { id: '3', name: 'Exalted Orb', type: 'Currency', rarity: 'Currency', level: 1, category: 'Currency' },
    { id: '4', name: 'Chaos Orb', type: 'Currency', rarity: 'Currency', level: 1, category: 'Currency' },
    { id: '5', name: 'Ancient Sword', type: 'Weapon', rarity: 'Rare', level: 85, category: 'Equipment' },
    { id: '6', name: 'Diamond Ring', type: 'Ring', rarity: 'Rare', level: 78, category: 'Equipment' },
    { id: '7', name: 'Ruby Jewel', type: 'Jewel', rarity: 'Magic', level: 1, category: 'Jewel' },
    { id: '8', name: 'Tabula Rasa', type: 'Body Armour', rarity: 'Unique', level: 1, category: 'Equipment' },
    { id: '9', name: 'Scroll of Wisdom', type: 'Currency', rarity: 'Currency', level: 1, category: 'Currency' },
    { id: '10', name: 'Portal Scroll', type: 'Currency', rarity: 'Currency', level: 1, category: 'Currency' }
  ]

  // Find matching rules for an item
  const findMatchingRules = (item: PreviewItem): FilterRule[] => {
    return rules.filter(rule => {
      if (!rule.enabled) return false

      return rule.conditions.every(condition => {
        switch (condition.type) {
          case 'Class':
            return item.type === condition.value
          case 'BaseType':
            return item.name === condition.value
          case 'Rarity':
            return item.rarity === condition.value
          case 'ItemLevel':
            if (condition.operator === '>=') {
              return item.level >= (condition.value as number)
            }
            return item.level === condition.value
          default:
            return true
        }
      })
    })
  }

  // Get the highest priority rule for an item
  const getItemRule = (item: PreviewItem): FilterRule | null => {
    const matchingRules = findMatchingRules(item)
    if (matchingRules.length === 0) return null

    return matchingRules.sort((a, b) => a.priority - b.priority)[0]
  }

  // Get item style from rule
  const getItemStyle = (item: PreviewItem) => {
    const rule = getItemRule(item)
    if (!rule) return {}

    const style: any = {}
    
    // Text Color
    const textColorAction = rule.actions.find(action => action.type === 'SetTextColor')
    if (textColorAction && textColorAction.values.length >= 3) {
      const [r, g, b] = textColorAction.values as number[]
      style.color = `rgb(${r}, ${g}, ${b})`
    }

    // Border Color
    const borderColorAction = rule.actions.find(action => action.type === 'SetBorderColor')
    if (borderColorAction && borderColorAction.values.length >= 3) {
      const [r, g, b] = borderColorAction.values as number[]
      style.borderColor = `rgb(${r}, ${g}, ${b})`
    }

    // Background Color
    const backgroundColorAction = rule.actions.find(action => action.type === 'SetBackgroundColor')
    if (backgroundColorAction && backgroundColorAction.values.length >= 3) {
      const [r, g, b] = backgroundColorAction.values as number[]
      style.backgroundColor = `rgb(${r}, ${g}, ${b})`
    }

    // Font Size
    const fontSizeAction = rule.actions.find(action => action.type === 'SetFontSize')
    if (fontSizeAction && fontSizeAction.values.length >= 1) {
      style.fontSize = `${fontSizeAction.values[0]}px`
    }

    return style
  }

  // Play sound for item
  const playItemSound = (item: PreviewItem) => {
    const rule = getItemRule(item)
    if (!rule) return

    const soundAction = rule.actions.find(action => action.type === 'CustomAlertSound')
    if (soundAction && soundAction.values.length >= 2) {
      const soundFile = soundAction.values[0] as string
      const volume = (soundAction.values[1] as number) / 100
      
      // Create audio element and play
      const audio = new Audio(`/sounds/${soundFile}`)
      audio.volume = volume
      audio.play().catch(() => {
        console.log('Sound file not found:', soundFile)
      })
    }
  }

  // Generate preview items
  const generatePreview = () => {
    setPreviewItems(sampleItems)
  }

  // Auto-refresh preview
  useEffect(() => {
    generatePreview()
    const interval = setInterval(generatePreview, 2000)
    return () => clearInterval(interval)
  }, [rules])

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="card-glass p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Eye className="w-6 h-6 text-blue-400 mr-3" />
            <div>
              <h2 className="text-heading text-white">Realtime Preview</h2>
              <p className="text-caption">See how your filter rules affect items</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={generatePreview}
              className="btn-secondary"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </button>
            
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className={`btn-outline ${isPlaying ? 'bg-green-500/20 text-green-400' : ''}`}
            >
              <Volume2 className="w-4 h-4 mr-2" />
              {isPlaying ? 'Stop' : 'Play'} Sounds
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gradient">{previewItems.length}</div>
            <div className="text-sm text-gray-400">Total Items</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gradient">
              {previewItems.filter(item => getItemRule(item)).length}
            </div>
            <div className="text-sm text-gray-400">Filtered</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gradient">
              {previewItems.filter(item => getItemRule(item)?.actions.find(a => a.type === 'CustomAlertSound')).length}
            </div>
            <div className="text-sm text-gray-400">With Sound</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gradient">
              {previewItems.filter(item => getItemRule(item)?.actions.find(a => a.type === 'MinimapIcon')).length}
            </div>
            <div className="text-sm text-gray-400">With Icons</div>
          </div>
        </div>
      </div>

      {/* Preview Items */}
      <div className="flex-1 overflow-y-auto space-y-3">
        {previewItems.map(item => {
          const rule = getItemRule(item)
          const style = getItemStyle(item)
          const hasSound = rule?.actions.find(a => a.type === 'CustomAlertSound')
          const hasIcon = rule?.actions.find(a => a.type === 'MinimapIcon')
          
          return (
            <div
              key={item.id}
              className={`card-modern p-4 cursor-pointer transition-all duration-200 hover-lift ${
                selectedItem?.id === item.id ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700/50'
              }`}
              onClick={() => {
                setSelectedItem(item)
                if (isPlaying) playItemSound(item)
              }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {/* Item Icon */}
                  <div className="flex items-center space-x-2">
                    {hasIcon && (
                      <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center text-xs font-bold">
                        ⭐
                      </div>
                    )}
                    {hasSound && (
                      <Volume2 className="w-4 h-4 text-green-400" />
                    )}
                  </div>

                  {/* Item Info */}
                  <div>
                    <div 
                      className="font-semibold"
                      style={style}
                    >
                      {item.name}
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-400">
                      <span className="px-2 py-1 bg-gray-700 rounded text-xs">
                        {item.type}
                      </span>
                      <span className="px-2 py-1 bg-gray-700 rounded text-xs">
                        {item.rarity}
                      </span>
                      <span>Level {item.level}</span>
                    </div>
                  </div>
                </div>

                {/* Rule Info */}
                <div className="text-right">
                  {rule ? (
                    <div className="text-sm">
                      <div className="text-green-400 font-semibold">{rule.name}</div>
                      <div className="text-gray-400">Priority: {rule.priority}</div>
                    </div>
                  ) : (
                    <div className="text-sm text-gray-500">No matching rule</div>
                  )}
                </div>
              </div>

              {/* Item Preview */}
              <div className="mt-3 pt-3 border-t border-gray-700/50">
                <div 
                  className="p-3 rounded-lg border-2"
                  style={style}
                >
                  <div className="font-bold">{item.name}</div>
                  <div className="text-sm opacity-80">{item.type}</div>
                  <div className="text-xs opacity-60">Item Level: {item.level}</div>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Selected Item Details */}
      {selectedItem && (
        <div className="card-glass p-4 mt-6">
          <h4 className="font-semibold text-white mb-3">Selected Item Details</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h5 className="text-sm font-medium text-gray-300 mb-2">Item Properties</h5>
              <div className="space-y-1 text-sm text-gray-400">
                <div>Name: {selectedItem.name}</div>
                <div>Type: {selectedItem.type}</div>
                <div>Rarity: {selectedItem.rarity}</div>
                <div>Level: {selectedItem.level}</div>
                <div>Category: {selectedItem.category}</div>
              </div>
            </div>
            
            <div>
              <h5 className="text-sm font-medium text-gray-300 mb-2">Matching Rules</h5>
              <div className="space-y-1 text-sm">
                {findMatchingRules(selectedItem).map(rule => (
                  <div key={rule.id} className="text-gray-400">
                    {rule.name} (Priority: {rule.priority})
                  </div>
                ))}
                {findMatchingRules(selectedItem).length === 0 && (
                  <div className="text-gray-500">No matching rules</div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}