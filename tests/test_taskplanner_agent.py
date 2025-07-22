import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_thinktank_mvp.agents.taskplanner import TaskPlannerAgent

def format_llm_output(result):
    """格式化LLM输出，使其更易读"""
    if isinstance(result, dict):
        if "error" in result:
            return f"Error: {result['error']}"
        
        # 检查是否是复杂的任务树结构
        if "阶段" in result and isinstance(result["阶段"], dict):
            formatted = f"目标: {result.get('目标', 'N/A')}\n\n"
            for stage_name, stage_data in result["阶段"].items():
                formatted += f"## {stage_name}\n"
                if "子任务" in stage_data:
                    for i, task in enumerate(stage_data["子任务"], 1):
                        formatted += f"  {i}. {task.get('任务', 'N/A')}\n"
                        formatted += f"     {task.get('说明', 'N/A')}\n"
                formatted += "\n"
            return formatted
        else:
            # 普通字典，用JSON格式化
            return json.dumps(result, ensure_ascii=False, indent=2)
    elif isinstance(result, list):
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        return str(result)

def test_taskplanner_agent():
    agent = TaskPlannerAgent()  # 直接实例化，不传API key参数
    test_inputs = [
        "我想开发一个AI写作助手",
        "我要做一个在线协作文档平台",
        "开发一个智能家居控制系统"
    ]
    
    print("=== 测试LLM模式 ===")
    try:
        for test_input in test_inputs:
            print(f"\n--- 测试输入: {test_input} ---")
            result_llm = agent.plan_tasks(test_input, output_format="dict")
            print("LLM输出（格式化）:")
            print(format_llm_output(result_llm))
    except Exception as e:
        print(f"LLM测试失败（可能是API key问题）: {e}")

if __name__ == "__main__":
    test_taskplanner_agent()
