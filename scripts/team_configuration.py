# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:51:23 2024

@author: Aidan Jacobsen
"""

import yaml #pip install PyYAML
import os
import glob
import re
import argparse
import sys

def modify_yaml_file(yaml_file_path):
    # Read the entire content of the YAML file into a single string
    with open(yaml_file_path, 'r') as file:
        content = file.read()

    # Load the YAML data to check the 'la_enabled' flag
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Define the base lines related to the logic analyzer
    la_lines = [
        r"(\s*- name: la_data_in[\s\S]*?description: Inputs from the Logic Analyzer)",
        r"(\s*- name: la_data_out[\s\S]*?description: Outputs from the Logic Analyzer)",
        r"(\s*- name: la_oenb[\s\S]*?description: Output Enable from the Logic Analyzer)"
    ]
    
    wb_master_lines = [
        r"(\s*- name: DAT_I[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: ACK_I[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: ADR_O[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: DAT_O[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: SEL_O[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: WE_O[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: STB_O[\s\S]*?description: Wishbone Master Signals)",
        r"(\s*- name: CYC_O[\s\S]*?description: Wishbone Master Signals)"
    ]

    # This function handles commenting and uncommenting lines based on the enable flag
    def process_lines(toggle_lines, content, enable):
        
        def comment_block(match):
            return '# ' + match.group(1).replace('\n', '\n#')
        
        def uncomment_block(match):
            return "  " +   match.group(1).replace('#', '')
        
        for line in toggle_lines:
            if enable:
                # Uncomment: Remove leading #
                content = re.sub(r"^#\s*(%s)" % line, uncomment_block, content, flags=re.MULTILINE)
            else:
                # Comment: Add leading #
                content = re.sub(r"^(%s)" % line, comment_block, content, flags=re.MULTILINE)
        return content

    # Check the la_enabled value and comment/uncomment the corresponding lines
    if data.get('project_info', {}).get('la_enabled', False):
        print("LA Enabled")
        updated_content = process_lines(la_lines, content, enable=True)
    else:
        print("LA Disabled")
        updated_content = process_lines(la_lines, content, enable=False)
        
    # Check the wb_master_enabled value and comment/ uncomment the corresponding lines
    if data.get('project_info', {}).get('wb_master_enabled', False):
        print("WB Master Enabled")
        updated_content = process_lines(wb_master_lines, updated_content, enable=True)
    else:
        print("WB Master Disabled")
        updated_content = process_lines(wb_master_lines, updated_content, enable=False)

    # Write the updated content back to the YAML file
    with open(yaml_file_path, 'w') as file:
        file.write(updated_content)
        
def modify_wrapper_file(wrapper_file_path, yaml_file_path):
    # Read the entire content of the Wrapper file into a single string
    with open(wrapper_file_path, 'r') as file:
        content = file.read()

    # Load the YAML data to check the flags
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # lines included when LA enabled
    la_pos_lines = [
        r"(\s*\.la_data_in\(la_data_in\),)",
        r"(\s*\.la_data_out\(la_data_out\),)",
        r"(\s*\.la_oenb\(la_oenb\),)"
    ]
    # Lines included when LA disabled
    la_neg_lines = [
        r"(\s*assign la_data_out = 32'b0;)"
    ]
    
    # Lines included when WB Master enabled
    wb_master_pos_lines = [
        r"(\s*\.ADR_O\(ADR_O\),)",
        r"(\s*\.DAT_O\(DAT_O\),)",
        r"(\s*\.SEL_O\(SEL_O\),)",
        r"(\s*\.WE_O\(WE_O\),)",
        r"(\s*\.STB_O\(STB_O\),)",
        r"(\s*\.CYC_O\(CYC_O\),)",
        r"(\s*\.ACK_I\(ACK_I\),)",
        r"(\s*\.DAT_I\(DAT_I\),)"
    ]

    # Lines included when WB Master disabled
    wb_master_neg_lines = [
        r"(\s*assign ADR_O = 32'b0;)",
        r"(\s*assign DAT_O = 32'b0;)",
        r"(\s*assign SEL_O = 4'b0;)",
        r"(\s*assign  WE_O = 1'b0;)",
        r"(\s*assign STB_O = 1'b0;)",
        r"(\s*assign CYC_O = 1'b0;)"
    ]

    # This function handles commenting and uncommenting lines based on the enable flag
    def process_lines(toggle_lines, content, enable):
        
        def comment_block(match):
            return '// ' + match.group(1).replace('\n', '\n//')
        
        def uncomment_block(match):
            return "    " +   match.group(1).replace('//', '')
        
        for line in toggle_lines:
            if enable:
                # Uncomment: Remove leading #
                content = re.sub(r"^//\s*(%s)" % line, uncomment_block, content, flags=re.MULTILINE)
            else:
                # Comment: Add leading #
                content = re.sub(r"^(%s)" % line, comment_block, content, flags=re.MULTILINE)
        return content

    # Check the la_enabled value and comment/uncomment the corresponding lines
    if data.get('project_info', {}).get('la_enabled', False):
        updated_content = process_lines(la_pos_lines, content, enable=True)
        updated_content = process_lines(la_neg_lines, updated_content, enable=False)
    else:
        updated_content = process_lines(la_pos_lines, content, enable=False)
        updated_content = process_lines(la_neg_lines, updated_content, enable=True)
        
    # Check the wb_master_enabled value and comment/ uncomment the corresponding lines
    if data.get('project_info', {}).get('wb_master_enabled', False):
        updated_content = process_lines(wb_master_pos_lines, updated_content, enable=True)
        updated_content = process_lines(wb_master_neg_lines, updated_content, enable=False)
    else:
        updated_content = process_lines(wb_master_pos_lines, updated_content, enable=False)
        updated_content = process_lines(wb_master_neg_lines, updated_content, enable=True)

    # Write the updated content back to the YAML file
    with open(wrapper_file_path, 'w') as file:
        file.write(updated_content)

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process filename and wrapper file arguments.")
    
    # Define the yaml file argument
    parser.add_argument('--yaml', type=str, help='Path to the YAML file', required=True)

    # Define the wrapper file argument
    parser.add_argument('--wrapper', type=str, help='Path to the wrapper file', required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    yaml_filename = args.yaml
    wrapper_filename = args.wrapper
    
    # Print the filenames
    print(f"Processing YAML file: {yaml_filename}")
    print(f"Processing wrapper file: {wrapper_filename}")
    
    modify_wrapper_file(wrapper_filename, yaml_filename)
    modify_yaml_file(yaml_filename)
    
if __name__ == "__main__":
    main()