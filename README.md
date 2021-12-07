# Samueli924/TeenStudy 青春湖北(青年大学习)

## 使用方法

### 第一步 准备代码需要的数据

#### 1.1 抓取微信公众号的openid

	openid是微信每个独立的公众号对于用户的一个唯一标识,在后续代码中用于身份认证

<b>获取步骤(Fiddler抓包)<b>  

	1.1.1 自行配置好Fiddler后开始抓包  

	1.1.2 打开公众号登录页面  

![Snipaste_2021-12-07_13-53-30](https://user-images.githubusercontent.com/65054820/144975543-8377215c-0c08-4548-8e28-b73f1db64c24.png)  
	
	1.1.3 在Fiddler抓包页面中找到这个请求  
![Snipaste_2021-12-07_13-54-00](https://user-images.githubusercontent.com/65054820/144975566-35ea335d-8c7b-4174-88ca-9f2daff6555a.png)  

	1.1.4 在请求详情中可以看到你的独立openid
![Snipaste_2021-12-07_14-00-37](https://user-images.githubusercontent.com/65054820/144975584-f723a842-6eea-4296-804a-bcc8cdcf85e1.png)  

	1.1.5 复制你的openid，保存到本地，稍后需要用到  
	
----

#### 1.2 openid
