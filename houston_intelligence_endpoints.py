#!/usr/bin/env python3
"""
Houston Intelligence Platform - Specialized Endpoints
Provides domain-specific API endpoints for targeted intelligence queries
"""

from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import json
from pathlib import Path
import datetime
from typing import Dict, List, Optional, Any
import logging

# Create blueprint for specialized endpoints
houston_endpoints = Blueprint('houston_endpoints', __name__)

# Configure logging
logger = logging.getLogger(__name__)

# Cache instance (will be set by main app)
cache = None

def init_endpoints(app_cache):
    """Initialize endpoints with app cache"""
    global cache
    cache = app_cache

# Helper function to read agent knowledge
def get_agent_knowledge(agent_name: str, knowledge_type: Optional[str] = None) -> List[Dict]:
    """Read knowledge files from specified agent"""
    agent_path = Path(f'{agent_name}_Intelligence_Agent')
    if not agent_path.exists():
        return []
    
    knowledge_files = list(agent_path.glob('knowledge_*.json'))
    knowledge_data = []
    
    for file in knowledge_files:
        with open(file, 'r') as f:
            data = json.load(f)
            if not knowledge_type or data.get('type') == knowledge_type:
                knowledge_data.append(data)
    
    return knowledge_data

@houston_endpoints.route('/api/v1/developments/active', methods=['GET'])
def get_active_developments():
    """Get all active development projects in Houston"""
    try:
        # Get market intelligence about active developments
        market_data = get_agent_knowledge('Market', 'development_opportunities')
        financial_data = get_agent_knowledge('Financial', 'project_analysis')
        
        developments = []
        
        # Combine data from multiple agents
        for market_item in market_data:
            if 'developments' in market_item:
                for dev in market_item['developments']:
                    development = {
                        'name': dev.get('name'),
                        'type': dev.get('type'),
                        'location': dev.get('location'),
                        'status': dev.get('status', 'active'),
                        'size': dev.get('size'),
                        'estimated_value': dev.get('value'),
                        'developer': dev.get('developer'),
                        'completion_date': dev.get('completion_date')
                    }
                    developments.append(development)
        
        return jsonify({
            'status': 'success',
            'total': len(developments),
            'developments': developments,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting active developments: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/neighborhoods/<neighborhood_name>', methods=['GET'])
def get_neighborhood_analysis(neighborhood_name):
    """Get comprehensive analysis for a specific neighborhood"""
    try:
        # Search for neighborhood data across agents
        neighborhood_data = get_agent_knowledge('Neighborhood')
        market_data = get_agent_knowledge('Market')
        
        analysis = {
            'name': neighborhood_name,
            'demographics': {},
            'market_metrics': {},
            'development_activity': {},
            'investment_potential': {},
            'risks': []
        }
        
        # Find matching neighborhood data
        for item in neighborhood_data:
            if neighborhood_name.lower() in str(item).lower():
                if 'demographics' in item:
                    analysis['demographics'] = item['demographics']
                if 'market_analysis' in item:
                    analysis['market_metrics'] = item['market_analysis']
                if 'development_opportunities' in item:
                    analysis['development_activity'] = item['development_opportunities']
        
        # Add market insights
        for item in market_data:
            if neighborhood_name.lower() in str(item).lower():
                if 'investment_score' in item:
                    analysis['investment_potential'] = {
                        'score': item['investment_score'],
                        'factors': item.get('scoring_factors', [])
                    }
                if 'risks' in item:
                    analysis['risks'].extend(item['risks'])
        
        return jsonify({
            'status': 'success',
            'neighborhood': analysis,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting neighborhood analysis: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/permits/recent', methods=['GET'])
def get_recent_permits():
    """Get recent building permits with filtering options"""
    try:
        # Get query parameters
        permit_type = request.args.get('type', 'all')
        limit = int(request.args.get('limit', 50))
        area = request.args.get('area')
        
        # Get regulatory data
        regulatory_data = get_agent_knowledge('Regulatory', 'permits')
        
        permits = []
        
        for item in regulatory_data:
            if 'permits' in item:
                for permit in item['permits']:
                    # Apply filters
                    if permit_type != 'all' and permit.get('type') != permit_type:
                        continue
                    if area and area.lower() not in permit.get('location', '').lower():
                        continue
                    
                    permits.append({
                        'permit_number': permit.get('number'),
                        'type': permit.get('type'),
                        'address': permit.get('address'),
                        'project_name': permit.get('project_name'),
                        'value': permit.get('value'),
                        'status': permit.get('status'),
                        'issued_date': permit.get('issued_date'),
                        'developer': permit.get('developer')
                    })
        
        # Sort by date (most recent first)
        permits.sort(key=lambda x: x.get('issued_date', ''), reverse=True)
        
        return jsonify({
            'status': 'success',
            'total': len(permits[:limit]),
            'permits': permits[:limit],
            'filters': {
                'type': permit_type,
                'area': area
            },
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting recent permits: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/market/trends', methods=['GET'])
def get_market_trends():
    """Get current market trends and projections"""
    try:
        # Get market and financial data
        market_data = get_agent_knowledge('Market', 'trends')
        financial_data = get_agent_knowledge('Financial', 'market_analysis')
        
        trends = {
            'residential': {
                'price_trend': 'increasing',
                'inventory': 'low',
                'demand': 'high',
                'hot_areas': []
            },
            'commercial': {
                'vacancy_rate': 0,
                'rental_rates': {},
                'sectors': {}
            },
            'industrial': {
                'demand': 'high',
                'new_construction': 0,
                'vacancy_rate': 0
            },
            'projections': {
                'next_quarter': {},
                'next_year': {}
            }
        }
        
        # Extract trend data
        for item in market_data:
            if 'residential_trends' in item:
                trends['residential'].update(item['residential_trends'])
            if 'commercial_trends' in item:
                trends['commercial'].update(item['commercial_trends'])
            if 'projections' in item:
                trends['projections'].update(item['projections'])
        
        return jsonify({
            'status': 'success',
            'trends': trends,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting market trends: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/opportunities/investment', methods=['POST'])
def find_investment_opportunities():
    """Find investment opportunities based on criteria"""
    try:
        data = request.get_json()
        
        # Extract criteria
        budget_min = data.get('budget_min', 0)
        budget_max = data.get('budget_max', float('inf'))
        property_types = data.get('property_types', ['all'])
        areas = data.get('areas', [])
        min_roi = data.get('min_roi', 0)
        
        # Get financial and market data
        financial_data = get_agent_knowledge('Financial', 'opportunities')
        market_data = get_agent_knowledge('Market', 'development_opportunities')
        
        opportunities = []
        
        # Search for matching opportunities
        for item in financial_data:
            if 'opportunities' in item:
                for opp in item['opportunities']:
                    # Apply filters
                    if opp.get('investment_required', 0) < budget_min:
                        continue
                    if opp.get('investment_required', float('inf')) > budget_max:
                        continue
                    if property_types != ['all'] and opp.get('type') not in property_types:
                        continue
                    if areas and not any(area in opp.get('location', '') for area in areas):
                        continue
                    if opp.get('projected_roi', 0) < min_roi:
                        continue
                    
                    opportunities.append({
                        'id': opp.get('id'),
                        'name': opp.get('name'),
                        'type': opp.get('type'),
                        'location': opp.get('location'),
                        'investment_required': opp.get('investment_required'),
                        'projected_roi': opp.get('projected_roi'),
                        'risk_level': opp.get('risk_level'),
                        'timeline': opp.get('timeline'),
                        'description': opp.get('description')
                    })
        
        # Sort by ROI (highest first)
        opportunities.sort(key=lambda x: x.get('projected_roi', 0), reverse=True)
        
        return jsonify({
            'status': 'success',
            'total': len(opportunities),
            'opportunities': opportunities,
            'criteria': {
                'budget_range': f"${budget_min:,.0f} - ${budget_max:,.0f}" if budget_max != float('inf') else f"${budget_min:,.0f}+",
                'property_types': property_types,
                'areas': areas,
                'min_roi': f"{min_roi}%"
            },
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error finding investment opportunities: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/risks/assessment', methods=['POST'])
def assess_project_risks():
    """Assess risks for a specific project or area"""
    try:
        data = request.get_json()
        
        location = data.get('location')
        project_type = data.get('project_type')
        
        if not location:
            return jsonify({'error': 'Location is required', 'status': 'error'}), 400
        
        # Get risk data from multiple agents
        environmental_data = get_agent_knowledge('Environmental', 'risk_assessment')
        regulatory_data = get_agent_knowledge('Regulatory', 'compliance_risks')
        market_data = get_agent_knowledge('Market', 'risk_factors')
        
        risk_assessment = {
            'location': location,
            'project_type': project_type,
            'environmental_risks': [],
            'regulatory_risks': [],
            'market_risks': [],
            'overall_risk_score': 0,
            'mitigation_strategies': []
        }
        
        # Compile risks from different sources
        for item in environmental_data:
            if location.lower() in str(item).lower():
                if 'flood_risk' in item:
                    risk_assessment['environmental_risks'].append({
                        'type': 'flood',
                        'level': item['flood_risk'],
                        'details': item.get('flood_details', '')
                    })
                if 'contamination_risk' in item:
                    risk_assessment['environmental_risks'].append({
                        'type': 'contamination',
                        'level': item['contamination_risk'],
                        'details': item.get('contamination_details', '')
                    })
        
        # Calculate overall risk score (simplified)
        total_risks = len(risk_assessment['environmental_risks']) + \
                     len(risk_assessment['regulatory_risks']) + \
                     len(risk_assessment['market_risks'])
        
        if total_risks == 0:
            risk_assessment['overall_risk_score'] = 0.2  # Low risk
        elif total_risks <= 3:
            risk_assessment['overall_risk_score'] = 0.5  # Medium risk
        else:
            risk_assessment['overall_risk_score'] = 0.8  # High risk
        
        return jsonify({
            'status': 'success',
            'risk_assessment': risk_assessment,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error assessing project risks: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/developers/top', methods=['GET'])
def get_top_developers():
    """Get top developers by permit activity"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # Get market data about developers
        market_data = get_agent_knowledge('Market', 'developer_analysis')
        
        developers = []
        
        for item in market_data:
            if 'developers' in item:
                for dev in item['developers']:
                    developers.append({
                        'name': dev.get('name'),
                        'permit_count': dev.get('permit_count', 0),
                        'average_home_value': dev.get('average_value'),
                        'specialization': dev.get('type'),
                        'active_projects': dev.get('projects', []),
                        'market_share': dev.get('market_share')
                    })
        
        # Sort by permit count
        developers.sort(key=lambda x: x.get('permit_count', 0), reverse=True)
        
        return jsonify({
            'status': 'success',
            'total': len(developers[:limit]),
            'developers': developers[:limit],
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting top developers: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@houston_endpoints.route('/api/v1/technology/innovations', methods=['GET'])
def get_tech_innovations():
    """Get technology and innovation opportunities in Houston real estate"""
    try:
        # Get technology agent data
        tech_data = get_agent_knowledge('Technology_Innovation', 'innovations')
        
        innovations = []
        
        for item in tech_data:
            if 'innovations' in item:
                for innovation in item['innovations']:
                    innovations.append({
                        'technology': innovation.get('name'),
                        'category': innovation.get('category'),
                        'application': innovation.get('application'),
                        'benefits': innovation.get('benefits', []),
                        'adoption_rate': innovation.get('adoption_rate'),
                        'implementation_cost': innovation.get('cost'),
                        'roi_potential': innovation.get('roi_potential')
                    })
        
        return jsonify({
            'status': 'success',
            'total': len(innovations),
            'innovations': innovations,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting tech innovations: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500