from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from agents.priority_agent import PriorityAgent
from agents.resource_agent import ResourceAgent
from agents.risk_agent import RiskAgent
from agents.coordinator import Coordinator

class SwarmDecisionEngine:
    """Swarm Intelligence 決策引擎"""
    
    def __init__(self, neo4j_manager=None, config: Optional[Dict[str, Any]] = None):
        """
        初始化 Swarm 決策引擎
        
        Args:
            neo4j_manager: Neo4j 管理器（可選）
            config: 配置參數（可選）
        """
        self.name = "Swarm Decision Engine"
        self.version = "1.0.0"
        self.neo4j_manager = neo4j_manager
        self.config = config or {}
        
        # 初始化 AI 代理人
        self.priority_agent = PriorityAgent(neo4j_manager, config)
        self.resource_agent = ResourceAgent(neo4j_manager, config)
        self.risk_agent = RiskAgent(neo4j_manager, config)
        self.coordinator = Coordinator()
        
        self.agents = [
            self.priority_agent,
            self.resource_agent,
            self.risk_agent
        ]
        
        print("🐝 Swarm Decision Engine 初始化完成")
        print(f"📋 載入 {len(self.agents)} 個專家代理人")
    
    def make_decision(self, task: Dict[str, Any], people: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        執行 Swarm 群體決策
        
        Args:
            task: 任務資訊
            people: 可用人員列表（可選，如果不提供則使用預設）
            
        Returns:
            決策結果
        """
        try:
            # 如果沒有提供人員列表，使用預設人員
            if people is None:
                people = self._get_default_people()
            
            # 更新資源代理人的人員資料
            if hasattr(self.resource_agent, 'available_people'):
                self.resource_agent.available_people = people
            
            print(f"🎯 開始為任務 {task.get('id', 'unknown')} 進行群體決策")
            
            # 收集各代理人的分析結果
            agent_results = {}
            
            # 優先權分析
            print("📊 執行優先權分析...")
            priority_result = self.priority_agent.analyze_priority(task)
            agent_results['priority'] = priority_result
            
            # 資源配對分析
            print("👤 執行資源配對分析...")
            resource_result = self.resource_agent.find_suitable_resources(task)
            agent_results['resources'] = resource_result
            
            # 風險評估
            print("⚠️ 執行風險評估...")
            risk_result = self.risk_agent.assess_risks(task)
            agent_results['risks'] = risk_result
            
            # 協調決策
            print("🤝 執行協調決策...")
            final_decision = self.coordinator.coordinate_decision(task, agent_results)
            
            # 增加 Swarm 引擎的元資料
            final_decision.update({
                'swarm_engine': self.name,
                'engine_version': self.version,
                'decision_method': 'swarm_intelligence',
                'agents_involved': len(self.agents),
                'people_considered': len(people)
            })
            
            print(f"✅ 決策完成，信心指數: {final_decision.get('confidence', 'N/A')}")
            
            return final_decision
            
        except Exception as e:
            print(f"❌ 決策過程發生錯誤: {e}")
            return {
                'decision_id': f"DEC_{task.get('id', 'unknown')}_ERROR",
                'task_id': task.get('id', 'unknown'),
                'recommendation': '群體決策失敗，建議人工評估',
                'confidence': 0.1,
                'risk_level': 'high',
                'assigned_to': '待分配',
                'error': str(e),
                'swarm_engine': self.name,
                'created_at': datetime.now().isoformat()
            }
    
    def _get_default_people(self) -> List[Dict[str, Any]]:
        """獲取預設人員列表"""
        return [
            {
                'id': 'PERSON001',
                'name': 'Alice Chen',
                'email': 'alice@company.com',
                'skills': ['Python', 'Flask', 'Database', 'Frontend'],
                'availability': 0.8,
                'current_workload': 0.6,
                'experience_level': 'senior',
                'department': 'Engineering'
            },
            {
                'id': 'PERSON002',
                'name': 'Bob Wang',
                'email': 'bob@company.com',
                'skills': ['Python', 'Neo4j', 'AI/ML', 'System Design'],
                'availability': 0.9,
                'current_workload': 0.4,
                'experience_level': 'senior',
                'department': 'Engineering'
            },
            {
                'id': 'PERSON003',
                'name': 'Carol Liu',
                'email': 'carol@company.com',
                'skills': ['Project Management', 'Requirements Analysis', 'Documentation'],
                'availability': 0.7,
                'current_workload': 0.5,
                'experience_level': 'mid',
                'department': 'Product'
            },
            {
                'id': 'PERSON004',
                'name': 'David Zhang',
                'email': 'david@company.com',
                'skills': ['System Design', 'Architecture', 'Performance'],
                'availability': 0.6,
                'current_workload': 0.7,
                'experience_level': 'senior',
                'department': 'Engineering'
            }
        ]
    
    def get_engine_status(self) -> Dict[str, Any]:
        """獲取引擎狀態"""
        return {
            'name': self.name,
            'version': self.version,
            'agents_count': len(self.agents),
            'agents_status': [
                {
                    'name': agent.name,
                    'version': getattr(agent, 'version', 'unknown'),
                    'status': 'active'
                }
                for agent in self.agents
            ],
            'coordinator_status': {
                'name': self.coordinator.name,
                'version': getattr(self.coordinator, 'version', 'unknown'),
                'status': 'active'
            }
        }
    
    def make_decision_with_custom_people(self, task: Dict[str, Any], people: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        使用自訂人員列表進行決策
        
        Args:
            task: 任務資訊
            people: 自訂人員列表
            
        Returns:
            決策結果
        """
        return self.make_decision(task, people)