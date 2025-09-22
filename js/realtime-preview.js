// DZX Filter Editor - Realtime Preview System

class RealtimePreview {
    constructor(filterEditor) {
        this.filterEditor = filterEditor;
        this.previewItems = [];
        this.currentFilter = null;
        this.soundCache = new Map();
        this.animationFrameId = null;
        this.isPreviewActive = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadSampleItems();
        this.startPreviewLoop();
    }
    
    setupEventListeners() {
        // Listen for rule changes
        document.addEventListener('ruleUpdated', (e) => {
            this.updatePreview();
        });
        
        // Listen for filter changes
        document.addEventListener('filterChanged', (e) => {
            this.updatePreview();
        });
        
        // Preview controls
        const refreshBtn = document.getElementById('refreshPreview');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshPreview();
            });
        }
        
        const playSoundBtn = document.getElementById('playSound');
        if (playSoundBtn) {
            playSoundBtn.addEventListener('click', () => {
                this.testAllSounds();
            });
        }
    }
    
    loadSampleItems() {
        // Load sample items for preview
        this.sampleItems = [
            {
                name: 'Chaos Orb',
                type: 'Currency',
                rarity: 'Normal',
                class: 'Currency',
                baseType: 'Chaos Orb',
                itemLevel: 1,
                areaLevel: 1
            },
            {
                name: 'Mirror of Kalandra',
                type: 'Currency',
                rarity: 'Normal',
                class: 'Currency',
                baseType: 'Mirror',
                itemLevel: 1,
                areaLevel: 1
            },
            {
                name: 'Divine Orb',
                type: 'Currency',
                rarity: 'Normal',
                class: 'Currency',
                baseType: 'Divine',
                itemLevel: 1,
                areaLevel: 1
            },
            {
                name: 'Exalted Orb',
                type: 'Currency',
                rarity: 'Normal',
                class: 'Currency',
                baseType: 'Exalted Orb',
                itemLevel: 1,
                areaLevel: 1
            },
            {
                name: 'Gold Ring',
                type: 'Ring',
                rarity: 'Rare',
                class: 'Rings',
                baseType: 'Gold Ring',
                itemLevel: 75,
                areaLevel: 70
            },
            {
                name: 'Heavy Belt',
                type: 'Belt',
                rarity: 'Magic',
                class: 'Belts',
                baseType: 'Heavy Belt',
                itemLevel: 80,
                areaLevel: 75
            },
            {
                name: 'Jade Amulet',
                type: 'Amulet',
                rarity: 'Normal',
                class: 'Amulets',
                baseType: 'Jade Amulet',
                itemLevel: 82,
                areaLevel: 80
            },
            {
                name: 'Timeless Jewel',
                type: 'Jewel',
                rarity: 'Unique',
                class: 'Jewel',
                baseType: 'Timeless Jewel',
                itemLevel: 84,
                areaLevel: 83
            }
        ];
    }
    
    startPreviewLoop() {
        this.isPreviewActive = true;
        this.updatePreview();
    }
    
    stopPreviewLoop() {
        this.isPreviewActive = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
    }
    
    updatePreview() {
        if (!this.isPreviewActive) return;
        
        this.generatePreviewItems();
        this.renderPreview();
        
        // Schedule next update
        this.animationFrameId = requestAnimationFrame(() => {
            if (this.isPreviewActive) {
                this.updatePreview();
            }
        });
    }
    
    generatePreviewItems() {
        this.previewItems = [];
        
        if (!this.filterEditor.rules) return;
        
        // Generate preview items based on current rules
        this.sampleItems.forEach(sampleItem => {
            const previewItem = this.createPreviewItem(sampleItem);
            if (previewItem) {
                this.previewItems.push(previewItem);
            }
        });
    }
    
    createPreviewItem(sampleItem) {
        // Find matching rules
        const matchingRules = this.findMatchingRules(sampleItem);
        
        if (matchingRules.length === 0) {
            return null; // Item would be hidden
        }
        
        // Get the highest priority rule
        const rule = matchingRules[0];
        
        // Create preview item
        const previewItem = {
            ...sampleItem,
            rule: rule,
            style: this.generateItemStyle(rule),
            sound: this.getSoundFromRule(rule),
            icon: this.getIconFromRule(rule)
        };
        
        return previewItem;
    }
    
    findMatchingRules(item) {
        const matchingRules = [];
        
        this.filterEditor.rules.forEach(rule => {
            if (!rule.enabled) return;
            
            if (this.itemMatchesRule(item, rule)) {
                matchingRules.push(rule);
            }
        });
        
        // Sort by priority (simplified - in real implementation, you'd have priority system)
        return matchingRules.sort((a, b) => {
            // Rules with more specific conditions have higher priority
            return b.conditions.length - a.conditions.length;
        });
    }
    
    itemMatchesRule(item, rule) {
        // Check if item matches all conditions in the rule
        return rule.conditions.every(condition => {
            return this.itemMatchesCondition(item, condition);
        });
    }
    
    itemMatchesCondition(item, condition) {
        const itemValue = this.getItemValue(item, condition.type);
        const conditionValues = condition.values;
        const operator = condition.operator;
        
        switch (operator) {
            case '==':
                return conditionValues.includes(itemValue);
            case '!=':
                return !conditionValues.includes(itemValue);
            case '>=':
                return itemValue >= parseFloat(conditionValues[0]);
            case '<=':
                return itemValue <= parseFloat(conditionValues[0]);
            case '>':
                return itemValue > parseFloat(conditionValues[0]);
            case '<':
                return itemValue < parseFloat(conditionValues[0]);
            default:
                return false;
        }
    }
    
    getItemValue(item, conditionType) {
        switch (conditionType) {
            case 'Class':
                return item.class;
            case 'BaseType':
                return item.baseType;
            case 'Rarity':
                return item.rarity;
            case 'ItemLevel':
                return item.itemLevel;
            case 'AreaLevel':
                return item.areaLevel;
            case 'Sockets':
                return item.sockets || 0;
            case 'Quality':
                return item.quality || 0;
            default:
                return null;
        }
    }
    
    generateItemStyle(rule) {
        const style = {
            color: '#ffffff',
            borderColor: 'transparent',
            backgroundColor: 'transparent',
            fontSize: '16px',
            fontWeight: 'normal',
            textDecoration: 'none',
            opacity: '1'
        };
        
        // Apply actions from rule
        rule.actions.forEach(action => {
            switch (action.type) {
                case 'SetTextColor':
                    if (action.values.length >= 3) {
                        style.color = `rgb(${action.values[0]}, ${action.values[1]}, ${action.values[2]})`;
                    }
                    break;
                    
                case 'SetBorderColor':
                    if (action.values.length >= 3) {
                        style.borderColor = `rgb(${action.values[0]}, ${action.values[1]}, ${action.values[2]})`;
                        style.borderWidth = '2px';
                        style.borderStyle = 'solid';
                    }
                    break;
                    
                case 'SetBackgroundColor':
                    if (action.values.length >= 3) {
                        style.backgroundColor = `rgb(${action.values[0]}, ${action.values[1]}, ${action.values[2]})`;
                    }
                    break;
                    
                case 'SetFontSize':
                    if (action.values.length >= 1) {
                        style.fontSize = `${action.values[0]}px`;
                    }
                    break;
                    
                case 'PlayEffect':
                    // Add effect class for CSS animations
                    if (action.values.length >= 1) {
                        style.effect = action.values[0];
                    }
                    break;
            }
        });
        
        return style;
    }
    
    getSoundFromRule(rule) {
        const soundAction = rule.actions.find(action => action.type === 'CustomAlertSound');
        if (soundAction && soundAction.values.length >= 2) {
            return {
                file: soundAction.values[0],
                volume: soundAction.values[1] / 100
            };
        }
        return null;
    }
    
    getIconFromRule(rule) {
        const iconAction = rule.actions.find(action => action.type === 'MinimapIcon');
        if (iconAction && iconAction.values.length >= 3) {
            return {
                size: iconAction.values[0],
                color: iconAction.values[1],
                type: iconAction.values[2]
            };
        }
        return null;
    }
    
    renderPreview() {
        const previewArea = document.getElementById('previewArea');
        if (!previewArea) return;
        
        // Clear existing preview
        previewArea.innerHTML = '';
        
        // Render preview items
        this.previewItems.forEach(item => {
            const itemElement = this.createPreviewElement(item);
            previewArea.appendChild(itemElement);
        });
        
        // Add empty state if no items
        if (this.previewItems.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'preview-empty';
            emptyState.innerHTML = `
                <i class="fas fa-eye-slash"></i>
                <p>No items match current filter rules</p>
            `;
            previewArea.appendChild(emptyState);
        }
    }
    
    createPreviewElement(item) {
        const div = document.createElement('div');
        div.className = 'preview-item';
        div.dataset.itemName = item.name;
        div.dataset.itemType = item.type;
        
        // Apply styles
        Object.assign(div.style, item.style);
        
        // Add effect classes
        if (item.style.effect) {
            div.classList.add(`effect-${item.style.effect.toLowerCase()}`);
        }
        
        // Create content
        div.innerHTML = `
            <div class="preview-item-header">
                <div class="preview-item-name">${item.name}</div>
                <div class="preview-item-icon">${this.createIconElement(item.icon)}</div>
            </div>
            <div class="preview-item-details">
                <div class="preview-item-type">${item.type}</div>
                <div class="preview-item-rarity">${item.rarity}</div>
                <div class="preview-item-level">Level ${item.itemLevel}</div>
            </div>
            <div class="preview-item-rule">
                <small>Rule: ${item.rule.comment || 'Unnamed'}</small>
            </div>
        `;
        
        // Add click handler for sound testing
        if (item.sound) {
            div.addEventListener('click', () => {
                this.playSound(item.sound);
            });
            div.style.cursor = 'pointer';
            div.title = 'Click to test sound';
        }
        
        return div;
    }
    
    createIconElement(icon) {
        if (!icon) return '';
        
        const iconMap = {
            'Circle': '●',
            'Diamond': '◆',
            'Star': '★',
            'Square': '■'
        };
        
        const iconChar = iconMap[icon.type] || '●';
        const colorClass = `icon-${icon.color.toLowerCase()}`;
        
        return `<span class="minimap-icon ${colorClass}" data-size="${icon.size}">${iconChar}</span>`;
    }
    
    playSound(sound) {
        if (!sound || !sound.file) return;
        
        // Check cache first
        if (this.soundCache.has(sound.file)) {
            const audio = this.soundCache.get(sound.file);
            audio.currentTime = 0;
            audio.volume = sound.volume;
            audio.play().catch(e => console.log('Could not play sound:', e));
            return;
        }
        
        // Load and cache sound
        const audio = new Audio(`dzx_filter/soundeffect/type-01/${sound.file}`);
        audio.volume = sound.volume;
        
        audio.addEventListener('canplaythrough', () => {
            this.soundCache.set(sound.file, audio);
            audio.play().catch(e => console.log('Could not play sound:', e));
        });
        
        audio.addEventListener('error', (e) => {
            console.log('Error loading sound:', e);
        });
        
        audio.load();
    }
    
    testAllSounds() {
        const uniqueSounds = new Set();
        
        this.previewItems.forEach(item => {
            if (item.sound) {
                uniqueSounds.add(item.sound.file);
            }
        });
        
        // Play each unique sound with a delay
        let delay = 0;
        uniqueSounds.forEach(soundFile => {
            setTimeout(() => {
                this.playSound({ file: soundFile, volume: 0.5 });
            }, delay);
            delay += 1000; // 1 second between sounds
        });
    }
    
    refreshPreview() {
        this.stopPreviewLoop();
        setTimeout(() => {
            this.startPreviewLoop();
        }, 100);
    }
    
    // Advanced preview features
    addCustomItem(itemData) {
        this.sampleItems.push(itemData);
        this.updatePreview();
    }
    
    removeCustomItem(itemName) {
        this.sampleItems = this.sampleItems.filter(item => item.name !== itemName);
        this.updatePreview();
    }
    
    updateItemLevel(itemName, newLevel) {
        const item = this.sampleItems.find(item => item.name === itemName);
        if (item) {
            item.itemLevel = newLevel;
            this.updatePreview();
        }
    }
    
    updateAreaLevel(itemName, newLevel) {
        const item = this.sampleItems.find(item => item.name === itemName);
        if (item) {
            item.areaLevel = newLevel;
            this.updatePreview();
        }
    }
    
    // Preview statistics
    getPreviewStats() {
        const stats = {
            totalItems: this.sampleItems.length,
            visibleItems: this.previewItems.length,
            hiddenItems: this.sampleItems.length - this.previewItems.length,
            rulesApplied: this.filterEditor.rules.filter(rule => rule.enabled).length,
            soundsUsed: new Set(this.previewItems.map(item => item.sound?.file).filter(Boolean)).size
        };
        
        return stats;
    }
    
    // Export preview data
    exportPreviewData() {
        return {
            items: this.previewItems,
            stats: this.getPreviewStats(),
            timestamp: new Date().toISOString()
        };
    }
    
    // Import preview data
    importPreviewData(data) {
        if (data.items) {
            this.previewItems = data.items;
            this.renderPreview();
        }
    }
}

// CSS for preview effects
const previewStyles = `
<style>
.preview-item {
    transition: all 0.3s ease;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
}

.preview-item:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.preview-item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.preview-item-name {
    font-weight: 600;
    font-size: 1.1em;
}

.preview-item-icon {
    font-size: 1.2em;
}

.preview-item-details {
    display: flex;
    gap: 0.5rem;
    font-size: 0.9em;
    color: #ccc;
    margin-bottom: 0.5rem;
}

.preview-item-rule {
    font-size: 0.8em;
    color: #888;
    border-top: 1px solid #333;
    padding-top: 0.5rem;
}

.preview-empty {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.preview-empty i {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.minimap-icon {
    display: inline-block;
    font-weight: bold;
}

.icon-red { color: #ff4444; }
.icon-blue { color: #4444ff; }
.icon-green { color: #44ff44; }
.icon-yellow { color: #ffff44; }
.icon-purple { color: #ff44ff; }
.icon-white { color: #ffffff; }

.effect-red {
    animation: pulse-red 2s infinite;
}

.effect-blue {
    animation: pulse-blue 2s infinite;
}

.effect-green {
    animation: pulse-green 2s infinite;
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 5px rgba(255, 68, 68, 0.5); }
    50% { box-shadow: 0 0 20px rgba(255, 68, 68, 0.8); }
}

@keyframes pulse-blue {
    0%, 100% { box-shadow: 0 0 5px rgba(68, 68, 255, 0.5); }
    50% { box-shadow: 0 0 20px rgba(68, 68, 255, 0.8); }
}

@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 5px rgba(68, 255, 68, 0.5); }
    50% { box-shadow: 0 0 20px rgba(68, 255, 68, 0.8); }
}
</style>
`;

// Inject styles
if (typeof document !== 'undefined') {
    document.head.insertAdjacentHTML('beforeend', previewStyles);
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RealtimePreview;
}
