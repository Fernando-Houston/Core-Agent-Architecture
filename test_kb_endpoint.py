#!/usr/bin/env python3
"""
Add a test endpoint to the API to check knowledge base status
This should be added to houston_intelligence_api.py
"""

# Add this route to houston_intelligence_api.py

"""
@app.route(f'/api/{API_VERSION}/debug/knowledge-base', methods=['GET'])
def debug_knowledge_base():
    '''Debug endpoint to check knowledge base status'''
    from pathlib import Path
    
    debug_info = {
        'knowledge_base_path': str(Path('Agent_Knowledge_Bases').absolute()),
        'knowledge_base_exists': Path('Agent_Knowledge_Bases').exists(),
        'agents_found': {},
        'total_files': 0,
        'sample_files': []
    }
    
    kb_path = Path('Agent_Knowledge_Bases')
    if kb_path.exists():
        for agent_folder in kb_path.iterdir():
            if agent_folder.is_dir():
                json_files = list(agent_folder.glob('*.json'))
                debug_info['agents_found'][agent_folder.name] = len(json_files)
                debug_info['total_files'] += len(json_files)
                
                # Add sample file names
                if json_files and len(debug_info['sample_files']) < 5:
                    debug_info['sample_files'].extend([f.name for f in json_files[:2]])
    
    # Also check the agent registry paths
    debug_info['agent_registry_paths'] = {}
    for agent_id, agent_path in intelligence_agent.agent_registry.items():
        debug_info['agent_registry_paths'][agent_id] = {
            'path': str(agent_path),
            'exists': agent_path.exists()
        }
    
    return jsonify(debug_info)
"""

print("Add the above endpoint to houston_intelligence_api.py to debug the knowledge base on Railway")