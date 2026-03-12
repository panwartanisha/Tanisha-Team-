"""
Electricity Consumption Analysis - Flask Web Application
Purpose: Embed Tableau dashboards and stories in a responsive web interface
"""

from flask import Flask, render_template, jsonify
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'electricity-consumption-2024'

# Load summary statistics
try:
    with open('summary_statistics.json', 'r') as f:
        SUMMARY_STATS = json.load(f)
except:
    SUMMARY_STATS = {}

# ============================================================================
# CONFIGURATION
# ============================================================================

# Tableau Server Configuration (Update with your Tableau Server details)
TABLEAU_CONFIG = {
    'server_url': 'https://your-tableau-server.com',
    'dashboard_url': 'your_dashboard_url',
    'story_url': 'your_story_url',
    'use_iframe': True,  # Set to True if embedding via iframe (no authentication needed)
}

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home/Index page with overview"""
    return render_template('index.html', stats=SUMMARY_STATS)

@app.route('/dashboard')
def dashboard():
    """Embedded Tableau Dashboard Page"""
    return render_template('dashboard.html', 
                         config=TABLEAU_CONFIG,
                         stats=SUMMARY_STATS)

@app.route('/story')
def story():
    """Embedded Tableau Story Page with Multi-Scene Narrative"""
    return render_template('story.html',
                         config=TABLEAU_CONFIG,
                         stats=SUMMARY_STATS)

@app.route('/analysis')
def analysis():
    """Analysis & Insights Page"""
    insights = {
        'findings': [
            {
                'title': '2019 vs 2020 Consumption',
                'description': 'Electricity consumption decreased by 59.42% in 2020 compared to 2019, primarily due to COVID-19 lockdown.',
                'metric': '-59.42%',
                'period': 'Annual'
            },
            {
                'title': 'Regional Consumption',
                'description': 'Western Region leads with 31.61% of national consumption, followed by Northern Region at 29.61%.',
                'metric': 'WR: 540,370 units',
                'period': 'Total'
            },
            {
                'title': 'Top Consuming State',
                'description': 'Maharashtra is the highest electricity consumer with 217,080 units, followed by Gujarat and UP.',
                'metric': 'Maharashtra',
                'period': 'Highest'
            },
            {
                'title': 'Lockdown Recovery',
                'description': 'Post-lockdown consumption showed an 8.39% recovery rate from lockdown levels.',
                'metric': '+8.39%',
                'period': 'Recovery'
            }
        ],
        'scenarios': [
            {
                'number': 1,
                'title': 'Change in Overall Consumption Trends',
                'description': 'From January 2019 to December 2020, India\'s electricity consumption underwent significant changes influenced by seasonal demand, economic growth, and COVID-19 lockdown impact.',
                'key_insight': 'The nationwide lockdown (March-June 2020) resulted in a significant consumption drop, followed by gradual recovery.'
            },
            {
                'number': 2,
                'title': 'Regional Variations in Demand',
                'description': 'Electricity consumption patterns differed significantly across Indian regions due to climate, industrial presence, and population density.',
                'key_insight': 'Western Region showed highest consumption, while North-Eastern Region had minimal usage.'
            },
            {
                'number': 3,
                'title': 'Recovery After Lockdown',
                'description': 'Following COVID-19 restrictions, electricity demand began to recover, but the pace of recovery differed widely across states.',
                'key_insight': 'Some states showed quick recovery while others lagged behind, indicating differential economic rebound.'
            }
        ]
    }
    return render_template('analysis.html', insights=insights)

@app.route('/about')
def about():
    """Project Information Page"""
    project_info = {
        'title': 'Electricity Consumption Analysis in India',
        'duration': 'January 2, 2019 - December 5, 2020',
        'objective': 'Analyze electricity consumption patterns across Indian states and understand the impact of COVID-19 lockdown',
        'team': [
            {'name': 'Antas Kumar Dubey', 'role': 'Team Lead'},
            {'name': 'Archit Dubey', 'role': 'Team Member'},
            {'name': 'Ganesh Ramnayan Kanojiya', 'role': 'Team Member'},
            {'name': 'Ganesh Mangalam Sinha', 'role': 'Team Member'}
        ],
        'tools': ['Tableau', 'Flask', 'Python', 'MySQL'],
        'data_overview': {
            'total_records': SUMMARY_STATS.get('dataset_overview', {}).get('total_records', 'N/A'),
            'states': SUMMARY_STATS.get('dataset_overview', {}).get('unique_states', 'N/A'),
            'regions': SUMMARY_STATS.get('dataset_overview', {}).get('unique_regions', 'N/A'),
        }
    }
    return render_template('about.html', project_info=project_info)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for summary statistics"""
    return jsonify(SUMMARY_STATS)

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Electricity Consumption Analysis'
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', error_code=404, error_message='Page Not Found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("Electricity Consumption Analysis - Flask Web Application")
    print("=" * 80)
    print(f"\nStarting server on http://localhost:5000")
    print("\nRoutes:")
    print("  - Home:       http://localhost:5000/")
    print("  - Dashboard:  http://localhost:5000/dashboard")
    print("  - Story:      http://localhost:5000/story")
    print("  - Analysis:   http://localhost:5000/analysis")
    print("  - About:      http://localhost:5000/about")
    print("\nAPI Endpoints:")
    print("  - Statistics: http://localhost:5000/api/statistics")
    print("  - Health:     http://localhost:5000/api/health")
    print("=" * 80)
    
    # Run the Flask app (set debug=True for development)
    app.run(debug=True, host='0.0.0.0', port=5000)
