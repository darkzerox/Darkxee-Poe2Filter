# DZX Filter POE2 - Filter Parser

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class FilterCondition:
    """Represents a condition in a filter rule"""
    type: str  # Class, BaseType, Rarity, AreaLevel, ItemLevel, etc.
    operator: str  # ==, !=, >=, <=, >, <
    values: List[str]  # List of values to match

@dataclass
class FilterAction:
    """Represents an action in a filter rule"""
    type: str  # SetTextColor, SetBorderColor, PlayEffect, etc.
    values: List[Any]  # Values for the action

@dataclass
class FilterRule:
    """Represents a complete filter rule"""
    id: str
    show_hide: str  # "Show" or "Hide"
    conditions: List[FilterCondition]
    actions: List[FilterAction]
    comment: Optional[str] = None
    enabled: bool = True

@dataclass
class FilterCategory:
    """Represents a category of filter rules"""
    name: str
    rules: List[FilterRule]
    description: Optional[str] = None

class FilterParser:
    """Parser for Path of Exile 2 filter files"""
    
    def __init__(self):
        self.conditions_pattern = re.compile(r'(\w+)\s+(.+?)(?=\s+\w+\s+|$)')
        self.actions_pattern = re.compile(r'(\w+(?:\w+\s+)*?)\s+([^\n]+)')
        self.color_pattern = re.compile(r'(\d+)\s+(\d+)\s+(\d+)(?:\s+(\d+))?')
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a filter file and return structured data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse_content(content)
        except Exception as e:
            raise Exception(f"Error parsing file {file_path}: {str(e)}")
    
    def parse_content(self, content: str) -> Dict[str, Any]:
        """Parse filter content and return structured data"""
        lines = content.split('\n')
        rules = []
        current_rule = None
        current_comment = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Handle comments
            if line.startswith('#'):
                current_comment = line[1:].strip()
                continue
            
            # Handle Show/Hide statements
            if line.startswith('Show') or line.startswith('Hide'):
                if current_rule:
                    rules.append(current_rule)
                
                show_hide = line.split()[0]
                current_rule = FilterRule(
                    id=f"rule_{len(rules) + 1}",
                    show_hide=show_hide,
                    conditions=[],
                    actions=[],
                    comment=current_comment
                )
                current_comment = None
                continue
            
            # Handle conditions and actions
            if current_rule:
                if self._is_condition(line):
                    condition = self._parse_condition(line)
                    if condition:
                        current_rule.conditions.append(condition)
                elif self._is_action(line):
                    action = self._parse_action(line)
                    if action:
                        current_rule.actions.append(action)
        
        # Add the last rule
        if current_rule:
            rules.append(current_rule)
        
        return {
            "rules": [asdict(rule) for rule in rules],
            "metadata": {
                "total_rules": len(rules),
                "parsed_at": str(Path().cwd())
            }
        }
    
    def _is_condition(self, line: str) -> bool:
        """Check if a line is a condition"""
        condition_keywords = [
            'Class', 'BaseType', 'Rarity', 'AreaLevel', 'ItemLevel',
            'Sockets', 'Quality', 'Width', 'Height', 'DropLevel'
        ]
        first_word = line.split()[0] if line.split() else ''
        return first_word in condition_keywords
    
    def _is_action(self, line: str) -> bool:
        """Check if a line is an action"""
        action_keywords = [
            'SetTextColor', 'SetBorderColor', 'SetBackgroundColor',
            'SetFontSize', 'PlayEffect', 'MinimapIcon', 'CustomAlertSound',
            'PlayAlertSound', 'DisableDropSound', 'Continue'
        ]
        first_word = line.split()[0] if line.split() else ''
        return first_word in action_keywords
    
    def _parse_condition(self, line: str) -> Optional[FilterCondition]:
        """Parse a condition line"""
        try:
            parts = line.split()
            if len(parts) < 2:
                return None
            
            condition_type = parts[0]
            values = []
            operator = "=="
            
            # Handle different operators
            if len(parts) >= 3:
                if parts[1] in ['>=', '<=', '>', '<', '==', '!=']:
                    operator = parts[1]
                    values = [parts[2]]
                else:
                    # Multiple values without operator
                    values = parts[1:]
            else:
                values = [parts[1]]
            
            return FilterCondition(
                type=condition_type,
                operator=operator,
                values=values
            )
        except Exception as e:
            print(f"Error parsing condition '{line}': {e}")
            return None
    
    def _parse_action(self, line: str) -> Optional[FilterAction]:
        """Parse an action line"""
        try:
            parts = line.split()
            if len(parts) < 2:
                return None
            
            action_type = parts[0]
            values = []
            
            # Handle different action types
            if action_type in ['SetTextColor', 'SetBorderColor', 'SetBackgroundColor']:
                # Parse RGB color values
                color_match = self.color_pattern.search(line)
                if color_match:
                    r, g, b = color_match.groups()[:3]
                    alpha = color_match.group(4) if color_match.group(4) else None
                    values = [int(r), int(g), int(b)]
                    if alpha:
                        values.append(int(alpha))
                else:
                    values = parts[1:]
            
            elif action_type == 'SetFontSize':
                values = [int(parts[1])]
            
            elif action_type in ['PlayEffect', 'MinimapIcon']:
                values = parts[1:]
            
            elif action_type == 'CustomAlertSound':
                # Extract sound file and volume
                sound_file = parts[1].strip('"')
                volume = int(parts[2]) if len(parts) > 2 else 100
                values = [sound_file, volume]
            
            else:
                values = parts[1:]
            
            return FilterAction(
                type=action_type,
                values=values
            )
        except Exception as e:
            print(f"Error parsing action '{line}': {e}")
            return None
    
    def validate_syntax(self, content: str) -> Dict[str, Any]:
        """Validate filter syntax and return validation results"""
        errors = []
        warnings = []
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Check for valid Show/Hide statements
            if line.startswith('Show') or line.startswith('Hide'):
                if not self._is_valid_show_hide(line):
                    errors.append(f"Line {line_num}: Invalid Show/Hide statement")
            
            # Check for valid conditions
            elif self._is_condition(line):
                if not self._is_valid_condition(line):
                    errors.append(f"Line {line_num}: Invalid condition syntax")
            
            # Check for valid actions
            elif self._is_action(line):
                if not self._is_valid_action(line):
                    warnings.append(f"Line {line_num}: Potentially invalid action syntax")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _is_valid_show_hide(self, line: str) -> bool:
        """Check if Show/Hide statement is valid"""
        return line in ['Show', 'Hide'] or line.startswith('Show ') or line.startswith('Hide ')
    
    def _is_valid_condition(self, line: str) -> bool:
        """Check if condition syntax is valid"""
        parts = line.split()
        return len(parts) >= 2
    
    def _is_valid_action(self, line: str) -> bool:
        """Check if action syntax is valid"""
        parts = line.split()
        return len(parts) >= 1
    
    def export_file(self, data: Dict[str, Any], file_path: str) -> None:
        """Export structured data to filter file"""
        try:
            content = self._generate_filter_content(data)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Error exporting file {file_path}: {str(e)}")
    
    def _generate_filter_content(self, data: Dict[str, Any]) -> str:
        """Generate filter file content from structured data"""
        lines = []
        
        # Add header comment
        lines.append("# DZX Filter for Path of Exile 2")
        lines.append("# Generated by DZX Filter Web Interface")
        lines.append("")
        
        rules = data.get('rules', [])
        for rule_data in rules:
            # Add comment if exists
            if rule_data.get('comment'):
                lines.append(f"# {rule_data['comment']}")
            
            # Add Show/Hide statement
            lines.append(rule_data['show_hide'])
            
            # Add conditions
            for condition in rule_data.get('conditions', []):
                condition_line = self._generate_condition_line(condition)
                if condition_line:
                    lines.append(f"  {condition_line}")
            
            # Add actions
            for action in rule_data.get('actions', []):
                action_line = self._generate_action_line(action)
                if action_line:
                    lines.append(f"  {action_line}")
            
            lines.append("")  # Empty line between rules
        
        return '\n'.join(lines)
    
    def _generate_condition_line(self, condition: Dict[str, Any]) -> str:
        """Generate condition line from condition data"""
        condition_type = condition['type']
        operator = condition['operator']
        values = condition['values']
        
        if operator == "==" and len(values) == 1:
            return f"{condition_type} {values[0]}"
        elif operator == "==" and len(values) > 1:
            return f"{condition_type} {' '.join(values)}"
        else:
            return f"{condition_type} {operator} {' '.join(values)}"
    
    def _generate_action_line(self, action: Dict[str, Any]) -> str:
        """Generate action line from action data"""
        action_type = action['type']
        values = action['values']
        
        if action_type in ['SetTextColor', 'SetBorderColor', 'SetBackgroundColor']:
            if len(values) >= 3:
                color_str = ' '.join(map(str, values[:3]))
                if len(values) > 3:
                    color_str += f" {values[3]}"
                return f"{action_type} {color_str}"
        
        elif action_type == 'CustomAlertSound':
            if len(values) >= 2:
                return f'{action_type} "{values[0]}" {values[1]}'
        
        else:
            return f"{action_type} {' '.join(map(str, values))}"
    
    def merge_filters(self, filter_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple filter data into one"""
        merged_rules = []
        total_rules = 0
        
        for filter_data in filter_data_list:
            rules = filter_data.get('rules', [])
            merged_rules.extend(rules)
            total_rules += len(rules)
        
        return {
            "rules": merged_rules,
            "metadata": {
                "total_rules": total_rules,
                "merged_from": len(filter_data_list),
                "merged_at": str(Path().cwd())
            }
        }

# Example usage
if __name__ == "__main__":
    parser = FilterParser()
    
    # Test parsing
    try:
        data = parser.parse_file("dzx_filter/filter_group/currency.filter")
        print("Parsed successfully!")
        print(f"Total rules: {data['metadata']['total_rules']}")
        
        # Test validation
        with open("dzx_filter/filter_group/currency.filter", 'r') as f:
            content = f.read()
        
        validation = parser.validate_syntax(content)
        print(f"Validation: {'Valid' if validation['valid'] else 'Invalid'}")
        if validation['errors']:
            print("Errors:", validation['errors'])
        if validation['warnings']:
            print("Warnings:", validation['warnings'])
            
    except Exception as e:
        print(f"Error: {e}")
