// DZX Filter Editor - Import/Export Manager

class ImportExportManager {
    constructor(filterEditor) {
        this.filterEditor = filterEditor;
        this.supportedFormats = ['.filter', '.json', '.yaml'];
        this.maxFileSize = 10 * 1024 * 1024; // 10MB
    }
    
    async importFile(file) {
        try {
            // Validate file
            this.validateFile(file);
            
            // Read file content
            const content = await this.readFileContent(file);
            
            // Parse based on file type
            let filterData;
            if (file.name.endsWith('.filter')) {
                filterData = await this.parseFilterFile(content);
            } else if (file.name.endsWith('.json')) {
                filterData = JSON.parse(content);
            } else if (file.name.endsWith('.yaml')) {
                filterData = await this.parseYamlFile(content);
            } else {
                throw new Error('Unsupported file format');
            }
            
            // Validate parsed data
            this.validateFilterData(filterData);
            
            // Import to editor
            this.filterEditor.currentFilter = filterData;
            this.filterEditor.rules = filterData.rules || [];
            this.filterEditor.updateRulesList();
            this.filterEditor.refreshPreview();
            
            return {
                success: true,
                message: 'Filter imported successfully',
                data: filterData
            };
            
        } catch (error) {
            return {
                success: false,
                message: error.message,
                error: error
            };
        }
    }
    
    async exportFile(format, data) {
        try {
            let content;
            let filename;
            let mimeType;
            
            switch (format) {
                case 'filter':
                    content = this.generateFilterContent(data);
                    filename = `${data.name || 'filter'}.filter`;
                    mimeType = 'text/plain';
                    break;
                    
                case 'json':
                    content = JSON.stringify(data, null, 2);
                    filename = `${data.name || 'filter'}.json`;
                    mimeType = 'application/json';
                    break;
                    
                case 'yaml':
                    content = this.generateYamlContent(data);
                    filename = `${data.name || 'filter'}.yaml`;
                    mimeType = 'text/yaml';
                    break;
                    
                default:
                    throw new Error('Unsupported export format');
            }
            
            // Create and download file
            this.downloadFile(content, filename, mimeType);
            
            return {
                success: true,
                message: 'Filter exported successfully',
                filename: filename
            };
            
        } catch (error) {
            return {
                success: false,
                message: error.message,
                error: error
            };
        }
    }
    
    validateFile(file) {
        // Check file size
        if (file.size > this.maxFileSize) {
            throw new Error(`File too large. Maximum size is ${this.maxFileSize / 1024 / 1024}MB`);
        }
        
        // Check file extension
        const extension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
        if (!this.supportedFormats.includes(extension)) {
            throw new Error(`Unsupported file format. Supported formats: ${this.supportedFormats.join(', ')}`);
        }
        
        // Check if file is empty
        if (file.size === 0) {
            throw new Error('File is empty');
        }
    }
    
    async readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                resolve(e.target.result);
            };
            
            reader.onerror = (e) => {
                reject(new Error('Failed to read file'));
            };
            
            reader.readAsText(file, 'utf-8');
        });
    }
    
    async parseFilterFile(content) {
        // Use the FilterParser to parse the content
        if (window.FilterParser) {
            const parser = new window.FilterParser();
            return parser.parse_content(content);
        } else {
            // Fallback parsing (simplified)
            return this.simpleFilterParse(content);
        }
    }
    
    simpleFilterParse(content) {
        const lines = content.split('\n');
        const rules = [];
        let currentRule = null;
        let currentComment = null;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (!line) continue;
            
            if (line.startsWith('#')) {
                currentComment = line.substring(1).trim();
                continue;
            }
            
            if (line.startsWith('Show') || line.startsWith('Hide')) {
                if (currentRule) {
                    rules.push(currentRule);
                }
                
                currentRule = {
                    id: `rule_${rules.length + 1}`,
                    show_hide: line.split()[0],
                    conditions: [],
                    actions: [],
                    comment: currentComment,
                    enabled: true
                };
                currentComment = null;
                continue;
            }
            
            if (currentRule) {
                if (this.isCondition(line)) {
                    const condition = this.parseCondition(line);
                    if (condition) {
                        currentRule.conditions.push(condition);
                    }
                } else if (this.isAction(line)) {
                    const action = this.parseAction(line);
                    if (action) {
                        currentRule.actions.push(action);
                    }
                }
            }
        }
        
        if (currentRule) {
            rules.push(currentRule);
        }
        
        return {
            name: 'Imported Filter',
            platform: 'pc',
            soundType: 'type-01',
            rules: rules,
            metadata: {
                total_rules: rules.length,
                imported_at: new Date().toISOString()
            }
        };
    }
    
    isCondition(line) {
        const conditionKeywords = [
            'Class', 'BaseType', 'Rarity', 'AreaLevel', 'ItemLevel',
            'Sockets', 'Quality', 'Width', 'Height', 'DropLevel'
        ];
        const firstWord = line.split()[0];
        return conditionKeywords.includes(firstWord);
    }
    
    isAction(line) {
        const actionKeywords = [
            'SetTextColor', 'SetBorderColor', 'SetBackgroundColor',
            'SetFontSize', 'PlayEffect', 'MinimapIcon', 'CustomAlertSound',
            'PlayAlertSound', 'DisableDropSound', 'Continue'
        ];
        const firstWord = line.split()[0];
        return actionKeywords.includes(firstWord);
    }
    
    parseCondition(line) {
        try {
            const parts = line.split();
            if (parts.length < 2) return null;
            
            const conditionType = parts[0];
            let values = [];
            let operator = '==';
            
            if (parts.length >= 3) {
                if (['>=', '<=', '>', '<', '==', '!='].includes(parts[1])) {
                    operator = parts[1];
                    values = [parts[2]];
                } else {
                    values = parts.slice(1);
                }
            } else {
                values = [parts[1]];
            }
            
            return {
                type: conditionType,
                operator: operator,
                values: values
            };
        } catch (error) {
            console.error('Error parsing condition:', error);
            return null;
        }
    }
    
    parseAction(line) {
        try {
            const parts = line.split();
            if (parts.length < 2) return null;
            
            const actionType = parts[0];
            let values = [];
            
            if (actionType.includes('Color')) {
                // Parse RGB color values
                const colorMatch = line.match(/(\d+)\s+(\d+)\s+(\d+)(?:\s+(\d+))?/);
                if (colorMatch) {
                    values = [
                        parseInt(colorMatch[1]),
                        parseInt(colorMatch[2]),
                        parseInt(colorMatch[3])
                    ];
                    if (colorMatch[4]) {
                        values.push(parseInt(colorMatch[4]));
                    }
                } else {
                    values = parts.slice(1);
                }
            } else if (actionType === 'SetFontSize') {
                values = [parseInt(parts[1])];
            } else if (actionType === 'CustomAlertSound') {
                const soundMatch = line.match(/"([^"]+)"/);
                const volumeMatch = line.match(/(\d+)$/);
                if (soundMatch && volumeMatch) {
                    values = [soundMatch[1], parseInt(volumeMatch[1])];
                } else {
                    values = parts.slice(1);
                }
            } else {
                values = parts.slice(1);
            }
            
            return {
                type: actionType,
                values: values
            };
        } catch (error) {
            console.error('Error parsing action:', error);
            return null;
        }
    }
    
    async parseYamlFile(content) {
        // Simple YAML parsing (for basic YAML files)
        // In a real implementation, you'd use a YAML parser library
        try {
            const lines = content.split('\n');
            const data = {};
            let currentSection = null;
            
            for (const line of lines) {
                const trimmed = line.trim();
                if (!trimmed || trimmed.startsWith('#')) continue;
                
                if (trimmed.endsWith(':')) {
                    currentSection = trimmed.slice(0, -1);
                    data[currentSection] = {};
                } else if (currentSection && trimmed.includes(':')) {
                    const [key, value] = trimmed.split(':', 2);
                    data[currentSection][key.trim()] = value.trim();
                }
            }
            
            return data;
        } catch (error) {
            throw new Error('Invalid YAML format');
        }
    }
    
    validateFilterData(data) {
        if (!data) {
            throw new Error('No data to validate');
        }
        
        if (!data.rules || !Array.isArray(data.rules)) {
            throw new Error('Invalid filter data: missing or invalid rules array');
        }
        
        // Validate each rule
        data.rules.forEach((rule, index) => {
            if (!rule.id) {
                throw new Error(`Rule ${index + 1}: missing ID`);
            }
            
            if (!rule.show_hide || !['Show', 'Hide'].includes(rule.show_hide)) {
                throw new Error(`Rule ${index + 1}: invalid show/hide value`);
            }
            
            if (!rule.conditions || !Array.isArray(rule.conditions)) {
                throw new Error(`Rule ${index + 1}: missing or invalid conditions`);
            }
            
            if (!rule.actions || !Array.isArray(rule.actions)) {
                throw new Error(`Rule ${index + 1}: missing or invalid actions`);
            }
        });
    }
    
    generateFilterContent(data) {
        let content = `# ${data.name || 'DZX Filter'}\n`;
        content += `# Generated by DZX Filter Editor\n`;
        content += `# Platform: ${data.platform || 'pc'}\n`;
        content += `# Sound Type: ${data.soundType || 'type-01'}\n\n`;
        
        if (data.rules) {
            data.rules.forEach(rule => {
                if (rule.comment) {
                    content += `# ${rule.comment}\n`;
                }
                
                content += `${rule.show_hide}\n`;
                
                if (rule.conditions) {
                    rule.conditions.forEach(condition => {
                        if (condition.operator === '==' && condition.values.length === 1) {
                            content += `  ${condition.type} ${condition.values[0]}\n`;
                        } else if (condition.operator === '==' && condition.values.length > 1) {
                            content += `  ${condition.type} ${condition.values.join(' ')}\n`;
                        } else {
                            content += `  ${condition.type} ${condition.operator} ${condition.values.join(' ')}\n`;
                        }
                    });
                }
                
                if (rule.actions) {
                    rule.actions.forEach(action => {
                        if (action.type.includes('Color') && action.values.length >= 3) {
                            const colorStr = action.values.slice(0, 3).join(' ');
                            const alpha = action.values[3] ? ` ${action.values[3]}` : '';
                            content += `  ${action.type} ${colorStr}${alpha}\n`;
                        } else if (action.type === 'CustomAlertSound' && action.values.length >= 2) {
                            content += `  ${action.type} "${action.values[0]}" ${action.values[1]}\n`;
                        } else {
                            content += `  ${action.type} ${action.values.join(' ')}\n`;
                        }
                    });
                }
                
                content += '\n';
            });
        }
        
        return content;
    }
    
    generateYamlContent(data) {
        let content = `# ${data.name || 'DZX Filter'}\n`;
        content += `# Generated by DZX Filter Editor\n\n`;
        
        content += `metadata:\n`;
        content += `  name: "${data.name || 'DZX Filter'}'\n`;
        content += `  platform: "${data.platform || 'pc'}'\n`;
        content += `  soundType: "${data.soundType || 'type-01'}'\n`;
        content += `  totalRules: ${data.rules ? data.rules.length : 0}\n\n`;
        
        if (data.rules) {
            content += `rules:\n`;
            data.rules.forEach((rule, index) => {
                content += `  - id: "${rule.id}"\n`;
                content += `    show_hide: "${rule.show_hide}"\n`;
                if (rule.comment) {
                    content += `    comment: "${rule.comment}"\n`;
                }
                content += `    enabled: ${rule.enabled}\n`;
                
                if (rule.conditions && rule.conditions.length > 0) {
                    content += `    conditions:\n`;
                    rule.conditions.forEach(condition => {
                        content += `      - type: "${condition.type}"\n`;
                        content += `        operator: "${condition.operator}"\n`;
                        content += `        values: [${condition.values.map(v => `"${v}"`).join(', ')}]\n`;
                    });
                }
                
                if (rule.actions && rule.actions.length > 0) {
                    content += `    actions:\n`;
                    rule.actions.forEach(action => {
                        content += `      - type: "${action.type}"\n`;
                        content += `        values: [${action.values.join(', ')}]\n`;
                    });
                }
                content += '\n';
            });
        }
        
        return content;
    }
    
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }
    
    // Utility methods for file operations
    async loadFromUrl(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const content = await response.text();
            const filename = url.split('/').pop() || 'filter.filter';
            
            // Create a mock file object
            const file = new File([content], filename, { type: 'text/plain' });
            
            return await this.importFile(file);
        } catch (error) {
            return {
                success: false,
                message: `Failed to load from URL: ${error.message}`,
                error: error
            };
        }
    }
    
    async saveToUrl(url, data) {
        try {
            const content = this.generateFilterContent(data);
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    filename: `${data.name || 'filter'}.filter`
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return {
                success: true,
                message: 'Filter saved to URL successfully'
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to save to URL: ${error.message}`,
                error: error
            };
        }
    }
    
    // Backup and restore functionality
    createBackup() {
        const backupData = {
            filter: this.filterEditor.currentFilter,
            rules: this.filterEditor.rules,
            timestamp: new Date().toISOString(),
            version: '1.0.0'
        };
        
        const backupJson = JSON.stringify(backupData, null, 2);
        this.downloadFile(backupJson, `dzx_filter_backup_${Date.now()}.json`, 'application/json');
        
        return {
            success: true,
            message: 'Backup created successfully'
        };
    }
    
    async restoreFromBackup(file) {
        try {
            const content = await this.readFileContent(file);
            const backupData = JSON.parse(content);
            
            // Validate backup data
            if (!backupData.filter || !backupData.rules) {
                throw new Error('Invalid backup file format');
            }
            
            // Restore data
            this.filterEditor.currentFilter = backupData.filter;
            this.filterEditor.rules = backupData.rules;
            this.filterEditor.updateRulesList();
            this.filterEditor.refreshPreview();
            
            return {
                success: true,
                message: 'Backup restored successfully',
                timestamp: backupData.timestamp
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to restore backup: ${error.message}`,
                error: error
            };
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ImportExportManager;
}
