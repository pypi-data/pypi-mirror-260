def dict_contain_key(source_dict, target_key):
    """
    判断 dict 是否包含某个元素
    source_dict 包含 target_key, 返回 True
    """
    try:
        if source_dict is not None and source_dict.__contains__(target_key) is True:
            if source_dict[target_key] is not None and source_dict[target_key] != '':
                return True
    except Exception as e:
        print(str(e))
    return False
