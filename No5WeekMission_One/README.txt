选课系统：
角色:学校、学员、课程、讲师
要求:
1. 创建北京、上海 2 所学校
2. 创建linux , python , go 3个课程 ， linux\py 在北京开， go 在上海开
3. 课程包含，周期，价格，通过学校创建课程
4. 通过学校创建班级， 班级关联课程、讲师
5. 创建学员时，选择学校，关联班级
5. 创建讲师角色时要关联学校，
6. 提供两个角色接口
6.1 学员视图， 可以注册，先选择班级, 再交学费
6.2 讲师视图， 讲师可管理自己的班级， 上课时选择班级， 查看班级学员列表 ， 修改所管理的学员的成绩
6.3 管理视图，创建讲师， 创建学校，创建班级，创建课程
7. 上面的操作产生的数据都通过pickle序列化保存到文件l里

任务进展:
基本写完：学员视图功能，讲师视图功能，管理员视图功能

操作指南：
1、管理员功能：
    1.1：创建学校
        管理员手动输入学校名称，随意创建，系统自动判断是否有重复校区创建(全名匹配)
    1.2：创建班级
        管理员首先输入学校全名,如果学校不存在则无法创建班级，如果学校存在则继续，根据需求，创建班级时要管理课程、讲师
        在输入课程和讲师时，如果有课程和讲师没有创建的则要先进行1.3和1.4分别创建讲师和课程。班级没有创建讲师和课程时，会将对应位置保持空，班级主体
        会创建好，更新班级数据库
    1.3：创建讲师
        管理员首先输入学校全名，如果学校不存在则无法创建讲师，如果学校存在则继续，根据需求，创建讲师时关联学校，并且要先判断讲师是否自己有在系统中
        注册过。
    1.4：创建课程
        管理员首先输入学校全名，如果学校不存在则无法创建课程，如果学校存在则继续，根据需求，创建课程时要录入学习周期，学费信息
2、普通用户功能：
    2.1：学员功能
        2.1.1：注册功能
            学员登陆，系统判断是否有注册过，没有注册过，提示进行注册流程
        2.1.2：选课
            注册完成后再次通过注册账号登陆系统后可进行：学员先要选在校区，如果校区不存在提示无法选课，校区存在继续，手动输入要选择的课程，
            判断课程是否在该校区创建过，如果没创建提示无法选课，如果创建了继续，提示是否缴费，选择Y后，将学员缴费注册标识置一，后续不准再次选课！
        2.1.3：查看成绩
            学员可登陆自己账号查看自己的在校区的成绩
    2.2：讲师功能
        2.2.1：上课选班
            讲师上课的时候可以根据系统已经录入好的班级信息进行班级选择
        2.2.2：查看班级学员
            讲师可选择查看班级学员基本信息
        2.2.3：评测
            讲师可以给学员打分
