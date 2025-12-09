#!/usr/bin/env python3
"""
Drone Image Analysis System - Launcher
Supports both CLI and GUI modes
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
  python3 run.py                    # Launch GUI (default)
  python3 run.py --cli              # Launch CLI interface
  python3 run.py --auto             # Auto demo mode (CLI)
  python3 run.py --legacy           # Launch legacy PyQt5 UI (if available)
        """
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode (interactive menu)'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Run auto-demo mode (CLI)'
    )
    parser.add_argument(
        '--legacy',
        action='store_true',
        help='Run legacy PyQt5 UI (original main.py)'
    )
    parser.add_argument(
        '--ui',
        action='store_true',
        default=True,
        help='Run GUI mode (default)'
    )
    
    args = parser.parse_args()
    
    # Determine which mode to run
    if args.cli or args.auto:
        logger.info('Launching in CLI mode...')
        from application import DroneAPP, main as cli_main
        if args.auto:
            # Auto demo
            from application import main
            sys.argv = [sys.argv[0], '--auto']
            main()
        else:
            # Interactive menu
            cli_main()
    elif args.legacy:
        logger.info('Launching legacy PyQt5 UI...')
        try:
            from main import DroneApp
            app = DroneApp()
            app.show()
            sys.exit(app.exec_())
        except Exception as e:
            logger.error('Failed to launch legacy UI: %s', e)
            logger.info('Falling back to new UI...')
            from ui_integration import main as ui_main
            ui_main()
    else:
        # Default: new integrated UI
        logger.info('Launching new integrated UI...')
        from ui_integration import main as ui_main
        ui_main()


if __name__ == '__main__':
    main()
