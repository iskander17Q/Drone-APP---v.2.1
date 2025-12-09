#!/usr/bin/env python3
"""
Drone Image Analysis System - Launcher
Supports CLI and GUI modes
"""
import sys
import argparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Drone Image Analysis System - Design Patterns Application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run.py                    # Launch interactive CLI (default)
  python3 run.py --auto             # Auto demo mode
  python3 run.py --ui               # Launch PyQt5 GUI (requires PyQt5)
        """
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Run auto-demo mode'
    )
    parser.add_argument(
        '--ui',
        action='store_true',
        help='Run GUI mode (requires PyQt5)'
    )
    
    args = parser.parse_args()
    
    try:
        from application import DroneAPP, main as app_main
        
        if args.auto:
            logger.info('Starting auto-demo mode...')
            app_main()
        elif args.ui:
            logger.info('Starting GUI mode...')
            from ui_integration import main as ui_main
            ui_main()
        else:
            # Default: Interactive CLI menu
            logger.info('Starting interactive CLI menu...')
            app = DroneAPP()
            app.interactive_menu()
            
    except KeyboardInterrupt:
        logger.info('Application interrupted by user')
        sys.exit(0)
    except Exception as e:
        logger.error(f'Error: {e}', exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
