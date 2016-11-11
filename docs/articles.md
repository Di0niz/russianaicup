# Описание алгортитма

## Основная идея алгоритма

использование агента с набором состояния

```python
def simple_problem_solving_agent(percept):

  state = updateState(state,action,percept)
  rule = ruleMatch(states, rules)
  
  action = ruleAction(rule)
  
  return action
  
```


# Используемые материалы
