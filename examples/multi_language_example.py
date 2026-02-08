"""
Example: Multi-Language Project Detection
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from thalos_core import IntelligentAnalyzer


def demonstrate_language_detection():
    """Demonstrate advanced language detection"""
    print("=" * 70)
    print("Multi-Language Detection Example")
    print("=" * 70)
    
    # Create analyzer
    analyzer = IntelligentAnalyzer('.')
    
    print("\n🔍 Analyzing project structure...")
    context = analyzer.analyze_project()
    
    print("\n📋 Detection Results:")
    print(f"\n  Languages Detected ({len(context.languages)}):")
    for lang in context.languages:
        print(f"    • {lang}")
    
    print(f"\n  Frameworks Detected ({len(context.frameworks)}):")
    for framework in context.frameworks:
        print(f"    • {framework}")
    
    print(f"\n  Build Tools Available ({len(context.build_tools)}):")
    for tool in context.build_tools:
        print(f"    • {tool}")
    
    print(f"\n  Files Analyzed: {len(context.file_signatures)}")
    
    print("\n  Optimization Hints:")
    for hint, value in context.optimization_hints.items():
        print(f"    • {hint}: {value}")


if __name__ == '__main__':
    demonstrate_language_detection()
