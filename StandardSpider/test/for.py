def div_list(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = int(ls_len / n)
        k = ls_len % n
        ### j,j,j,...(前面有n-1个j),j+k  
        # 步长j,次数n-1
        ls_return = []
        for i in range(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
            # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


if __name__ == "__main__":
    print(div_list([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 3))
