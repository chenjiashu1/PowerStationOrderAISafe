import unittest

from module.smart_monitoring.ai_smart_monitoring import extract_markdown_content


class TestExample(unittest.TestCase):
    def test_extract_markdown_content(self):
        content = """```markdown
# 订单数据分析可视化报表

## 1. 订单状态分布
```mermaid
pie
    title Pie Chart
        "Dogs" : 386
        "cats" : 567
        "rabbit" : 700
        "pig":365
        "tiger" : 15
```

```"""
        result =extract_markdown_content(content)
        print(f"result====={result}")

if __name__ == '__main__':
    unittest.main()
