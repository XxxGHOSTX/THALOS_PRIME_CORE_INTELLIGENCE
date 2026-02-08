"""
THALOS PRIME - Advanced Utilities Module

Additional helper utilities for superior automation capabilities.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class BuildMetrics:
    """Track build performance metrics"""
    start_time: float
    end_time: float
    duration: float
    strategy_used: str
    languages_detected: List[str]
    files_analyzed: int
    cache_hit: bool
    success: bool
    optimization_gains: Dict[str, Any]


class MetricsCollector:
    """Collect and analyze build metrics for continuous improvement"""
    
    def __init__(self, metrics_file: Path):
        self.metrics_file = metrics_file
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_build: Optional[Dict[str, Any]] = None
    
    def start_build(self, strategy: str, context: Any):
        """Start tracking a build"""
        self.current_build = {
            'start_time': time.time(),
            'strategy_used': strategy,
            'languages_detected': context.languages if hasattr(context, 'languages') else [],
            'files_analyzed': len(context.file_signatures) if hasattr(context, 'file_signatures') else 0
        }
    
    def end_build(self, success: bool, cache_hit: bool = False, optimization_gains: Optional[Dict] = None):
        """Complete build tracking"""
        if self.current_build is None:
            return
        
        end_time = time.time()
        self.current_build.update({
            'end_time': end_time,
            'duration': end_time - self.current_build['start_time'],
            'success': success,
            'cache_hit': cache_hit,
            'optimization_gains': optimization_gains or {}
        })
        
        self._save_metrics()
    
    def _save_metrics(self):
        """Save metrics to file"""
        if self.current_build is None:
            return
        
        # Load existing metrics
        metrics = []
        if self.metrics_file.exists():
            try:
                metrics = json.loads(self.metrics_file.read_text())
            except:
                pass
        
        # Append new build
        metrics.append(self.current_build)
        
        # Keep only last 100 builds
        metrics = metrics[-100:]
        
        # Save
        self.metrics_file.write_text(json.dumps(metrics, indent=2))
        self.current_build = None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get build statistics"""
        if not self.metrics_file.exists():
            return {}
        
        try:
            metrics = json.loads(self.metrics_file.read_text())
            
            total_builds = len(metrics)
            successful_builds = sum(1 for m in metrics if m.get('success', False))
            avg_duration = sum(m.get('duration', 0) for m in metrics) / total_builds if total_builds > 0 else 0
            cache_hits = sum(1 for m in metrics if m.get('cache_hit', False))
            
            return {
                'total_builds': total_builds,
                'successful_builds': successful_builds,
                'success_rate': successful_builds / total_builds if total_builds > 0 else 0,
                'average_duration': avg_duration,
                'cache_hit_rate': cache_hits / total_builds if total_builds > 0 else 0
            }
        except:
            return {}


class DependencyResolver:
    """Advanced dependency resolution using graph analysis"""
    
    def __init__(self):
        self.dependency_graph: Dict[str, List[str]] = {}
    
    def add_dependency(self, package: str, depends_on: List[str]):
        """Add a dependency relationship"""
        self.dependency_graph[package] = depends_on
    
    def get_build_order(self) -> List[str]:
        """Get optimal build order using topological sort"""
        # Simple topological sort implementation
        visited = set()
        result = []
        
        def visit(node: str):
            if node in visited:
                return
            visited.add(node)
            
            for dep in self.dependency_graph.get(node, []):
                visit(dep)
            
            result.append(node)
        
        for node in self.dependency_graph:
            visit(node)
        
        return result
    
    def detect_cycles(self) -> List[List[str]]:
        """Detect circular dependencies"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def visit(node: str, path: List[str]) -> bool:
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for dep in self.dependency_graph.get(node, []):
                visit(dep, path + [node])
            
            rec_stack.remove(node)
            return False
        
        for node in self.dependency_graph:
            visit(node, [])
        
        return cycles


class SmartCache:
    """Intelligent caching with content-aware invalidation"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = cache_dir / 'cache_index.json'
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve from cache"""
        index = self._load_index()
        if key in index:
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                try:
                    return json.loads(cache_file.read_text())
                except:
                    pass
        return None
    
    def set(self, key: str, value: Any, dependencies: Optional[List[str]] = None):
        """Store in cache with dependencies"""
        index = self._load_index()
        
        cache_file = self.cache_dir / f"{key}.cache"
        cache_file.write_text(json.dumps(value, indent=2))
        
        index[key] = {
            'timestamp': time.time(),
            'dependencies': dependencies or [],
            'file': str(cache_file)
        }
        
        self._save_index(index)
    
    def invalidate(self, key: str):
        """Invalidate cache entry"""
        index = self._load_index()
        if key in index:
            cache_file = Path(index[key]['file'])
            if cache_file.exists():
                cache_file.unlink()
            del index[key]
            self._save_index(index)
    
    def invalidate_dependent(self, dependency: str):
        """Invalidate all entries that depend on a specific dependency"""
        index = self._load_index()
        to_invalidate = []
        
        for key, data in index.items():
            if dependency in data.get('dependencies', []):
                to_invalidate.append(key)
        
        for key in to_invalidate:
            self.invalidate(key)
    
    def clear(self):
        """Clear entire cache"""
        for file in self.cache_dir.glob("*.cache"):
            file.unlink()
        if self.index_file.exists():
            self.index_file.unlink()
    
    def _load_index(self) -> Dict[str, Any]:
        """Load cache index"""
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except:
                pass
        return {}
    
    def _save_index(self, index: Dict[str, Any]):
        """Save cache index"""
        self.index_file.write_text(json.dumps(index, indent=2))


class PatternLearner:
    """Learn from build patterns to improve future builds"""
    
    def __init__(self, learning_file: Path):
        self.learning_file = learning_file
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        self.patterns: Dict[str, Any] = self._load_patterns()
    
    def record_pattern(self, project_type: str, strategy: str, success: bool, duration: float):
        """Record a build pattern"""
        if project_type not in self.patterns:
            self.patterns[project_type] = {
                'strategies': {},
                'total_builds': 0
            }
        
        if strategy not in self.patterns[project_type]['strategies']:
            self.patterns[project_type]['strategies'][strategy] = {
                'success_count': 0,
                'failure_count': 0,
                'avg_duration': 0,
                'total_duration': 0,
                'count': 0
            }
        
        strategy_data = self.patterns[project_type]['strategies'][strategy]
        
        if success:
            strategy_data['success_count'] += 1
        else:
            strategy_data['failure_count'] += 1
        
        strategy_data['total_duration'] += duration
        strategy_data['count'] += 1
        strategy_data['avg_duration'] = strategy_data['total_duration'] / strategy_data['count']
        
        self.patterns[project_type]['total_builds'] += 1
        
        self._save_patterns()
    
    def get_best_strategy(self, project_type: str) -> Optional[str]:
        """Get the best strategy for a project type based on learning"""
        if project_type not in self.patterns:
            return None
        
        strategies = self.patterns[project_type]['strategies']
        if not strategies:
            return None
        
        # Score based on success rate and duration
        best_strategy = None
        best_score = -1
        
        for strategy, data in strategies.items():
            if data['count'] == 0:
                continue
            
            success_rate = data['success_count'] / data['count']
            # Normalize duration (inverse, so faster is better)
            duration_score = 1 / (data['avg_duration'] + 1)
            
            # Combined score (70% success rate, 30% speed)
            score = (success_rate * 0.7) + (duration_score * 0.3)
            
            if score > best_score:
                best_score = score
                best_strategy = strategy
        
        return best_strategy
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load learned patterns"""
        if self.learning_file.exists():
            try:
                return json.loads(self.learning_file.read_text())
            except:
                pass
        return {}
    
    def _save_patterns(self):
        """Save learned patterns"""
        self.learning_file.write_text(json.dumps(self.patterns, indent=2))


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


def detect_cpu_cores() -> int:
    """Detect available CPU cores for parallel execution"""
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except:
        return 4  # Default fallback
