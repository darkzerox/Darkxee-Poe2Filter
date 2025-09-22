// DZX Filter Editor - Browser Filter Parser

class BrowserFilterParser {
    constructor() {
        this.conditionsPattern = /(\w+)\s+(.+?)(?=\s+\w+\s+|$)/g;
        this.actionsPattern = /(\w+(?:\w+\s+)*?)\s+([^\n]+)/g;
        this.colorPattern = /(\d+)\s+(\d+)\s+(\d+)(?:\s+(\d+))?/;
    }
    
    parseFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const content = e.target.result;
                    const parsedData = this.parseContent(content);
                    resolve(parsedData);
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = () => {
                reject(new Error('Failed to read file'));
            };
            
            reader.readAsText(file, 'utf-8');
        });
    }
    
    parseContent(content) {
        const lines = content.split('\n');
        const rules = [];
        let currentRule = null;
        let currentComment = null;
        
        for (let lineNum = 0; lineNum < lines.length; lineNum++) {
            const line = lines[lineNum].trim();
            
            // Skip empty lines
            if (!line) continue;
            
            // Handle comments
            if (line.startsWith('#')) {
                currentComment = line.substring(1).trim();
                continue;
            }
            
            // Handle Show/Hide statements
            if (line.startsWith('Show') || line.startsWith('Hide')) {
                if (currentRule) {
                    rules.push(currentRule);
                }
                
                const showHide = line.split()[0];
                currentRule = {
                    id: `rule_${rules.length + 1}`,
                    show_hide: showHide,
                    conditions: [],
                    actions: [],
                    comment: currentComment,
                    enabled: true
                };
                currentComment = null;
                continue;
            }
            
            // Handle conditions and actions
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
        
        // Add the last rule
        if (currentRule) {
            rules.push(currentRule);
        }
        
        return {
            rules: rules,
            metadata: {
                total_rules: rules.length,
                parsed_at: new Date().toISOString()
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
            
            // Handle different operators
            if (parts.length >= 3) {
                if (['>=', '<=', '>', '<', '==', '!='].includes(parts[1])) {
                    operator = parts[1];
                    values = [parts[2]];
                } else {
                    // Multiple values without operator
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
            console.error(`Error parsing condition '${line}':`, error);
            return null;
        }
    }
    
    parseAction(line) {
        try {
            const parts = line.split();
            if (parts.length < 2) return null;
            
            const actionType = parts[0];
            let values = [];
            
            // Handle different action types
            if (actionType.includes('Color')) {
                // Parse RGB color values
                const colorMatch = this.colorPattern.exec(line);
                if (colorMatch) {
                    const r = parseInt(colorMatch[1]);
                    const g = parseInt(colorMatch[2]);
                    const b = parseInt(colorMatch[3]);
                    values = [r, g, b];
                    if (colorMatch[4]) {
                        values.push(parseInt(colorMatch[4]));
                    }
                } else {
                    values = parts.slice(1);
                }
            } else if (actionType === 'SetFontSize') {
                values = [parseInt(parts[1])];
            } else if (actionType === 'CustomAlertSound') {
                // Extract sound file and volume
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
            console.error(`Error parsing action '${line}':`, error);
            return null;
        }
    }
    
    validateSyntax(content) {
        const errors = [];
        const warnings = [];
        
        const lines = content.split('\n');
        for (let lineNum = 0; lineNum < lines.length; lineNum++) {
            const line = lines[lineNum].trim();
            
            // Skip empty lines and comments
            if (!line || line.startsWith('#')) continue;
            
            // Check for valid Show/Hide statements
            if (line.startsWith('Show') || line.startsWith('Hide')) {
                if (!this.isValidShowHide(line)) {
                    errors.push(`Line ${lineNum + 1}: Invalid Show/Hide statement`);
                }
            }
            
            // Check for valid conditions
            else if (this.isCondition(line)) {
                if (!this.isValidCondition(line)) {
                    errors.push(`Line ${lineNum + 1}: Invalid condition syntax`);
                }
            }
            
            // Check for valid actions
            else if (this.isAction(line)) {
                if (!this.isValidAction(line)) {
                    warnings.push(`Line ${lineNum + 1}: Potentially invalid action syntax`);
                }
            }
        }
        
        return {
            valid: errors.length === 0,
            errors: errors,
            warnings: warnings
        };
    }
    
    isValidShowHide(line) {
        return line === 'Show' || line === 'Hide' || 
               line.startsWith('Show ') || line.startsWith('Hide ');
    }
    
    isValidCondition(line) {
        const parts = line.split();
        return parts.length >= 2;
    }
    
    isValidAction(line) {
        const parts = line.split();
        return parts.length >= 1;
    }
    
    exportFile(data, filename) {
        const content = this.generateFilterContent(data);
        const blob = new Blob([content], { type: 'text/plain' });
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
    
    generateFilterContent(data) {
        let content = `# ${data.name || 'DZX Filter'}\n`;
        content += `# Generated by DZX Filter Editor\n`;
        content += `# Platform: ${data.platform || 'pc'}\n`;
        content += `# Sound Type: ${data.soundType || 'type-01'}\n\n`;
        
        const rules = data.rules || [];
        rules.forEach(rule => {
            // Add comment if exists
            if (rule.comment) {
                content += `# ${rule.comment}\n`;
            }
            
            // Add Show/Hide statement
            content += `${rule.show_hide}\n`;
            
            // Add conditions
            rule.conditions.forEach(condition => {
                const conditionLine = this.generateConditionLine(condition);
                if (conditionLine) {
                    content += `  ${conditionLine}\n`;
                }
            });
            
            // Add actions
            rule.actions.forEach(action => {
                const actionLine = this.generateActionLine(action);
                if (actionLine) {
                    content += `  ${actionLine}\n`;
                }
            });
            
            content += '\n'; // Empty line between rules
        });
        
        return content;
    }
    
    generateConditionLine(condition) {
        const conditionType = condition.type;
        const operator = condition.operator;
        const values = condition.values;
        
        if (operator === '==' && values.length === 1) {
            return `${conditionType} ${values[0]}`;
        } else if (operator === '==' && values.length > 1) {
            return `${conditionType} ${values.join(' ')}`;
        } else {
            return `${conditionType} ${operator} ${values.join(' ')}`;
        }
    }
    
    generateActionLine(action) {
        const actionType = action.type;
        const values = action.values;
        
        if (actionType.includes('Color')) {
            if (values.length >= 3) {
                let colorStr = values.slice(0, 3).join(' ');
                if (values.length > 3) {
                    colorStr += ` ${values[3]}`;
                }
                return `${actionType} ${colorStr}`;
            }
        } else if (actionType === 'CustomAlertSound') {
            if (values.length >= 2) {
                return `${actionType} "${values[0]}" ${values[1]}`;
            }
        }
        
        return `${actionType} ${values.join(' ')}`;
    }
    
    mergeFilters(filterDataList) {
        const mergedRules = [];
        let totalRules = 0;
        
        filterDataList.forEach(filterData => {
            const rules = filterData.rules || [];
            mergedRules.push(...rules);
            totalRules += rules.length;
        });
        
        return {
            rules: mergedRules,
            metadata: {
                total_rules: totalRules,
                merged_from: filterDataList.length,
                merged_at: new Date().toISOString()
            }
        };
    }
    
    // Utility methods
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
    
    // Advanced parsing methods
    parseAdvancedCondition(line) {
        // Handle complex conditions like "ItemLevel >= 80 && AreaLevel < 90"
        const operators = ['&&', '||', '>=', '<=', '>', '<', '==', '!='];
        const parts = line.split(/\s+/);
        
        const conditions = [];
        let currentCondition = null;
        
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            
            if (operators.includes(part)) {
                if (currentCondition) {
                    currentCondition.operator = part;
                }
            } else if (currentCondition && currentCondition.operator) {
                currentCondition.values.push(part);
            } else {
                if (currentCondition) {
                    conditions.push(currentCondition);
                }
                currentCondition = {
                    type: part,
                    operator: '==',
                    values: []
                };
            }
        }
        
        if (currentCondition) {
            conditions.push(currentCondition);
        }
        
        return conditions;
    }
    
    // Validation helpers
    validateRule(rule) {
        const errors = [];
        
        if (!rule.id) {
            errors.push('Rule missing ID');
        }
        
        if (!rule.show_hide || !['Show', 'Hide'].includes(rule.show_hide)) {
            errors.push('Invalid show/hide value');
        }
        
        if (!rule.conditions || !Array.isArray(rule.conditions)) {
            errors.push('Missing or invalid conditions');
        }
        
        if (!rule.actions || !Array.isArray(rule.actions)) {
            errors.push('Missing or invalid actions');
        }
        
        // Validate conditions
        rule.conditions.forEach((condition, index) => {
            if (!condition.type) {
                errors.push(`Condition ${index + 1}: missing type`);
            }
            if (!condition.operator) {
                errors.push(`Condition ${index + 1}: missing operator`);
            }
            if (!condition.values || !Array.isArray(condition.values)) {
                errors.push(`Condition ${index + 1}: missing or invalid values`);
            }
        });
        
        // Validate actions
        rule.actions.forEach((action, index) => {
            if (!action.type) {
                errors.push(`Action ${index + 1}: missing type`);
            }
            if (!action.values || !Array.isArray(action.values)) {
                errors.push(`Action ${index + 1}: missing or invalid values`);
            }
        });
        
        return {
            valid: errors.length === 0,
            errors: errors
        };
    }
    
    // Performance optimization
    optimizeRules(rules) {
        // Remove duplicate rules
        const uniqueRules = [];
        const seenRules = new Set();
        
        rules.forEach(rule => {
            const ruleKey = this.generateRuleKey(rule);
            if (!seenRules.has(ruleKey)) {
                seenRules.add(ruleKey);
                uniqueRules.push(rule);
            }
        });
        
        // Sort rules by priority (simplified)
        return uniqueRules.sort((a, b) => {
            // Rules with more conditions have higher priority
            return b.conditions.length - a.conditions.length;
        });
    }
    
    generateRuleKey(rule) {
        const conditionsKey = rule.conditions
            .map(c => `${c.type}${c.operator}${c.values.join(',')}`)
            .join('|');
        const actionsKey = rule.actions
            .map(a => `${a.type}${a.values.join(',')}`)
            .join('|');
        return `${rule.show_hide}|${conditionsKey}|${actionsKey}`;
    }
}

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.BrowserFilterParser = BrowserFilterParser;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = BrowserFilterParser;
}
