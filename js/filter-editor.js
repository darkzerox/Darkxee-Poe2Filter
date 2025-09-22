// DZX Filter Editor - Main JavaScript

class FilterEditor {
    constructor() {
        this.currentFilter = null;
        this.currentCategory = 'currency';
        this.currentSection = 'high-value';
        this.selectedRule = null;
        this.rules = [];
        this.categories = {
            currency: { name: 'Currency', icon: 'fas fa-coins' },
            equipment: { name: 'Equipment', icon: 'fas fa-shield-alt' },
            jewels: { name: 'Jewels', icon: 'fas fa-gem' },
            maps: { name: 'Maps', icon: 'fas fa-map' },
            special: { name: 'Special Items', icon: 'fas fa-star' }
        };
        
        // Initialize managers
        this.importExportManager = null;
        this.realtimePreview = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadDefaultFilter();
        this.initializeManagers();
        this.updateUI();
    }
    
    initializeManagers() {
        // Initialize Import/Export Manager
        if (typeof ImportExportManager !== 'undefined') {
            this.importExportManager = new ImportExportManager(this);
        }
        
        // Initialize Realtime Preview
        if (typeof RealtimePreview !== 'undefined') {
            this.realtimePreview = new RealtimePreview(this);
        }
    }
    
    setupEventListeners() {
        // Header buttons
        document.getElementById('importBtn').addEventListener('click', () => this.importFilter());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportFilter());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveFilter());
        
        // Category selection
        document.querySelectorAll('.category-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.selectCategory(e.currentTarget.dataset.category);
            });
        });
        
        // Section selection
        document.querySelectorAll('.section-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.selectSection(e.currentTarget.dataset.section);
            });
        });
        
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.currentTarget.dataset.tab);
            });
        });
        
        // Tool buttons
        document.getElementById('addRuleBtn').addEventListener('click', () => this.addRule());
        document.getElementById('duplicateRuleBtn').addEventListener('click', () => this.duplicateRule());
        document.getElementById('deleteRuleBtn').addEventListener('click', () => this.deleteRule());
        
        // Properties panel
        this.setupPropertiesListeners();
        
        // Search and filter
        document.getElementById('searchRules').addEventListener('input', (e) => {
            this.filterRules(e.target.value);
        });
        
        document.getElementById('ruleFilter').addEventListener('change', (e) => {
            this.filterRulesByType(e.target.value);
        });
        
        // Preview controls
        document.getElementById('refreshPreview').addEventListener('click', () => {
            this.refreshPreview();
        });
        
        document.getElementById('playSound').addEventListener('click', () => {
            this.testSound();
        });
    }
    
    setupPropertiesListeners() {
        // Color inputs
        ['textColor', 'borderColor', 'backgroundColor'].forEach(colorId => {
            const colorInput = document.getElementById(colorId);
            const rgbInput = document.getElementById(colorId + 'RGB');
            
            colorInput.addEventListener('change', (e) => {
                const rgb = this.hexToRgb(e.target.value);
                if (rgb) {
                    rgbInput.value = `${rgb.r} ${rgb.g} ${rgb.b}`;
                }
                this.updateSelectedRule();
            });
            
            rgbInput.addEventListener('input', (e) => {
                const rgb = e.target.value.split(' ').map(Number);
                if (rgb.length === 3 && rgb.every(n => !isNaN(n) && n >= 0 && n <= 255)) {
                    const hex = this.rgbToHex(rgb[0], rgb[1], rgb[2]);
                    colorInput.value = hex;
                }
                this.updateSelectedRule();
            });
        });
        
        // Font size
        document.getElementById('fontSizeInput').addEventListener('input', (e) => {
            this.updateSelectedRule();
        });
        
        // Sound properties
        document.getElementById('soundFile').addEventListener('change', () => {
            this.updateSelectedRule();
        });
        
        document.getElementById('soundVolume').addEventListener('input', (e) => {
            document.getElementById('soundVolumeValue').textContent = e.target.value + '%';
            this.updateSelectedRule();
        });
        
        document.getElementById('testSound').addEventListener('click', () => {
            this.testSelectedSound();
        });
        
        // Icon properties
        ['iconType', 'iconColor', 'iconSize'].forEach(propId => {
            document.getElementById(propId).addEventListener('change', () => {
                this.updateSelectedRule();
            });
        });
        
        // Add condition/action buttons
        document.getElementById('addCondition').addEventListener('click', () => {
            this.addCondition();
        });
        
        document.getElementById('addAction').addEventListener('click', () => {
            this.addAction();
        });
    }
    
    loadDefaultFilter() {
        // Load default filter data
        this.currentFilter = {
            name: 'DZX Custom Filter',
            platform: 'pc',
            soundType: 'type-01',
            rules: this.generateDefaultRules()
        };
        
        this.rules = this.currentFilter.rules;
        this.updateRulesList();
    }
    
    generateDefaultRules() {
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
        ];
    }
    
    selectCategory(category) {
        this.currentCategory = category;
        
        // Update UI
        document.querySelectorAll('.category-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');
        
        this.updateRulesList();
    }
    
    selectSection(section) {
        this.currentSection = section;
        
        // Update UI
        document.querySelectorAll('.section-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');
        
        this.updateRulesList();
    }
    
    switchTab(tabName) {
        // Update tab UI
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName + 'Tab').classList.add('active');
        
        // Update content based on tab
        if (tabName === 'preview') {
            this.refreshPreview();
        }
    }
    
    updateRulesList() {
        const rulesList = document.getElementById('rulesList');
        rulesList.innerHTML = '';
        
        const filteredRules = this.rules.filter(rule => {
            // Filter by category and section (simplified for demo)
            return rule.enabled;
        });
        
        filteredRules.forEach(rule => {
            const ruleElement = this.createRuleElement(rule);
            rulesList.appendChild(ruleElement);
        });
    }
    
    createRuleElement(rule) {
        const div = document.createElement('div');
        div.className = 'rule-item';
        div.dataset.ruleId = rule.id;
        
        const conditionsText = rule.conditions.map(c => 
            `${c.type} ${c.operator} ${c.values.join(' ')}`
        ).join(', ');
        
        const actionsText = rule.actions.map(a => 
            `${a.type} ${a.values.join(' ')}`
        ).join(', ');
        
        div.innerHTML = `
            <div class="rule-header">
                <div class="rule-title">${rule.comment || 'Unnamed Rule'}</div>
                <div class="rule-type ${rule.show_hide.toLowerCase()}">${rule.show_hide}</div>
            </div>
            <div class="rule-conditions">
                <h5>Conditions:</h5>
                <div class="condition-item">${conditionsText}</div>
            </div>
            <div class="rule-actions">
                <h5>Actions:</h5>
                <div class="action-item">${actionsText}</div>
            </div>
        `;
        
        div.addEventListener('click', () => {
            this.selectRule(rule);
        });
        
        return div;
    }
    
    selectRule(rule) {
        this.selectedRule = rule;
        
        // Update UI
        document.querySelectorAll('.rule-item').forEach(item => {
            item.classList.remove('selected');
        });
        document.querySelector(`[data-rule-id="${rule.id}"]`).classList.add('selected');
        
        // Update properties panel
        this.updatePropertiesPanel(rule);
    }
    
    updatePropertiesPanel(rule) {
        // Update conditions
        const conditionList = document.getElementById('conditionList');
        conditionList.innerHTML = '';
        
        rule.conditions.forEach(condition => {
            const div = document.createElement('div');
            div.className = 'condition-item';
            div.innerHTML = `
                <span>${condition.type} ${condition.operator} ${condition.values.join(' ')}</span>
                <button class="btn-close" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            `;
            conditionList.appendChild(div);
        });
        
        // Update actions
        const actionList = document.getElementById('actionList');
        actionList.innerHTML = '';
        
        rule.actions.forEach(action => {
            const div = document.createElement('div');
            div.className = 'action-item';
            div.innerHTML = `
                <span>${action.type} ${action.values.join(' ')}</span>
                <button class="btn-close" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            `;
            actionList.appendChild(div);
        });
        
        // Update visual properties
        this.updateVisualProperties(rule);
    }
    
    updateVisualProperties(rule) {
        // Find color actions
        const textColorAction = rule.actions.find(a => a.type === 'SetTextColor');
        const borderColorAction = rule.actions.find(a => a.type === 'SetBorderColor');
        const backgroundColorAction = rule.actions.find(a => a.type === 'SetBackgroundColor');
        const fontSizeAction = rule.actions.find(a => a.type === 'SetFontSize');
        
        if (textColorAction) {
            const hex = this.rgbToHex(textColorAction.values[0], textColorAction.values[1], textColorAction.values[2]);
            document.getElementById('textColor').value = hex;
            document.getElementById('textColorRGB').value = textColorAction.values.join(' ');
        }
        
        if (borderColorAction) {
            const hex = this.rgbToHex(borderColorAction.values[0], borderColorAction.values[1], borderColorAction.values[2]);
            document.getElementById('borderColor').value = hex;
            document.getElementById('borderColorRGB').value = borderColorAction.values.join(' ');
        }
        
        if (backgroundColorAction) {
            const hex = this.rgbToHex(backgroundColorAction.values[0], backgroundColorAction.values[1], backgroundColorAction.values[2]);
            document.getElementById('backgroundColor').value = hex;
            document.getElementById('backgroundColorRGB').value = backgroundColorAction.values.join(' ');
        }
        
        if (fontSizeAction) {
            document.getElementById('fontSizeInput').value = fontSizeAction.values[0];
        }
        
        // Update sound properties
        const soundAction = rule.actions.find(a => a.type === 'CustomAlertSound');
        if (soundAction) {
            document.getElementById('soundFile').value = soundAction.values[0];
            document.getElementById('soundVolume').value = soundAction.values[1];
            document.getElementById('soundVolumeValue').textContent = soundAction.values[1] + '%';
        }
        
        // Update icon properties
        const iconAction = rule.actions.find(a => a.type === 'MinimapIcon');
        if (iconAction) {
            document.getElementById('iconType').value = iconAction.values[2];
            document.getElementById('iconColor').value = iconAction.values[1];
            document.getElementById('iconSize').value = iconAction.values[0];
        }
    }
    
    updateSelectedRule() {
        if (!this.selectedRule) return;
        
        // Update visual properties
        const textColorRGB = document.getElementById('textColorRGB').value.split(' ').map(Number);
        const borderColorRGB = document.getElementById('borderColorRGB').value.split(' ').map(Number);
        const backgroundColorRGB = document.getElementById('backgroundColorRGB').value.split(' ').map(Number);
        const fontSize = parseInt(document.getElementById('fontSizeInput').value);
        
        // Update actions
        this.updateAction(this.selectedRule, 'SetTextColor', textColorRGB);
        this.updateAction(this.selectedRule, 'SetBorderColor', borderColorRGB);
        this.updateAction(this.selectedRule, 'SetBackgroundColor', backgroundColorRGB);
        this.updateAction(this.selectedRule, 'SetFontSize', [fontSize]);
        
        // Update sound
        const soundFile = document.getElementById('soundFile').value;
        const soundVolume = parseInt(document.getElementById('soundVolume').value);
        this.updateAction(this.selectedRule, 'CustomAlertSound', [soundFile, soundVolume]);
        
        // Update icon
        const iconType = document.getElementById('iconType').value;
        const iconColor = document.getElementById('iconColor').value;
        const iconSize = parseInt(document.getElementById('iconSize').value);
        this.updateAction(this.selectedRule, 'MinimapIcon', [iconSize, iconColor, iconType]);
        
        // Refresh preview
        this.refreshPreview();
    }
    
    updateAction(rule, actionType, values) {
        let action = rule.actions.find(a => a.type === actionType);
        if (action) {
            action.values = values;
        } else {
            rule.actions.push({ type: actionType, values: values });
        }
    }
    
    addRule() {
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
        };
        
        this.rules.push(newRule);
        this.updateRulesList();
        this.selectRule(newRule);
    }
    
    duplicateRule() {
        if (!this.selectedRule) return;
        
        const duplicatedRule = {
            ...this.selectedRule,
            id: 'rule_' + Date.now(),
            comment: this.selectedRule.comment + ' (Copy)'
        };
        
        this.rules.push(duplicatedRule);
        this.updateRulesList();
        this.selectRule(duplicatedRule);
    }
    
    deleteRule() {
        if (!this.selectedRule) return;
        
        if (confirm('Are you sure you want to delete this rule?')) {
            this.rules = this.rules.filter(rule => rule.id !== this.selectedRule.id);
            this.selectedRule = null;
            this.updateRulesList();
            this.clearPropertiesPanel();
        }
    }
    
    clearPropertiesPanel() {
        document.getElementById('conditionList').innerHTML = '';
        document.getElementById('actionList').innerHTML = '';
        
        // Reset visual properties
        document.getElementById('textColor').value = '#ffffff';
        document.getElementById('textColorRGB').value = '255 255 255';
        document.getElementById('borderColor').value = '#ff0000';
        document.getElementById('borderColorRGB').value = '255 0 0';
        document.getElementById('backgroundColor').value = '#000000';
        document.getElementById('backgroundColorRGB').value = '0 0 0';
        document.getElementById('fontSizeInput').value = '32';
    }
    
    filterRules(searchTerm) {
        const ruleItems = document.querySelectorAll('.rule-item');
        
        ruleItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            const matches = text.includes(searchTerm.toLowerCase());
            item.style.display = matches ? 'block' : 'none';
        });
    }
    
    filterRulesByType(type) {
        const ruleItems = document.querySelectorAll('.rule-item');
        
        ruleItems.forEach(item => {
            const ruleType = item.querySelector('.rule-type').textContent.toLowerCase();
            const matches = type === 'all' || ruleType === type;
            item.style.display = matches ? 'block' : 'none';
        });
    }
    
    refreshPreview() {
        if (this.realtimePreview) {
            this.realtimePreview.refreshPreview();
        } else {
            // Fallback preview
            const previewArea = document.getElementById('previewArea');
            previewArea.innerHTML = '';
            
            this.rules.forEach(rule => {
                if (rule.enabled && rule.show_hide === 'Show') {
                    const previewItem = this.createPreviewItem(rule);
                    previewArea.appendChild(previewItem);
                }
            });
        }
    }
    
    createPreviewItem(rule) {
        const div = document.createElement('div');
        div.className = 'preview-item';
        
        // Apply styling from rule actions
        const textColorAction = rule.actions.find(a => a.type === 'SetTextColor');
        const borderColorAction = rule.actions.find(a => a.type === 'SetBorderColor');
        const backgroundColorAction = rule.actions.find(a => a.type === 'SetBackgroundColor');
        const fontSizeAction = rule.actions.find(a => a.type === 'SetFontSize');
        
        let style = '';
        if (textColorAction) {
            style += `color: rgb(${textColorAction.values.join(', ')}); `;
        }
        if (borderColorAction) {
            style += `border: 2px solid rgb(${borderColorAction.values.join(', ')}); `;
        }
        if (backgroundColorAction) {
            style += `background-color: rgb(${backgroundColorAction.values.join(', ')}); `;
        }
        if (fontSizeAction) {
            style += `font-size: ${fontSizeAction.values[0]}px; `;
        }
        
        div.style.cssText = style;
        
        div.innerHTML = `
            <div class="preview-item-name">${rule.comment || 'Sample Item'}</div>
            <div class="preview-item-type">${rule.conditions[0]?.values[0] || 'Item'}</div>
        `;
        
        return div;
    }
    
    testSound() {
        // Play a test sound
        const audio = new Audio('dzx_filter/soundeffect/type-01/currency.mp3');
        audio.volume = 0.5;
        audio.play().catch(e => console.log('Could not play sound:', e));
    }
    
    testSelectedSound() {
        if (!this.selectedRule) return;
        
        const soundAction = this.selectedRule.actions.find(a => a.type === 'CustomAlertSound');
        if (soundAction) {
            const audio = new Audio(`dzx_filter/soundeffect/type-01/${soundAction.values[0]}`);
            audio.volume = soundAction.values[1] / 100;
            audio.play().catch(e => console.log('Could not play sound:', e));
        }
    }
    
    async importFilter() {
        if (!this.importExportManager) {
            alert('Import/Export manager not initialized');
            return;
        }
        
        const fileInput = document.getElementById('fileInput');
        fileInput.click();
        
        fileInput.onchange = async (e) => {
            const file = e.target.files[0];
            if (file) {
                try {
                    const result = await this.importExportManager.importFile(file);
                    
                    if (result.success) {
                        alert('Filter imported successfully!');
                        this.updateRulesList();
                        this.refreshPreview();
                    } else {
                        alert('Error importing filter: ' + result.message);
                    }
                } catch (error) {
                    alert('Error importing filter: ' + error.message);
                }
            }
        };
    }
    
    async exportFilter() {
        if (!this.importExportManager) {
            alert('Import/Export manager not initialized');
            return;
        }
        
        try {
            const result = await this.importExportManager.exportFile('filter', this.currentFilter);
            
            if (result.success) {
                alert('Filter exported successfully!');
            } else {
                alert('Error exporting filter: ' + result.message);
            }
        } catch (error) {
            alert('Error exporting filter: ' + error.message);
        }
    }
    
    generateFilterContent() {
        let content = `# ${this.currentFilter.name}\n`;
        content += `# Generated by DZX Filter Editor\n\n`;
        
        this.rules.forEach(rule => {
            if (rule.comment) {
                content += `# ${rule.comment}\n`;
            }
            
            content += `${rule.show_hide}\n`;
            
            rule.conditions.forEach(condition => {
                content += `  ${condition.type} ${condition.operator} ${condition.values.join(' ')}\n`;
            });
            
            rule.actions.forEach(action => {
                if (action.type === 'CustomAlertSound') {
                    content += `  ${action.type} "${action.values[0]}" ${action.values[1]}\n`;
                } else {
                    content += `  ${action.type} ${action.values.join(' ')}\n`;
                }
            });
            
            content += '\n';
        });
        
        return content;
    }
    
    saveFilter() {
        // Save current filter state
        const filterData = {
            ...this.currentFilter,
            rules: this.rules,
            savedAt: new Date().toISOString()
        };
        
        localStorage.setItem('dzx_filter_editor', JSON.stringify(filterData));
        alert('Filter saved successfully!');
    }
    
    updateUI() {
        // Update any UI elements that need refreshing
        this.updateRulesList();
        this.refreshPreview();
    }
    
    // Utility functions
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }
    
    rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }
}

// Initialize the editor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.filterEditor = new FilterEditor();
});
