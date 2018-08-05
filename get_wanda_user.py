import sqlite3

conn = sqlite3.connect('/Users/demon/Desktop/userdata.db')
c = conn.cursor()
# 获取区域
cursor = c.execute("select DeptId, CnDeptName from DeptInfoTb where PId = '3822'")
# 遍历区域
for row in cursor:
    DeptId = row[0]
    CnDeptName = row[1]
    # 获取具体广场
    guangchang_c = conn.cursor()
    guangchang_sql = "select DeptId, CnDeptName from DeptInfoTb where PId = '%s'" % DeptId
    guangchang = guangchang_c.execute(guangchang_sql)
    for guangchang_row in guangchang:
        guangchang_DeptId = guangchang_row[0]
        guangchang_CnDeptName = guangchang_row[1]
        # 获取具体广场下的部门
        dep_c = conn.cursor()
        dep_sql = "select DeptId, CnDeptName from DeptInfoTb where PId = '%s'" % guangchang_DeptId
        dep = dep_c.execute(dep_sql)
        for dep_row in dep:
            dep_DeptId = dep_row[0]
            dep_CnDeptName = dep_row[1]
            # 获取具体部门下的人员信息
            user_c = conn.cursor()
            user_sql = "select udit.CnUserName, uit.Post, uit.Phone from UserDeptInfoTb udit left join UserInfoTb uit on udit.UserId = uit.UserId where udit.DeptId = '%s'" % dep_DeptId
            user = user_c.execute(user_sql)
            for user_row in user:
                user_CnUserName = user_row[0]
                user_Post = user_row[1]
                user_Phone = user_row[2]
                if user_Phone is None:
                    continue
                print(
                    CnDeptName + "," + guangchang_CnDeptName + "," + dep_CnDeptName + "," + user_CnUserName + "," + user_Post + "," + user_Phone)
