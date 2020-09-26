

###	初学web注入试写sql注入小工具

####	共有两个版本：手动版和自动版

自动版是get方式自动攻击靶场（sqli-labs）1-10

包括了联合查询、报错注入、盲注（折半查询）

会自动判断注入方式

有python3环境的话，cmd 打开控制台 输入 pytho空格 然后把文件拖进去就可以执行

####	手动版使用指南:

每一关自动选择注入方式   之后会弹出以下选择

请输入指令:
1.查询database()
2.查询指定数据库名所有表名
3.查询指定表下的所有字段名
4.查询指定表下字段及对应的信息
5.一键查询用户名和密码
0.退出



####	注意：1、5、0 是不需要用户额外输入。2,3,4需要额外输入

```2
2
请输入要查询的数据库名:security
..
emails,referers,uagents,users

security
```

//////////////////我是图片//////////////////

<img src="C:\Users\libaobao\AppData\Roaming\Typora\typora-user-images\image-20200926134137605.png" alt="image-20200926134137605" style="float: left; zoom: 50%;" />

//////////////////我是图片//////////////////

```2
3
请输入要查询的表名:users
..

id,username,password
users
```



//////////////////我是图片//////////////////

<img src="C:\Users\libaobao\AppData\Roaming\Typora\typora-user-images\image-20200926133350076.png" alt="image-20200926133350076" style="float: left; zoom: 67%;" />

//////////////////我是图片//////////////////



```2
4
请输入要查询的表名:users
请输入要查询的字段1:username
请输入要查询的字段2:password
..
Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4

```

//////////////////我是图片//////////////////

<img src="C:\Users\libaobao\AppData\Roaming\Typora\typora-user-images\image-20200926134318042.png" alt="image-20200926134318042" style="float: left; zoom: 50%;" />

//////////////////我是图片//////////////////