'use client'

import { useState, useEffect } from 'react'
import { Palette, Volume2, Image, Settings, Save, RotateCcw } from 'lucide-react'
import { FilterRule, FilterAction, FilterCondition } from '@/lib/FilterParser'

interface PropertiesPanelProps {
  rule: FilterRule
  onUpdateRule: (rule: FilterRule) => void
}

export default function PropertiesPanel({ rule, onUpdateRule }: PropertiesPanelProps) {
  const [textColor, setTextColor] = useState('#ffffff')
  const [borderColor, setBorderColor] = useState('#000000')
  const [backgroundColor, setBackgroundColor] = useState('#000000')
  const [fontSize, setFontSize] = useState(32)
  const [soundFile, setSoundFile] = useState('')
  const [soundVolume, setSoundVolume] = useState(100)
  const [iconType, setIconType] = useState('Star')
  const [iconColor, setIconColor] = useState('Red')
  const [iconSize, setIconSize] = useState(0)

  // Helper functions
  const rgbToHex = (r: number, g: number, b: number): string => {
    return `#${[r, g, b].map(x => {
      const hex = x.toString(16)
      return hex.length === 1 ? '0' + hex : hex
    }).join('')}`
  }

  const hexToRgb = (hex: string): { r: number; g: number; b: number } => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : { r: 255, g: 255, b: 255 }
  }

  // Initialize state from rule
  useEffect(() => {
    if (rule && rule.actions) {
      // Text Color
      const textColorAction = rule.actions.find(action => action.type === 'SetTextColor')
      if (textColorAction && textColorAction.values.length >= 3) {
        const hex = rgbToHex(textColorAction.values[0] as number, textColorAction.values[1] as number, textColorAction.values[2] as number)
        setTextColor(hex)
      }

      // Border Color
      const borderColorAction = rule.actions.find(action => action.type === 'SetBorderColor')
      if (borderColorAction && borderColorAction.values.length >= 3) {
        const hex = rgbToHex(borderColorAction.values[0] as number, borderColorAction.values[1] as number, borderColorAction.values[2] as number)
        setBorderColor(hex)
      }

      // Background Color
      const backgroundColorAction = rule.actions.find(action => action.type === 'SetBackgroundColor')
      if (backgroundColorAction && backgroundColorAction.values.length >= 3) {
        const hex = rgbToHex(backgroundColorAction.values[0] as number, backgroundColorAction.values[1] as number, backgroundColorAction.values[2] as number)
        setBackgroundColor(hex)
      }

      // Font Size
      const fontSizeAction = rule.actions.find(action => action.type === 'SetFontSize')
      if (fontSizeAction && fontSizeAction.values.length >= 1) {
        setFontSize(fontSizeAction.values[0] as number)
      }

      // Sound
      const soundAction = rule.actions.find(action => action.type === 'CustomAlertSound')
      if (soundAction && soundAction.values.length >= 2) {
        setSoundFile(soundAction.values[0] as string)
        setSoundVolume(soundAction.values[1] as number)
      }

      // Icon
      const iconAction = rule.actions.find(action => action.type === 'MinimapIcon')
      if (iconAction && iconAction.values.length >= 3) {
        setIconSize(iconAction.values[0] as number)
        setIconColor(iconAction.values[1] as string)
        setIconType(iconAction.values[2] as string)
      }
    }
  }, [rule])

  const updateRuleAction = (actionType: string, values: (string | number)[]) => {
    const updatedRule = { ...rule }
    const actionIndex = updatedRule.actions.findIndex(action => action.type === actionType)
    
    if (actionIndex >= 0) {
      updatedRule.actions[actionIndex] = { type: actionType as any, values }
    } else {
      updatedRule.actions.push({ type: actionType as any, values })
    }
    
    onUpdateRule(updatedRule)
  }

  const handleTextColorChange = (color: string) => {
    setTextColor(color)
    const rgb = hexToRgb(color)
    updateRuleAction('SetTextColor', [rgb.r, rgb.g, rgb.b])
  }

  const handleBorderColorChange = (color: string) => {
    setBorderColor(color)
    const rgb = hexToRgb(color)
    updateRuleAction('SetBorderColor', [rgb.r, rgb.g, rgb.b])
  }

  const handleBackgroundColorChange = (color: string) => {
    setBackgroundColor(color)
    const rgb = hexToRgb(color)
    updateRuleAction('SetBackgroundColor', [rgb.r, rgb.g, rgb.b])
  }

  const handleFontSizeChange = (size: number) => {
    setFontSize(size)
    updateRuleAction('SetFontSize', [size])
  }

  const handleSoundChange = (file: string, volume: number) => {
    setSoundFile(file)
    setSoundVolume(volume)
    updateRuleAction('CustomAlertSound', [file, volume])
  }

  const handleIconChange = (size: number, color: string, type: string) => {
    setIconSize(size)
    setIconColor(color)
    setIconType(type)
    updateRuleAction('MinimapIcon', [size, color, type])
  }

  const soundFiles = [
    'currency.mp3',
    'divine.mp3',
    'mirror.mp3',
    'unique.mp3',
    'rare.mp3',
    'jewel.mp3',
    'base_item.mp3',
    'gacha.mp3',
    'salvage.mp3',
    'special_currency.mp3',
    'waystone.mp3'
  ]

  const iconTypes = ['Star', 'Circle', 'Diamond', 'Square', 'Triangle', 'Cross']
  const iconColors = ['Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'White', 'Black']

  return (
    <div className="w-80 bg-gray-800/50 backdrop-blur-sm border-l border-gray-700/50 p-6 overflow-y-auto">
      <div className="mb-6">
        <h3 className="text-heading text-white mb-2">Properties</h3>
        <p className="text-caption">Edit rule properties</p>
      </div>

      {/* Rule Info */}
      <div className="card-glass p-4 mb-6">
        <h4 className="font-semibold text-white mb-2">{rule.name}</h4>
        <div className="space-y-1 text-sm text-gray-400">
          <div>Category: {rule.category}</div>
          <div>Priority: {rule.priority}</div>
          <div>Status: <span className={rule.enabled ? 'text-green-400' : 'text-red-400'}>{rule.enabled ? 'Enabled' : 'Disabled'}</span></div>
        </div>
      </div>

      {/* Colors Section */}
      <div className="card-glass p-4 mb-6">
        <div className="flex items-center mb-4">
          <Palette className="w-5 h-5 text-blue-400 mr-2" />
          <h4 className="font-semibold text-white">Colors</h4>
        </div>

        <div className="space-y-4">
          {/* Text Color */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Text Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={textColor}
                onChange={(e) => handleTextColorChange(e.target.value)}
                className="w-12 h-8 rounded border border-gray-600 cursor-pointer"
              />
              <input
                type="text"
                value={textColor}
                onChange={(e) => handleTextColorChange(e.target.value)}
                className="flex-1 input-modern focus-modern"
              />
            </div>
            <div className="mt-2 flex items-center space-x-2">
              <div 
                className="w-6 h-6 rounded border border-gray-600"
                style={{ backgroundColor: textColor }}
              />
              <span className="text-sm text-gray-400">
                RGB: {hexToRgb(textColor).r}, {hexToRgb(textColor).g}, {hexToRgb(textColor).b}
              </span>
            </div>
          </div>

          {/* Border Color */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Border Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={borderColor}
                onChange={(e) => handleBorderColorChange(e.target.value)}
                className="w-12 h-8 rounded border border-gray-600 cursor-pointer"
              />
              <input
                type="text"
                value={borderColor}
                onChange={(e) => handleBorderColorChange(e.target.value)}
                className="flex-1 input-modern focus-modern"
              />
            </div>
            <div className="mt-2 flex items-center space-x-2">
              <div 
                className="w-6 h-6 rounded border border-gray-600"
                style={{ backgroundColor: borderColor }}
              />
              <span className="text-sm text-gray-400">
                RGB: {hexToRgb(borderColor).r}, {hexToRgb(borderColor).g}, {hexToRgb(borderColor).b}
              </span>
            </div>
          </div>

          {/* Background Color */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Background Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={backgroundColor}
                onChange={(e) => handleBackgroundColorChange(e.target.value)}
                className="w-12 h-8 rounded border border-gray-600 cursor-pointer"
              />
              <input
                type="text"
                value={backgroundColor}
                onChange={(e) => handleBackgroundColorChange(e.target.value)}
                className="flex-1 input-modern focus-modern"
              />
            </div>
            <div className="mt-2 flex items-center space-x-2">
              <div 
                className="w-6 h-6 rounded border border-gray-600"
                style={{ backgroundColor: backgroundColor }}
              />
              <span className="text-sm text-gray-400">
                RGB: {hexToRgb(backgroundColor).r}, {hexToRgb(backgroundColor).g}, {hexToRgb(backgroundColor).b}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Font Size */}
      <div className="card-glass p-4 mb-6">
        <div className="flex items-center mb-4">
          <Settings className="w-5 h-5 text-purple-400 mr-2" />
          <h4 className="font-semibold text-white">Font Size</h4>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Size: {fontSize}px
          </label>
          <input
            type="range"
            min="12"
            max="60"
            value={fontSize}
            onChange={(e) => handleFontSizeChange(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>12px</span>
            <span>60px</span>
          </div>
        </div>
      </div>

      {/* Sound Effects */}
      <div className="card-glass p-4 mb-6">
        <div className="flex items-center mb-4">
          <Volume2 className="w-5 h-5 text-green-400 mr-2" />
          <h4 className="font-semibold text-white">Sound Effects</h4>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Sound File
            </label>
            <select
              value={soundFile}
              onChange={(e) => handleSoundChange(e.target.value, soundVolume)}
              className="input-modern focus-modern"
            >
              <option value="">No Sound</option>
              {soundFiles.map(file => (
                <option key={file} value={file}>{file}</option>
              ))}
            </select>
          </div>

          {soundFile && (
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Volume: {soundVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={soundVolume}
                onChange={(e) => handleSoundChange(soundFile, parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>0%</span>
                <span>100%</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Minimap Icon */}
      <div className="card-glass p-4 mb-6">
        <div className="flex items-center mb-4">
          <Image className="w-5 h-5 text-yellow-400 mr-2" />
          <h4 className="font-semibold text-white">Minimap Icon</h4>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Icon Size: {iconSize}
            </label>
            <input
              type="range"
              min="0"
              max="3"
              value={iconSize}
              onChange={(e) => handleIconChange(parseInt(e.target.value), iconColor, iconType)}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>0</span>
              <span>3</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Icon Color
            </label>
            <select
              value={iconColor}
              onChange={(e) => handleIconChange(iconSize, e.target.value, iconType)}
              className="input-modern focus-modern"
            >
              {iconColors.map(color => (
                <option key={color} value={color}>{color}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Icon Type
            </label>
            <select
              value={iconType}
              onChange={(e) => handleIconChange(iconSize, iconColor, e.target.value)}
              className="input-modern focus-modern"
            >
              {iconTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Preview */}
      <div className="card-glass p-4">
        <h4 className="font-semibold text-white mb-4">Preview</h4>
        <div 
          className="p-4 rounded-lg border-2"
          style={{
            color: textColor,
            borderColor: borderColor,
            backgroundColor: backgroundColor,
            fontSize: `${fontSize}px`
          }}
        >
          <div className="font-bold">Sample Item</div>
          <div className="text-sm opacity-80">This is how your item will look</div>
          {soundFile && (
            <div className="text-xs opacity-60 mt-2">🔊 {soundFile}</div>
          )}
        </div>
      </div>
    </div>
  )
}