#!/usr/bin/env python3
"""
Houston Intelligence Platform API
Provides RESTful API endpoints for accessing the Houston Development Intelligence system
"""

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import json
from pathlib import Path
import datetime
from typing import Dict, List, Optional, Any
import logging
from functools import wraps
import time
import os

# Import our master intelligence agent
from master_intelligence_agent import MasterIntelligenceAgent
try:
    from master_intelligence_agent_replicate import ReplicateEnhancedMasterAgent
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False
from houston_data_enhanced import HoustonDataAPI
from houston_intelligence_endpoints import houston_endpoints, init_endpoints

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['*'])

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Master Intelligence Agent
USE_REPLICATE = os.getenv('USE_REPLICATE', 'true').lower() == 'true'
if USE_REPLICATE and REPLICATE_AVAILABLE:
    try:
        intelligence_agent = ReplicateEnhancedMasterAgent()
        logger.info("🚀 Using Replicate-Enhanced Master Intelligence Agent")
    except Exception as e:
        logger.warning(f"Failed to initialize Replicate: {e}. Using standard agent.")
        intelligence_agent = MasterIntelligenceAgent()
else:
    intelligence_agent = MasterIntelligenceAgent()
    logger.info("Using Master Intelligence Agent")

# API version
API_VERSION = "v1"

# Register specialized endpoints blueprint
app.register_blueprint(houston_endpoints)
init_endpoints(cache)

def log_request(f):
    """Decorator to log API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
        
        response = f(*args, **kwargs)
        
        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} in {duration:.2f}s")
        
        return response
    return decorated_function

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'name': 'Houston Intelligence Platform API',
        'version': API_VERSION,
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'query': f'/api/{API_VERSION}/query',
            'agents': f'/api/{API_VERSION}/agents',
            'stats': f'/api/{API_VERSION}/stats',
            'insights': f'/api/{API_VERSION}/insights/latest',
            'search': f'/api/{API_VERSION}/search'
        },
        'documentation': 'https://github.com/Fernando-Houston/Core-Agent-Architecture'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': API_VERSION
    })

@app.route(f'/api/{API_VERSION}/query', methods=['POST'])
@limiter.limit("10 per minute")
@log_request
def query_intelligence():
    """
    Main query endpoint for Houston Intelligence Platform
    Accepts natural language queries and returns structured intelligence
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query parameter',
                'status': 'error'
            }), 400
        
        query = data['query']
        context = data.get('context', {})
        
        # Process query through Master Intelligence Agent
        response = intelligence_agent.analyze_query(query)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'response': {
                'answer': response.get('executive_summary', 'No summary available'),
                'insights': response.get('key_insights', []),
                'data': response.get('data_highlights', []),
                'sources': response.get('sources', []),
                'full_analysis': response
            },
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route(f'/api/{API_VERSION}/agents', methods=['GET'])
@cache.cached(timeout=3600)  # Cache for 1 hour
@log_request
def list_agents():
    """List all available intelligence agents and their capabilities"""
    agents = []
    
    for agent_name, agent_path in intelligence_agent.agent_registry.items():
        capabilities_file = agent_path / 'capabilities.json'
        capabilities = {}
        
        if capabilities_file.exists():
            with open(capabilities_file, 'r') as f:
                capabilities = json.load(f)
        
        agents.append({
            'name': agent_name,
            'description': capabilities.get('description', ''),
            'data_sources': capabilities.get('data_sources', []),
            'query_types': capabilities.get('query_types', [])
        })
    
    return jsonify({
        'status': 'success',
        'agents': agents,
        'total': len(agents)
    })

@app.route(f'/api/{API_VERSION}/agent/<agent_name>', methods=['GET'])
@cache.cached(timeout=600)  # Cache for 10 minutes
@log_request
def get_agent_details(agent_name):
    """Get detailed information about a specific agent"""
    if agent_name not in intelligence_agent.agent_registry:
        return jsonify({
            'error': f'Agent {agent_name} not found',
            'status': 'error'
        }), 404
    
    agent_path = intelligence_agent.agent_registry[agent_name]
    
    # Get capabilities
    capabilities_file = agent_path / 'capabilities.json'
    capabilities = {}
    if capabilities_file.exists():
        with open(capabilities_file, 'r') as f:
            capabilities = json.load(f)
    
    # Get knowledge base info
    knowledge_files = list(agent_path.glob('knowledge_*.json'))
    knowledge_summary = {
        'total_files': len(knowledge_files),
        'last_updated': None
    }
    
    if knowledge_files:
        latest_file = max(knowledge_files, key=lambda p: p.stat().st_mtime)
        knowledge_summary['last_updated'] = datetime.datetime.fromtimestamp(
            latest_file.stat().st_mtime
        ).isoformat()
    
    return jsonify({
        'status': 'success',
        'agent': {
            'name': agent_name,
            'capabilities': capabilities,
            'knowledge_summary': knowledge_summary
        }
    })

@app.route(f'/api/{API_VERSION}/insights/latest', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
@log_request
def get_latest_insights():
    """Get the latest insights across all agents"""
    insights = []
    
    # Look for recent insights in each agent folder
    for agent_name, agent_path in intelligence_agent.agent_registry.items():
        insights_file = agent_path / 'latest_insights.json'
        
        if insights_file.exists():
            with open(insights_file, 'r') as f:
                agent_insights = json.load(f)
                
                for insight in agent_insights.get('insights', []):
                    insights.append({
                        'agent': agent_name,
                        'type': insight.get('type'),
                        'title': insight.get('title'),
                        'summary': insight.get('summary'),
                        'timestamp': insight.get('timestamp'),
                        'confidence': insight.get('confidence', 0.8)
                    })
    
    # Sort by timestamp (most recent first)
    insights.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        'status': 'success',
        'insights': insights[:20],  # Return top 20 most recent
        'total': len(insights)
    })

@app.route(f'/api/{API_VERSION}/search', methods=['POST'])
@limiter.limit("20 per minute")
@log_request
def search_intelligence():
    """Search across all intelligence data"""
    try:
        data = request.get_json()
        
        if not data or 'keywords' not in data:
            return jsonify({
                'error': 'Missing keywords parameter',
                'status': 'error'
            }), 400
        
        keywords = data['keywords']
        filters = data.get('filters', {})
        
        # Perform search across agents
        results = []
        
        for agent_name, agent_path in intelligence_agent.agent_registry.items():
            # Skip if agent filter is applied and doesn't match
            if filters.get('agents') and agent_name not in filters['agents']:
                continue
            
            # Search in knowledge files
            for knowledge_file in agent_path.glob('knowledge_*.json'):
                with open(knowledge_file, 'r') as f:
                    content = f.read().lower()
                    
                    # Simple keyword matching (can be enhanced)
                    if any(keyword.lower() in content for keyword in keywords):
                        with open(knowledge_file, 'r') as f:
                            knowledge_data = json.load(f)
                            
                        results.append({
                            'agent': agent_name,
                            'file': knowledge_file.name,
                            'type': knowledge_data.get('type', 'unknown'),
                            'preview': knowledge_data.get('summary', '')[:200] + '...',
                            'timestamp': datetime.datetime.fromtimestamp(
                                knowledge_file.stat().st_mtime
                            ).isoformat()
                        })
        
        return jsonify({
            'status': 'success',
            'keywords': keywords,
            'results': results[:50],  # Limit to 50 results
            'total': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route(f'/api/{API_VERSION}/debug/knowledge-base', methods=['GET'])
def debug_knowledge_base():
    """Debug endpoint to check knowledge base status"""
    kb_path = Path("Agent_Knowledge_Bases")
    debug_info = {
        "agent_knowledge_bases_exists": kb_path.exists(),
        "current_working_directory": os.getcwd(),
        "files_in_cwd": os.listdir("."),
        "knowledge_base_structure": {}
    }
    
    if kb_path.exists():
        for folder in kb_path.iterdir():
            if folder.is_dir():
                json_files = list(folder.glob("*.json"))
                debug_info["knowledge_base_structure"][folder.name] = {
                    "file_count": len(json_files),
                    "files": [f.name for f in json_files][:5]  # Show first 5 files
                }
    
    # Also check 6 Specialized Agents path
    agents_path = Path("6 Specialized Agents")
    debug_info["six_specialized_agents_exists"] = agents_path.exists()
    
    return jsonify(debug_info)

@app.route(f'/api/{API_VERSION}/stats', methods=['GET'])
@cache.cached(timeout=600)  # Cache for 10 minutes
@log_request
def get_platform_stats():
    """Get platform statistics and metrics"""
    stats = {
        'total_agents': len(intelligence_agent.agent_registry),
        'data_sources': 0,
        'knowledge_files': 0,
        'last_refresh': None,
        'coverage': {
            'permits': 0,
            'developments': 0,
            'neighborhoods': 0,
            'regulations': 0
        }
    }
    
    # Count knowledge files and get last update
    latest_update = None
    
    # Look in Agent_Knowledge_Bases instead of agent registry paths
    kb_base_path = Path("Agent_Knowledge_Bases")
    if kb_base_path.exists():
        folder_mapping = {
            "market_intelligence": "Market_Intelligence",
            "neighborhood_intelligence": "Neighborhood_Intelligence",
            "financial_intelligence": "Financial_Intelligence",
            "environmental_intelligence": "Environmental_Intelligence",
            "regulatory_intelligence": "Regulatory_Intelligence",
            "technology_intelligence": "Technology_Innovation_Intelligence"
        }
        
        for agent_name in intelligence_agent.agent_registry.keys():
            kb_folder = kb_base_path / folder_mapping.get(agent_name, agent_name)
            if kb_folder.exists():
                knowledge_files = list(kb_folder.glob('*.json'))
                stats['knowledge_files'] += len(knowledge_files)
                
                if knowledge_files:
                    latest_file = max(knowledge_files, key=lambda p: p.stat().st_mtime)
                    file_time = datetime.datetime.fromtimestamp(latest_file.stat().st_mtime)
                    
                    if not latest_update or file_time > latest_update:
                        latest_update = file_time
    
    if latest_update:
        stats['last_refresh'] = latest_update.isoformat()
    
    # Count data sources
    data_processing_path = Path('Data Processing')
    if data_processing_path.exists():
        stats['data_sources'] = len([p for p in data_processing_path.iterdir() if p.is_dir()])
    
    return jsonify({
        'status': 'success',
        'stats': stats,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({
        'error': 'Rate limit exceeded',
        'status': 'error',
        'message': str(error.description)
    }), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Turn off debug for production
    )