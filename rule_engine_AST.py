class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # 'operator' or 'operand'
        self.left = left
        self.right = right
        self.value = value  # Value for operand nodes, e.g., condition


# Helper function to parse conditions like "age > 30"
def parse_condition(condition):
    if '>' in condition:
        attribute, value = condition.split('>')
        return attribute.strip(), '>', value.strip()
    elif '<' in condition:
        attribute, value = condition.split('<')
        return attribute.strip(), '<', value.strip()
    elif '=' in condition:
        attribute, value = condition.split('=')
        return attribute.strip(), '==', value.strip().strip("'")  # Handle string comparisons
    return None


# Function to create the AST from a rule string
def create_rule(rule_string):
    operators = ['AND', 'OR']
    
    for operator in operators:
        if operator in rule_string:
            left_side, right_side = rule_string.split(operator, 1)
            left_node = create_rule(left_side.strip())
            right_node = create_rule(right_side.strip())
            return Node(type='operator', left=left_node, right=right_node, value=operator)
    
    # If no operators found, treat it as an operand
    return Node(type='operand', value=rule_string)


# Function to combine multiple rule ASTs
def combine_rules(rules):
    if not rules:
        return None
    if len(rules) == 1:
        return rules[0]
    
    combined = rules[0]
    for rule in rules[1:]:
        combined = Node(type='operator', left=combined, right=rule, value='OR')
    return combined


# Function to evaluate the AST against user data
def evaluate_rule(ast_node, data):
    if ast_node.type == 'operand':
        return eval_operand(ast_node.value, data)
    elif ast_node.type == 'operator':
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result


# Helper function to evaluate an operand like "age > 30"
def eval_operand(condition, data):
    parsed = parse_condition(condition)
    if parsed is None:
        raise ValueError(f"Invalid condition: {condition}")

    attribute, operator, value = parsed
    if attribute not in data:
        raise KeyError(f"Attribute '{attribute}' not found in data.")
    
    # Safely evaluate the expression
    return eval(f"{data[attribute]} {operator} {value}")


# Example usage
if __name__ == "__main__":
    # Test data - Rule 1
    rule1_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    
    # Test data - Rule 2
    rule2_string = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
    
    # Create AST for Rule 1
    rule1_ast = create_rule(rule1_string)
    print("AST for Rule 1 created.")

    # Create AST for Rule 2
    rule2_ast = create_rule(rule2_string)
    print("AST for Rule 2 created.")

    # Combine Rule 1 and Rule 2 into a single AST
    combined_ast = combine_rules([rule1_ast, rule2_ast])
    print("Combined AST created for Rule 1 and Rule 2.")

    # Test Data 1 - Should match Rule 1
    test_data_1 = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }

    # Test Data 2 - Should match Rule 2
    test_data_2 = {
        "age": 32,
        "department": "Marketing",
        "salary": 25000,
        "experience": 4
    }

    # Test Data 3 - Should NOT match any rule
    test_data_3 = {
        "age": 22,
        "department": "Sales",
        "salary": 15000,
        "experience": 2
    }

