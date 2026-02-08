"""
Example: Using THALOS PRIME for Python Project Analysis
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from thalos_core import ThalosCore, BuildStrategy


def example_basic_analysis():
    """Basic project analysis example"""
    print("=" * 70)
    print("Example 1: Basic Project Analysis")
    print("=" * 70)
    
    # Analyze current directory
    thalos = ThalosCore('.')
    info = thalos.get_project_info()
    
    print("\n📊 Project Analysis Results:")
    print(f"  Languages: {', '.join(info['languages']) or 'None detected'}")
    print(f"  Frameworks: {', '.join(info['frameworks']) or 'None detected'}")
    print(f"  Build Tools: {', '.join(info['build_tools']) or 'None detected'}")
    print(f"  Optimization Hints: {info['optimization_hints']}")
    
    if info['dependencies']:
        print("\n  Dependencies:")
        for lang, deps in info['dependencies'].items():
            print(f"    {lang}: {len(deps)} dependencies")


def example_custom_strategy():
    """Example with custom build strategy"""
    print("\n" + "=" * 70)
    print("Example 2: Build with Custom Strategy")
    print("=" * 70)
    
    thalos = ThalosCore('.')
    
    # Use intelligent parallel strategy
    print("\n🚀 Building with Intelligent Parallel strategy...")
    success = thalos.analyze_and_build(BuildStrategy.INTELLIGENT_PARALLEL)
    
    if success:
        print("✅ Build completed successfully!")
    else:
        print("❌ Build failed - check logs")


def example_adaptive_learning():
    """Example with adaptive learning (default)"""
    print("\n" + "=" * 70)
    print("Example 3: Adaptive Learning Build")
    print("=" * 70)
    
    thalos = ThalosCore('.')
    
    print("\n🎓 Building with Adaptive Learning strategy...")
    print("   (System will automatically select optimal strategy)")
    
    success = thalos.analyze_and_build(BuildStrategy.ADAPTIVE_LEARNING)
    
    return success


if __name__ == '__main__':
    print("\n🧠 THALOS PRIME - Usage Examples\n")
    
    # Run examples
    example_basic_analysis()
    
    # Uncomment to run build examples
    # example_custom_strategy()
    # example_adaptive_learning()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
