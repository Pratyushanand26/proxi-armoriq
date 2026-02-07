#!/usr/bin/env python3
"""
Quick verification script to test Proxi components.
Run this to verify the installation is working correctly.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.guardrails.policy_engine import PolicyEngine, PolicyViolationError
        print("  ✓ Policy Engine")
    except Exception as e:
        print(f"  ✗ Policy Engine: {e}")
        return False
    
    try:
        from src.mcp_server.tools import cloud_infra
        print("  ✓ MCP Tools")
    except Exception as e:
        print(f"  ✗ MCP Tools: {e}")
        return False
    
    try:
        from src.agent.bot import ProxiAgent
        print("  ✓ Agent")
    except Exception as e:
        print(f"  ✗ Agent: {e}")
        return False
    
    return True


def test_policy_engine():
    """Test the policy engine functionality."""
    print("\nTesting Policy Engine...")
    
    from src.guardrails.policy_engine import PolicyEngine, PolicyViolationError
    
    try:
        # Load policy
        engine = PolicyEngine("policies/ops_policy.json")
        print("  ✓ Policy loaded")
        
        # Test NORMAL mode validation
        engine.set_mode("NORMAL")
        
        # Should succeed
        engine.validate("get_service_status")
        print("  ✓ NORMAL mode: read-only allowed")
        
        # Should fail
        try:
            engine.validate("restart_service")
            print("  ✗ NORMAL mode: restart should be blocked")
            return False
        except PolicyViolationError:
            print("  ✓ NORMAL mode: restart correctly blocked")
        
        # Test EMERGENCY mode
        engine.set_mode("EMERGENCY")
        engine.validate("restart_service")
        print("  ✓ EMERGENCY mode: restart allowed")
        
        # Delete should always be blocked
        try:
            engine.validate("delete_database")
            print("  ✗ Delete should always be blocked")
            return False
        except PolicyViolationError:
            print("  ✓ Delete correctly blocked (always)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_tools():
    """Test the mock cloud infrastructure tools."""
    print("\nTesting Cloud Tools...")
    
    from src.mcp_server.tools import cloud_infra
    
    try:
        # Test read operations
        status = cloud_infra.get_service_status()
        print(f"  ✓ Get status: {len(status['services'])} services")
        
        logs = cloud_infra.read_logs(5)
        print(f"  ✓ Read logs: {len(logs['log_lines'])} lines")
        
        # Test active operations
        result = cloud_infra.restart_service("web-server")
        print(f"  ✓ Restart service: {result['status']}")
        
        result = cloud_infra.scale_fleet(5)
        print(f"  ✓ Scale fleet: {result['new_size']} instances")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_agent():
    """Test agent initialization."""
    print("\nTesting Agent...")
    
    from src.agent.bot import ProxiAgent
    
    try:
        agent = ProxiAgent(use_mock=True)
        print("  ✓ Agent initialized with mock LLM")
        
        # Test that tools are available
        print(f"  ✓ Agent has {len(agent.tools)} tools available")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("  PROXI INSTALLATION VERIFICATION")
    print("="*60 + "\n")
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
        print("\n❌ Import test failed. Check your installation.")
    
    if not test_policy_engine():
        all_passed = False
        print("\n❌ Policy Engine test failed.")
    
    if not test_tools():
        all_passed = False
        print("\n❌ Tools test failed.")
    
    if not test_agent():
        all_passed = False
        print("\n❌ Agent test failed.")
    
    print("\n" + "="*60)
    if all_passed:
        print("  ✅ ALL TESTS PASSED")
        print("  Ready to run the demo with: python main.py")
    else:
        print("  ❌ SOME TESTS FAILED")
        print("  Please check the error messages above")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
