
def node_function_1(data, multiplier, data_manager) -> int:
   
    some_data = data_manager.get_jetline_data("Name")
    
    result = data * multiplier * some_data
    return result


def node_function_2(data, offset) -> int:
   
   
    result = data + offset
    return result
