#!/usr/bin/env python3
"""
🌐 VoltageGPU Dashboard API
API backend for the SHA-256 Bot dashboard integration
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import sqlite3
import logging
from datetime import datetime, timedelta
import threading
import time
import os
from modules.monitoring import monitor
from modules.security import security_manager
from modules.anti_shadowban import anti_shadowban
from modules.human_behavior import human_behavior

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'voltagegpu-sha256-dashboard-2025'
CORS(app, origins=["https://voltagegpu.com", "http://localhost:*"])
socketio = SocketIO(app, cors_allowed_origins=["https://voltagegpu.com", "http://localhost:*"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global bot status
bot_status = {
    'running': False,
    'start_time': None,
    'last_activity': None,
    'posts_today': 0,
    'success_rate': 0.0,
    'platforms': {
        'twitter': {'status': 'disconnected', 'last_post': None},
        'reddit': {'status': 'disconnected', 'last_post': None},
        'telegram': {'status': 'disconnected', 'last_post': None}
    }
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get current bot status"""
    try:
        # Get monitoring data
        performance_summary = monitor.get_performance_summary()
        security_status = security_manager.get_security_status()
        
        # Get platform statuses
        platform_statuses = {}
        for platform in ['twitter', 'reddit', 'telegram']:
            platform_statuses[platform] = anti_shadowban.get_platform_status(platform)
        
        return jsonify({
            'success': True,
            'data': {
                'bot_status': bot_status,
                'performance': performance_summary,
                'security': security_status,
                'platforms': platform_statuses,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """Get performance metrics"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
        metrics = {
            'cpu_usage': monitor.get_metric_history('cpu_percent', hours),
            'memory_usage': monitor.get_metric_history('memory_percent', hours),
            'posts_sent': monitor.get_metric_history('counter_posts_sent', hours),
            'success_rate': monitor.get_metric_history('success_rate', hours)
        }
        
        return jsonify({
            'success': True,
            'data': metrics
        })
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    try:
        hours = request.args.get('hours', 24, type=int)
        alerts = monitor.get_alerts(hours)
        
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/security/audit')
def get_security_audit():
    """Get security audit report"""
    try:
        hours = request.args.get('hours', 24, type=int)
        audit = security_manager.audit_security_events(hours)
        
        return jsonify({
            'success': True,
            'data': audit
        })
    except Exception as e:
        logger.error(f"Error getting security audit: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the bot"""
    try:
        global bot_status
        
        if bot_status['running']:
            return jsonify({
                'success': False,
                'error': 'Bot is already running'
            }), 400
        
        # Start monitoring
        monitor.start_monitoring()
        
        # Update status
        bot_status['running'] = True
        bot_status['start_time'] = datetime.now().isoformat()
        bot_status['last_activity'] = datetime.now().isoformat()
        
        # Log security event
        security_manager.log_security_event(
            'bot_started', 'medium', 'api',
            'Bot started via dashboard API',
            {'source_ip': request.remote_addr}
        )
        
        # Emit status update
        socketio.emit('bot_status_changed', {
            'status': 'started',
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Bot started successfully'
        })
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    try:
        global bot_status
        
        if not bot_status['running']:
            return jsonify({
                'success': False,
                'error': 'Bot is not running'
            }), 400
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        # Update status
        bot_status['running'] = False
        bot_status['start_time'] = None
        
        # Log security event
        security_manager.log_security_event(
            'bot_stopped', 'medium', 'api',
            'Bot stopped via dashboard API',
            {'source_ip': request.remote_addr}
        )
        
        # Emit status update
        socketio.emit('bot_status_changed', {
            'status': 'stopped',
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Bot stopped successfully'
        })
        
    except Exception as e:
        logger.error(f"Error stopping bot: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bot/restart', methods=['POST'])
def restart_bot():
    """Restart the bot"""
    try:
        # Stop first
        stop_response = stop_bot()
        if not stop_response[0].get_json().get('success'):
            return stop_response
        
        # Wait a moment
        time.sleep(2)
        
        # Start again
        return start_bot()
        
    except Exception as e:
        logger.error(f"Error restarting bot: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config', methods=['GET', 'POST'])
def bot_config():
    """Get or update bot configuration"""
    if request.method == 'GET':
        try:
            # Return current configuration
            config = {
                'platforms': {
                    'twitter': {
                        'enabled': True,
                        'posting_interval': 30,
                        'daily_limit': 50
                    },
                    'reddit': {
                        'enabled': True,
                        'posting_interval': 240,
                        'daily_limit': 10
                    },
                    'telegram': {
                        'enabled': True,
                        'posting_interval': 10,
                        'daily_limit': 100
                    }
                },
                'content': {
                    'affiliate_code': os.getenv('AFFILIATE_CODE', 'YOUR_AFFILIATE_CODE'),
                    'base_url': os.getenv('BASE_URL', 'https://voltagegpu.com'),
                    'auto_optimize': True
                },
                'security': {
                    'anti_shadowban': True,
                    'human_behavior': True,
                    'content_analysis': True
                }
            }
            
            return jsonify({
                'success': True,
                'data': config
            })
            
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    else:  # POST
        try:
            config_data = request.get_json()
            
            # Validate and save configuration
            # In a real implementation, this would save to database
            
            # Log security event
            security_manager.log_security_event(
                'config_updated', 'medium', 'api',
                'Bot configuration updated via dashboard',
                {'source_ip': request.remote_addr, 'config': config_data}
            )
            
            return jsonify({
                'success': True,
                'message': 'Configuration updated successfully'
            })
            
        except Exception as e:
            logger.error(f"Error updating config: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    try:
        lines = request.args.get('lines', 100, type=int)
        
        # Read log file
        log_file = 'voltagegpu_bot.log'
        logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-lines:]
        
        return jsonify({
            'success': True,
            'data': {
                'logs': [log.strip() for log in logs],
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/widget')
def widget():
    """Embeddable widget for voltagegpu.com"""
    return render_template('widget.html')

@app.route('/api/widget/status')
def widget_status():
    """Simplified status for widget"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'running': bot_status['running'],
                'posts_today': bot_status['posts_today'],
                'success_rate': bot_status['success_rate'],
                'uptime': _calculate_uptime(),
                'affiliate_code': os.getenv('AFFILIATE_CODE', 'YOUR_AFFILIATE_CODE'),
                'last_update': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Error getting widget status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def _calculate_uptime():
    """Calculate bot uptime"""
    if not bot_status['running'] or not bot_status['start_time']:
        return 0
    
    start_time = datetime.fromisoformat(bot_status['start_time'])
    uptime_seconds = (datetime.now() - start_time).total_seconds()
    return int(uptime_seconds)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to SHA-256 Bot Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('request_status')
def handle_status_request():
    """Handle status request from client"""
    try:
        status_data = get_status().get_json()
        emit('status_update', status_data)
    except Exception as e:
        logger.error(f"Error handling status request: {e}")
        emit('error', {'message': str(e)})

# Background task to send periodic updates
def background_updates():
    """Send periodic updates to connected clients"""
    while True:
        try:
            if bot_status['running']:
                # Update bot activity
                bot_status['last_activity'] = datetime.now().isoformat()
                
                # Get current metrics
                current_metrics = monitor.get_current_metrics()
                
                # Emit updates
                socketio.emit('metrics_update', {
                    'timestamp': datetime.now().isoformat(),
                    'metrics': current_metrics
                })
            
            time.sleep(10)  # Update every 10 seconds
            
        except Exception as e:
            logger.error(f"Error in background updates: {e}")
            time.sleep(30)

# Start background thread
background_thread = threading.Thread(target=background_updates, daemon=True)
background_thread.start()

if __name__ == '__main__':
    # Initialize security and monitoring
    security_manager.log_security_event(
        'dashboard_started', 'low', 'system',
        'Dashboard API server started'
    )
    
    # Run the app
    print("🚀 SHA-256 Bot Dashboard API starting...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🌐 Widget endpoint: http://localhost:5000/widget")
    print("🔗 For voltagegpu.com integration")
    print("🎯 Affiliate Code: SHA-256-76360B81D39F")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
