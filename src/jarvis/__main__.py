"""Entry point for running Jarvis as a module: python -m jarvis"""

from jarvis.assistant import Jarvis

def main():
    """Main entry point."""
    jarvis = Jarvis()
    jarvis.run()

if __name__ == "__main__":
    main()
