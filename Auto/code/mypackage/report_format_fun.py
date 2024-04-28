def ban_fun(df):
    str_1 = df['告警封禁地區']
    # str_1 = '重庆重庆移动, 北京北京移动, 湖北武汉电信, 山东青岛电信, 重庆重庆联通, 湖北武汉联通, 山东青岛联通, 山东济南联通'  
    if len(str_1) !=0:
        str_1 = str_1.split(', ')

    str_2 = df['有恢復封禁地區']
    # str_2 = '重庆重庆移动, 北京北京移动, 湖北襄阳移动'
    if len(str_2) !=0:
         str_2 = str_2.split(', ')
  
    ban_result = []
    recover_result = []

    for i in str_1:
        if i in str_2:
            ban_result.append(i)
        else:
            recover_result.append(i)

    for j in str_2:
        if j in str_1:
            continue
        else:
             ban_result.append(j)


    ban_finall = ""
    for k in ban_result:
        k += ", " 
        ban_finall += k

    ban_finall = ban_finall[0:-2]

    recover_finall = ""
    for k in recover_result:
        k += ", "
        recover_finall += k

    recover_finall = recover_finall[0:-2]

    return ban_finall


def recover_fun(df):
    str_1 = df['告警封禁地區']
    # str_1 = '重庆重庆移动, 北京北京移动, 湖北武汉电信, 山东青岛电信, 重庆重庆联通, 湖北武汉联通, 山东青岛联通, 山东济南联通'  
    if len(str_1) !=0:
        str_1 = str_1.split(', ')

    str_2 = df['有恢復封禁地區']
    # str_2 = '重庆重庆移动, 北京北京移动, 湖北襄阳移动'
    if len(str_2) !=0:
         str_2 = str_2.split(', ')
  
    ban_result = []
    recover_result = []

    for i in str_1:
        if i in str_2:
            ban_result.append(i)
        else:
            recover_result.append(i)

    for j in str_2:
        if j in str_1:
            continue
        else:
             ban_result.append(j)


    ban_finall = ""
    for k in ban_result:
        k += ", " 
        ban_finall += k

    ban_finall = ban_finall[0:-2]

    recover_finall = ""
    for k in recover_result:
        k += ", "
        recover_finall += k

    recover_finall = recover_finall[0:-2]
    
    return recover_finall
