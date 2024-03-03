


def order_matrix_optimize(columns):
    '''
    Function dùng optimize cho order matrix
    '''
    cumulative_sum = 0
    result = []
    for value in columns:
        cumulative_sum += value
        if cumulative_sum > 1 :
            result.append(0)
            cumulative_sum = 1
        elif cumulative_sum < 0:
            result.append(0)
            cumulative_sum = 0
        elif cumulative_sum in [0,1]:
            result.append(value)
        else:
            result.append(0)
    return result


def sub_conditions_optimize(row,nums = 5):
    '''
    Function dùng để optimize điều kiện phụ cho danh mục đầu tư
    '''
    result = row.rank(ascending=False,method='max',na_option='bottom')
    result = result.apply(lambda x: 1 if x < nums + 1 else 0)
    return result