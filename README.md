# 介绍
这是一个基于scrapy实现的猫眼电影爬虫项目，该项目主要爬取网页中的电影，影院，以及院线信息
# 使用
运行start_cinema.py / startMaoYan.py启动爬虫项目，修改main中的setting实现自定义存储位置
运行save_in2_mysql.py实现数据存储进入数据库,使用前需配置数据库信息

在settings.py的pryxy_list中添加IP地址，可以实现在爬取失败或验证码检测时自动切换IP

# 补充
电影票价格信息网站采用了动态字体加密，由于个人需求不高，该信息使用随机数生成，如需破解加密，在网页源码中搜寻stonefont可以找到加密字体的网址。

电影的相关信息请求采用了MD5加密，逆向方法在method.py中
