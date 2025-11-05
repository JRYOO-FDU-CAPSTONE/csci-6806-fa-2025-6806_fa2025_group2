#!/usr/bin/env python3
"""
Simple unit test for A4 eviction policies
Tests basic functionality of PolicyLRU, PolicyDTSLRU, and PolicyEDE
"""

import sys
import os

# Add BCacheSim to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BCacheSim'))

from cachesim.policies_a4 import PolicyLRU, PolicyDTSLRU, PolicyEDE

class MockItem:
    """Mock cache item for testing"""
    def __init__(self, key, size=128*1024, timestamp=0):
        self.key = key
        self.size = size
        self.admission_time = timestamp
        self.last_access_time = timestamp


def test_policy_lru():
    """Test basic LRU functionality"""
    print("\n=== Testing PolicyLRU ===")
    policy = PolicyLRU()
    
    # Admit items
    for i in range(5):
        item = MockItem(f"key{i}")
        policy.admit(f"key{i}", item)
    
    assert len(policy) == 5, "Should have 5 items"
    print(f"✓ Admitted 5 items, cache size: {len(policy)}")
    
    # Touch key2 (make it MRU)
    policy.touch("key2")
    
    # Victim should be key0 (oldest)
    victim = policy.victim()
    assert victim == "key0", f"Expected key0, got {victim}"
    print(f"✓ Victim is oldest: {victim}")
    
    # Evict
    key, item = policy.evict()
    assert key == "key0", f"Expected to evict key0, got {key}"
    assert len(policy) == 4, "Should have 4 items after eviction"
    print(f"✓ Evicted {key}, remaining: {len(policy)}")
    
    print("✓ PolicyLRU tests passed!")
    return True


def test_policy_dtslru():
    """Test DT-SLRU with promotion logic"""
    print("\n=== Testing PolicyDTSLRU ===")
    policy = PolicyDTSLRU(tau_dt=1.0)
    
    # Admit items
    for i in range(5):
        item = MockItem(f"key{i}")
        policy.admit(f"key{i}", item)
    
    assert len(policy) == 5, "Should have 5 items"
    print(f"✓ Admitted 5 items, cache size: {len(policy)}")
    
    # All items should be in probation initially
    assert len(policy.probation) == 5, "All items should be in probation"
    assert len(policy.protected) == 0, "No items in protected yet"
    print(f"✓ Probation: {len(policy.probation)}, Protected: {len(policy.protected)}")
    
    # Touch key1 twice to promote it
    policy.touch("key1")  # First hit
    policy.touch("key1")  # Second hit - should promote
    
    assert "key1" in policy.protected, "key1 should be promoted to protected"
    print(f"✓ key1 promoted to Protected after 2 hits")
    
    # Victim should come from probation (key0)
    victim = policy.victim()
    assert victim == "key0", f"Expected key0 from probation, got {victim}"
    print(f"✓ Victim from Probation: {victim}")
    
    print("✓ PolicyDTSLRU tests passed!")
    return True


def test_policy_ede():
    """Test Episode-Deadline Eviction"""
    print("\n=== Testing PolicyEDE ===")
    policy = PolicyEDE(alpha_tti=0.5, protected_cap=0.3)
    
    # Admit items with timestamps
    for i in range(5):
        item = MockItem(f"key{i}", timestamp=i*100)
        policy.admit(f"key{i}", item)
    
    assert len(policy) == 5, "Should have 5 items"
    print(f"✓ Admitted 5 items, cache size: {len(policy)}")
    
    # Check that expiry times are set
    assert len(policy.expiry_times) == 5, "All items should have expiry times"
    print(f"✓ Expiry times calculated for all items")
    
    # Touch an item to update its expiry
    if "key2" in policy.items:
        policy.touch("key2")
        print(f"✓ Updated expiry time for key2")
    
    # Get victim
    victim = policy.victim()
    assert victim is not None, "Should have a victim"
    print(f"✓ Victim selected: {victim}")
    
    # Evict
    key, item = policy.evict()
    assert key is not None, "Should evict an item"
    assert len(policy) == 4, "Should have 4 items after eviction"
    print(f"✓ Evicted {key}, remaining: {len(policy)}")
    
    print("✓ PolicyEDE tests passed!")
    return True


def test_dt_calculation():
    """Test DT-per-byte calculation"""
    print("\n=== Testing DT Calculation ===")
    from cachesim.policies_a4 import compute_dt_per_byte
    
    # Test with default parameters
    size_bytes = 128 * 1024  # 128 KB
    dt = compute_dt_per_byte(size_bytes, seek_time_ms=5.0, bandwidth_mbps=100)
    
    assert dt > 0, "DT should be positive"
    print(f"✓ DT per byte for 128KB: {dt:.6f} ms/byte")
    
    # Larger objects should have lower DT per byte (amortized seek time)
    dt_large = compute_dt_per_byte(1024*1024, seek_time_ms=5.0, bandwidth_mbps=100)
    assert dt_large < dt, "Larger objects should have lower DT per byte"
    print(f"✓ DT per byte for 1MB: {dt_large:.6f} ms/byte (lower than 128KB)")
    
    print("✓ DT calculation tests passed!")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("A4 Eviction Policies - Unit Tests")
    print("=" * 60)
    
    try:
        tests = [
            test_dt_calculation,
            test_policy_lru,
            test_policy_dtslru,
            test_policy_ede,
        ]
        
        for test in tests:
            if not test():
                print(f"\n✗ Test failed: {test.__name__}")
                return 1
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
