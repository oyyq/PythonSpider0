import requests
from scrapy import Selector
from models import *
from datetime import datetime as dtime
import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed
import httpx


# headers = {
# 'origin': 'https://bbs.csdn.net',
# 'referer': 'https://bbs.csdn.net/forums/GamesDevelop?category=2',
# 'sec-ch-ua-mobile': '?0',
# 'sec-fetch-dest': 'empty',
# 'sec-fetch-mode': 'cors',
# 'sec-fetch-site': 'same-site',
# 'x-ca-key': '203899271',
# 'x-ca-nonce': '502f4d1f-77d8-477f-8ae8-6465f0732458',
# 'x-ca-signature': 'dHHWZox7cHKVPpWQrztXwhkNK27V35BqHOOEhG2Go9g=',
# 'x-ca-signature-headers': 'x-ca-key,x-ca-nonce'
# }

# res = requests.get('https://bizapi.csdn.net/community-cloud/v1/homepage/community/by/tag?deviceType=PC&tagId=1', headers=headers)
# print(res.text)


tag1 = {"code":200,"msg":"ok","message":"ok","data":[{"id":227,"tagName":"C#","url":"https://bbs.csdn.net/forums/CSharp","avatarUrl":"https://img-community.csdnimg.cn/avatar/a7b2a15d77ba47b6968a126366232f4f.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":211,"tagName":".NET技术社区","url":"https://bbs.csdn.net/forums/DotNET","avatarUrl":"https://img-community.csdnimg.cn/avatar/282f575123174474b214c64e76f83bd0.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":315,"tagName":"C语言","url":"https://bbs.csdn.net/forums/C","avatarUrl":"https://img-community.csdnimg.cn/avatar/cd06246cb9df4d5c81b23f7b20057bca.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":164,"tagName":"C++ 语言","url":"https://bbs.csdn.net/forums/CPPLanguage","avatarUrl":"https://img-community.csdnimg.cn/avatar/83a82941223c42dbaa3a5002b7138676.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":223,"tagName":"数据结构与算法","url":"https://bbs.csdn.net/forums/ST_Arithmetic","avatarUrl":"https://img-community.csdnimg.cn/avatar/d3186ee4f5614520ba2adc50f637aa21.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":132,"tagName":"汇编语言","url":"https://bbs.csdn.net/forums/ASM","avatarUrl":"https://img-community.csdnimg.cn/avatar/0d544d419d624d2a96cdf43c7fa0b83e.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":161,"tagName":"Java","url":"https://bbs.csdn.net/forums/JavaOther","avatarUrl":"https://img-community.csdnimg.cn/avatar/5c1c09171f7341999c41e44f163c4c7c.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":163,"tagName":"脚本语言(Perl/Python)","url":"https://bbs.csdn.net/forums/OL_Script","avatarUrl":"https://img-community.csdnimg.cn/avatar/9918604df5e24641a4c80d542bcb991a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":185,"tagName":"Apache","url":"https://bbs.csdn.net/forums/Apache","avatarUrl":"https://img-community.csdnimg.cn/avatar/b71ccd87fe29466f99f49bfee8dcf11e.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":137,"tagName":"VB","url":"https://bbs.csdn.net/forums/VB","avatarUrl":"https://img-community.csdnimg.cn/avatar/431d96d262c2448ca2e0d4d9d418b08a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":125,"tagName":"PHP","url":"https://bbs.csdn.net/forums/php","avatarUrl":"https://img-community.csdnimg.cn/avatar/cc5e4fe8f177499588cb75b2298ba739.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":133,"tagName":"数据库开发","url":"https://bbs.csdn.net/forums/HPDatabase","avatarUrl":"https://img-community.csdnimg.cn/avatar/f78af391b64d471982ec33ad7624ddf9.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":80,"tagName":"Python全栈技术社区","url":"https://bbs.csdn.net/forums/python","avatarUrl":"https://img-community.csdnimg.cn/avatar/824ac3b3e5d04a25ae338c8e3b2bbb70.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":268,"tagName":"C++ Builder","url":"https://bbs.csdn.net/forums/BCBBase","avatarUrl":"https://img-community.csdnimg.cn/avatar/3ca1c66e94c14f789b1ddeaf74b08829.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":319,"tagName":"Ruby/Rails","url":"https://bbs.csdn.net/forums/ROR","avatarUrl":"https://img-community.csdnimg.cn/avatar/df8120e1c6ec4052a24be3b62037cac6.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":144,"tagName":".NET技术其他语言","url":"https://bbs.csdn.net/forums/DotNET_Other","avatarUrl":"https://img-community.csdnimg.cn/avatar/27275c2258fb4e41a3f47cd4eeadb060.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":188,"tagName":"Delphi","url":"https://bbs.csdn.net/forums/DelphiVCL","avatarUrl":"https://img-community.csdnimg.cn/avatar/0863b3b6b8774fe5b2e8bc593dbf652a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":342,"tagName":"Swift","url":"https://bbs.csdn.net/forums/swift","avatarUrl":"https://img-community.csdnimg.cn/avatar/d75e25c1f0aa44978b86d5890ba15227.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":330,"tagName":"go语言","url":"https://bbs.csdn.net/forums/golang","avatarUrl":"https://img-community.csdnimg.cn/avatar/1f71ef51f8c24dda83a9ccf56286e3b4.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":201,"tagName":"OpenCL和异构编程","url":"https://bbs.csdn.net/forums/Heterogeneous","avatarUrl":"https://img-community.csdnimg.cn/avatar/29d70093e82c422aa2eef8bf60280465.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":134,"tagName":"CUDA","url":"https://bbs.csdn.net/forums/CUDA_Dev","avatarUrl":"https://img-community.csdnimg.cn/avatar/0c1273c0e2ca42df81e694d0c87e2082.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":88,"tagName":"10x Rust","url":"https://bbs.csdn.net/forums/rust","avatarUrl":"https://img-community.csdnimg.cn/avatar/978bb103daed41839952b2a7479acd01.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag2 = {"code":200,"msg":"ok","message":"ok","data":[{"id":298,"tagName":"游戏开发","url":"https://bbs.csdn.net/forums/GamesDevelop","avatarUrl":"https://img-community.csdnimg.cn/avatar/caa6b41b74ec47f7a37b28459b3056fc.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":360,"tagName":"Unity3D","url":"https://bbs.csdn.net/forums/GD_Unity3D","avatarUrl":"https://img-community.csdnimg.cn/avatar/1bd3d7830db84409b6dcbbfadcf914cb.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":359,"tagName":"Cocos2d-x","url":"https://bbs.csdn.net/forums/GD_Cocos2d-x","avatarUrl":"https://img-community.csdnimg.cn/avatar/161bcebdf6b7455f8acd3f35d251354e.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":362,"tagName":"游戏策划与运营","url":"https://bbs.csdn.net/forums/Gdesignoperation","avatarUrl":"https://img-community.csdnimg.cn/avatar/bf09f6082fce4018bd8e6fe9e303790d.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag3 = {"code":200,"msg":"ok","message":"ok","data":[{"id":209,"tagName":"JavaScript","url":"https://bbs.csdn.net/forums/JavaScript","avatarUrl":"https://img-community.csdnimg.cn/avatar/ca46c476a908476d9927eaee4b0afc10.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":126,"tagName":"CSS","url":"https://bbs.csdn.net/forums/HTMLCSS","avatarUrl":"https://img-community.csdnimg.cn/avatar/34450b38a2f048c8a5e780c51b36fb79.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":326,"tagName":"HTML5","url":"https://bbs.csdn.net/forums/HTML5","avatarUrl":"https://img-community.csdnimg.cn/avatar/a3a3e28849de4fdfaa5d9b402e5ecd92.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":230,"tagName":"XML/XSL","url":"https://bbs.csdn.net/forums/XMLSOAP","avatarUrl":"https://img-community.csdnimg.cn/avatar/60a37c831f5649b780f7d8a656fba7bb.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":168,"tagName":"IIS","url":"https://bbs.csdn.net/forums/IIS","avatarUrl":"https://img-community.csdnimg.cn/avatar/5ddc0816d49847bc914bdcdb4309bb17.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":273,"tagName":"CGI","url":"https://bbs.csdn.net/forums/CGI","avatarUrl":"https://img-community.csdnimg.cn/avatar/78db63eae7174f9688ea7f23bd0910d0.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":314,"tagName":"ColdFusion","url":"https://bbs.csdn.net/forums/ColdFusion","avatarUrl":"https://img-community.csdnimg.cn/avatar/230ed309fb954988b77a1ffda56a6cf9.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":420,"tagName":"VUE","url":"https://bbs.csdn.net/forums/vue","avatarUrl":"https://img-community.csdnimg.cn/avatar/961925a75f8e42e0b19f03045c2f4a13.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag4 = {"code":200,"msg":"ok","message":"ok","data":[{"id":139,"tagName":"Hadoop","url":"https://bbs.csdn.net/forums/hadoop","avatarUrl":"https://img-community.csdnimg.cn/avatar/6c81cbd3a337478eb7a2e911019868cb.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":266,"tagName":"云安全","url":"https://bbs.csdn.net/forums/ST_Security","avatarUrl":"https://img-community.csdnimg.cn/avatar/ff96c4df098d41d38f04837650e32744.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":336,"tagName":"云存储","url":"https://bbs.csdn.net/forums/CloudStorage","avatarUrl":"https://img-community.csdnimg.cn/avatar/d4f9c4eafa9d4c5684b5078c6b204c99.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":410,"tagName":"涛思数据TDengine官方社区","url":"https://bbs.csdn.net/forums/tdengine","avatarUrl":"https://img-community.csdnimg.cn/avatar/48bde994d4cc4cdab49c0ddc24459a64.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":274,"tagName":"Cloud Foundry","url":"https://bbs.csdn.net/forums/CloudFoundry","avatarUrl":"https://img-community.csdnimg.cn/avatar/b5c4b893f5cc484b81fa9d615940fff2.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":333,"tagName":"数据运维","url":"https://bbs.csdn.net/forums/server","avatarUrl":"https://img-community.csdnimg.cn/avatar/839255bc06154167b9022594691c8e8f.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":341,"tagName":"Spark","url":"https://bbs.csdn.net/forums/spark","avatarUrl":"https://img-community.csdnimg.cn/avatar/1e7810b22ffe45958516f9006ecd39d3.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":343,"tagName":"Docker","url":"https://bbs.csdn.net/forums/docker","avatarUrl":"https://img-community.csdnimg.cn/avatar/04137b708ccd4085a4916432fec915fa.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":345,"tagName":"华为云计算","url":"https://bbs.csdn.net/forums/huaweicloud","avatarUrl":"https://img-community.csdnimg.cn/avatar/fd3be0d599b8465989bd471fb3a026a4.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":331,"tagName":"AWS","url":"https://bbs.csdn.net/forums/AWS","avatarUrl":"https://img-community.csdnimg.cn/avatar/f05331a772c94390a175af84fba468ba.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":332,"tagName":"GAE","url":"https://bbs.csdn.net/forums/GAE","avatarUrl":"https://img-community.csdnimg.cn/avatar/3c5744442dbf43e7adbf8c5ac3c208ad.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":348,"tagName":"云计算","url":"https://bbs.csdn.net/forums/hwfsdeveloper","avatarUrl":"https://img-community.csdnimg.cn/avatar/8ff1ca7179c041be87e94858070db828.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag6 = {"code":200,"msg":"ok","message":"ok","data":[{"id":29,"tagName":"TensorFlow 社区","url":"https://bbs.csdn.net/forums/tensorflow","avatarUrl":"https://img-community.csdnimg.cn/avatar/d5ba9ceb46be4481a898b70a64864acd.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":33,"tagName":"飞桨PaddlePaddle","url":"https://bbs.csdn.net/forums/paddlepaddle","avatarUrl":"https://img-community.csdnimg.cn/avatar/cd9a309f1bf043c58b926cea356ffeaf.png"},{"id":131,"tagName":"机器视觉","url":"https://bbs.csdn.net/forums/ST_Image","avatarUrl":"https://img-community.csdnimg.cn/avatar/8de40427e76448a8ad8320bbcc666d3a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":372,"tagName":"OpenCV","url":"https://bbs.csdn.net/forums/OpenCV","avatarUrl":"https://img-community.csdnimg.cn/avatar/d8ff3c664bcc4b8e9a99098c8d709101.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":413,"tagName":"自然语言处理(NLP)","url":"https://bbs.csdn.net/forums/nlp","avatarUrl":"https://img-community.csdnimg.cn/avatar/de2743426204446d9a7718062cca4532.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":386,"tagName":"VR/AR","url":"https://bbs.csdn.net/forums/vrar","avatarUrl":"https://img-community.csdnimg.cn/avatar/5e79abde59d84c83afa953f6459acbc1.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":422,"tagName":"OPEN AI LAB开放智能","url":"https://bbs.csdn.net/forums/Tengine","avatarUrl":"https://img-community.csdnimg.cn/avatar/1695272992d44c689254d493f5f78eef.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag8 = {"code":200,"msg":"ok","message":"ok","data":[{"id":297,"tagName":"通信技术","url":"https://bbs.csdn.net/forums/ST_Network","avatarUrl":"https://img-community.csdnimg.cn/avatar/7fd91304e7da4bb2be2293fef16416ac.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":151,"tagName":"交换及路由技术","url":"https://bbs.csdn.net/forums/Hardware_SwitchRouter","avatarUrl":"https://img-community.csdnimg.cn/avatar/3c1b8863f014418086707a7349f45bb4.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":192,"tagName":"VoIP","url":"https://bbs.csdn.net/forums/voip","avatarUrl":"https://img-community.csdnimg.cn/avatar/f3841b3b01e1474281140afeb64a0706.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":364,"tagName":"网络协议与配置","url":"https://bbs.csdn.net/forums/IP_Protocolconfiguration","avatarUrl":"https://img-community.csdnimg.cn/avatar/6984c531ca344af3b3d076f31602f849.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":365,"tagName":"网络维护与管理","url":"https://bbs.csdn.net/forums/maintainmanage","avatarUrl":"https://img-community.csdnimg.cn/avatar/5fc60a28c9784f3caf96e8b3a405df36.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":384,"tagName":"智能路由器","url":"https://bbs.csdn.net/forums/IR","avatarUrl":"https://img-community.csdnimg.cn/avatar/3431be8e66b54e3d978aa9b25da7b48b.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":366,"tagName":"CDN","url":"https://bbs.csdn.net/forums/NetworkC_CDN","avatarUrl":"https://img-community.csdnimg.cn/avatar/4f058fa0ad8c447a9bbf6a3709a96077.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag9 = {"code":200,"msg":"ok","message":"ok","data":[{"id":279,"tagName":"嵌入开发(WinCE)","url":"https://bbs.csdn.net/forums/WinCE","avatarUrl":"https://img-community.csdnimg.cn/avatar/57cd9aa6ebf84c4484c897ff22fa4f9e.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":199,"tagName":"硬件相关讨论专区","url":"https://bbs.csdn.net/forums/HardwareUse","avatarUrl":"https://img-community.csdnimg.cn/avatar/f19d128865ff423f932f6e43e05c27b8.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":251,"tagName":"电脑整机及配件","url":"https://bbs.csdn.net/forums/Hardware_Computer","avatarUrl":"https://img-community.csdnimg.cn/avatar/f101019c088c489684179fcbce610d4a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":244,"tagName":"VxWorks","url":"https://bbs.csdn.net/forums/VxWorks","avatarUrl":"https://img-community.csdnimg.cn/avatar/a1672356c1b0475bac2066ef6531b803.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":294,"tagName":"数码设备","url":"https://bbs.csdn.net/forums/Hardware_Digital","avatarUrl":"https://img-community.csdnimg.cn/avatar/3861ee71c1004a5ea20b76c8b2ae723f.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":329,"tagName":"智能硬件","url":"https://bbs.csdn.net/forums/SmartHardware","avatarUrl":"https://img-community.csdnimg.cn/avatar/ab69442965f345d3811b61d638198091.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":411,"tagName":"极术公开课","url":"https://bbs.csdn.net/forums/aijishu","avatarUrl":"https://img-community.csdnimg.cn/avatar/60f53b0bedaf42fd84f3df160f4040be.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag11 = {"code":200,"msg":"ok","message":"ok","data":[{"id":243,"tagName":"Android","url":"https://bbs.csdn.net/forums/Android","avatarUrl":"https://img-community.csdnimg.cn/avatar/3589160dfe4546b8bb89f43819f07f40.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":152,"tagName":"iOS","url":"https://bbs.csdn.net/forums/ios","avatarUrl":"https://img-community.csdnimg.cn/avatar/b4d635c8a8bc486f82274e7b97a643df.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":313,"tagName":"移动广告","url":"https://bbs.csdn.net/forums/MobileAD","avatarUrl":"https://img-community.csdnimg.cn/avatar/3b67a0711e474da5b28a35b6c4bc870a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":344,"tagName":"微信开发","url":"https://bbs.csdn.net/forums/weixin","avatarUrl":"https://img-community.csdnimg.cn/avatar/a69a400c6ca14690acda59ea069dfb83.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag12 = {"code":200,"msg":"ok","message":"ok","data":[{"id":123,"tagName":"Windows客户端使用","url":"https://bbs.csdn.net/forums/Windows7","avatarUrl":"https://img-community.csdnimg.cn/avatar/33ba40ba4b1c4296b12b9bb7335a0fc0.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":293,"tagName":"安全技术/病毒","url":"https://bbs.csdn.net/forums/WindowsSecurity","avatarUrl":"https://img-community.csdnimg.cn/avatar/a2c28e1aee3647beba6d15a5d2e330d9.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":130,"tagName":"WPF/Silverlight","url":"https://bbs.csdn.net/forums/Silverlight","avatarUrl":"https://img-community.csdnimg.cn/avatar/9ddd71aca26e43868e1df1ff53089c5d.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":127,"tagName":"VC/MFC","url":"https://bbs.csdn.net/forums/VC_Basic","avatarUrl":"https://img-community.csdnimg.cn/avatar/349f6169dd2d4f2c9b404f74e1744fb8.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":138,"tagName":"Windows客户端开发","url":"https://bbs.csdn.net/forums/WindowsMobile","avatarUrl":"https://img-community.csdnimg.cn/avatar/3bd92056efb643689ad008cd6fd50a14.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":242,"tagName":"Windows Server","url":"https://bbs.csdn.net/forums/WinNT2000XP2003","avatarUrl":"https://img-community.csdnimg.cn/avatar/a71b8ac69c1c4f3a8d181605ae27c235.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":221,"tagName":"windows网络管理与配置","url":"https://bbs.csdn.net/forums/NetworkConfiguration","avatarUrl":"https://img-community.csdnimg.cn/avatar/6eed68a2635c4b1385dfdc0d7a4c6c57.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":259,"tagName":"一般软件使用","url":"https://bbs.csdn.net/forums/WindowsBase","avatarUrl":"https://img-community.csdnimg.cn/avatar/ebafbaed924a4be6abd99c65ab7a295d.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag14 = {"code":200,"msg":"ok","message":"ok","data":[{"id":305,"tagName":"软件测试","url":"https://bbs.csdn.net/forums/SE_Quality","avatarUrl":"https://img-community.csdnimg.cn/avatar/5b3bd78b1668451098abe57058982104.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":194,"tagName":"设计模式","url":"https://bbs.csdn.net/forums/DesignPatterns","avatarUrl":"https://img-community.csdnimg.cn/avatar/3db570280be64ca69b5736a24f6d5195.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":423,"tagName":"构建之法","url":"https://bbs.csdn.net/forums/SoftwareEngineering","avatarUrl":"https://img-community.csdnimg.cn/avatar/d4d803f641ee496fa944aaddefeec625.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":210,"tagName":"版本控制","url":"https://bbs.csdn.net/forums/CVS_SVN","avatarUrl":"https://img-community.csdnimg.cn/avatar/0aa0ac3626da4c209a415e41b3275ee1.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":157,"tagName":"研发管理","url":"https://bbs.csdn.net/forums/SE_Management","avatarUrl":"https://img-community.csdnimg.cn/avatar/604dad74385544f7bd2fea4ec419593e.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":424,"tagName":"Autosar中文社区","url":"https://bbs.csdn.net/forums/autosar","avatarUrl":"https://img-community.csdnimg.cn/avatar/4eca0484c4f543888f042d614e1def6c.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag16 = {"code":200,"msg":"ok","message":"ok","data":[{"id":34,"tagName":"HarmonyOS技术社区","url":"https://bbs.csdn.net/forums/harmonyos","avatarUrl":"https://img-community.csdnimg.cn/avatar/3065baa3d0bf46f5ac557b2fb7cda287.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":282,"tagName":"Linux/Unix社区","url":"https://bbs.csdn.net/forums/Linux_Development","avatarUrl":"https://img-community.csdnimg.cn/avatar/81196fc56b964e648565e92a2093c869.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":226,"tagName":"Web开发应用服务器","url":"https://bbs.csdn.net/forums/WebAppServer","avatarUrl":"https://img-community.csdnimg.cn/avatar/97b84714f6f948358f517925176600eb.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":141,"tagName":"Linux_Kernel","url":"https://bbs.csdn.net/forums/Linux_Kernel","avatarUrl":"https://img-community.csdnimg.cn/avatar/b16e38a3f33c4d6abfafd54648304111.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag18 = {"code":200,"msg":"ok","message":"ok","data":[{"id":186,"tagName":"MySQL","url":"https://bbs.csdn.net/forums/MySQL","avatarUrl":"https://img-community.csdnimg.cn/avatar/5ccaf5d8403f42c7b9a804234ad81c77.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":302,"tagName":"MS-SQL Server","url":"https://bbs.csdn.net/forums/MSSQL_Basic","avatarUrl":"https://img-community.csdnimg.cn/avatar/db13a8bbc42a48ce93c67e94237e250c.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":124,"tagName":"Access","url":"https://bbs.csdn.net/forums/Access","avatarUrl":"https://img-community.csdnimg.cn/avatar/fe901a65cd8b4f888bfeb57d81aba4cb.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":140,"tagName":"Oracle","url":"https://bbs.csdn.net/forums/Oracle_Develop","avatarUrl":"https://img-community.csdnimg.cn/avatar/8805c625786b44df96c1a9fef9f7d757.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":181,"tagName":"MongoDB","url":"https://bbs.csdn.net/forums/MongoDB","avatarUrl":"https://img-community.csdnimg.cn/avatar/a812e126a8774ba8b28ffef532a8a5a9.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":396,"tagName":"PostgreSQL","url":"https://bbs.csdn.net/forums/PostgreSQL","avatarUrl":"https://img-community.csdnimg.cn/avatar/743eafb901594663b01db755d2c5c818.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":431,"tagName":"Gauss松鼠会","url":"https://bbs.csdn.net/forums/gaussdb","avatarUrl":"https://img-community.csdnimg.cn/avatar/7b9f375d81f94e95b6aa20ba8cfe4bd6.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":328,"tagName":"Informatica","url":"https://bbs.csdn.net/forums/DataIntegration","avatarUrl":"https://img-community.csdnimg.cn/avatar/f3223517c36145d0992e8c75627478b1.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":380,"tagName":"Greenplum","url":"https://bbs.csdn.net/forums/Greenplum","avatarUrl":"https://img-community.csdnimg.cn/avatar/b1c72c0de58f4b83b06a2efe5f102e70.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
tag19 = {"code":200,"msg":"ok","message":"ok","data":[{"id":175,"tagName":"ERP/CRM","url":"https://bbs.csdn.net/forums/ERP","avatarUrl":"https://img-community.csdnimg.cn/avatar/ccb921e23bff407daa0219a516eafd1b.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":252,"tagName":"消息协作","url":"https://bbs.csdn.net/forums/ExchangeServer","avatarUrl":"https://img-community.csdnimg.cn/avatar/bdf3eefd2847486b9b960afdbd6b3725.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":176,"tagName":"英特尔边缘计算技术","url":"https://bbs.csdn.net/forums/intel","avatarUrl":"https://img-community.csdnimg.cn/avatar/1221b941092b44379c97b5443ed3eb09.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":338,"tagName":"Qualcomm开发","url":"https://bbs.csdn.net/forums/qualcomm","avatarUrl":"https://img-community.csdnimg.cn/avatar/bb4bae0b2e2948bd9a2f1fe0fc33c196.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":340,"tagName":"Xamarin技术","url":"https://bbs.csdn.net/forums/Xamarin","avatarUrl":"https://img-community.csdnimg.cn/avatar/265b1f87b84148bb9ed1fcf4cc8b8b3a.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":339,"tagName":"T客","url":"https://bbs.csdn.net/forums/tcl","avatarUrl":"https://img-community.csdnimg.cn/avatar/b80e5d94e41c413b87373674b4e472cc.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":337,"tagName":"Atlassian技术","url":"https://bbs.csdn.net/forums/atlassian","avatarUrl":"https://img-community.csdnimg.cn/avatar/526c1308ff33463e8f955fdab4ad84f5.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":347,"tagName":"联通WO+开放平台","url":"https://bbs.csdn.net/forums/chinaunicom","avatarUrl":"https://img-community.csdnimg.cn/avatar/fc89144a43e343afb036ab67ab14672f.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":421,"tagName":"企业级低代码开发","url":"https://bbs.csdn.net/forums/cosmic","avatarUrl":"https://img-community.csdnimg.cn/avatar/7ee461f454b54356bf7973ff1bbe2bf4.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":369,"tagName":"JetBrains技术论坛","url":"https://bbs.csdn.net/forums/JetBrains","avatarUrl":"https://img-community.csdnimg.cn/avatar/43eab18eccef4779b63f78e3c4d8744f.png?x-oss-process=image/resize,m_fixed,h_88,w_88"},{"id":371,"tagName":"FusionInsight HD","url":"https://bbs.csdn.net/forums/fusioninsightdeveloper","avatarUrl":"https://img-community.csdnimg.cn/avatar/6226486827724542b17b0374e4e721e2.png?x-oss-process=image/resize,m_fixed,h_88,w_88"}]}
#taglist = [tag1, tag2, tag3, tag4, tag6, tag8, tag9, tag11, tag12, tag14, tag16, tag18, tag19]

taglist = [tag1]

# 每篇帖子的回答都提取出来了
answers_ext = [ False for i in range(len(taglist)) ]
# 每篇帖子的作者信息都提取出来了
author_ext = [ False for i in range(len(taglist)) ]

answer_queue = Queue()
author_queue = Queue()


feed_thpool = ThreadPoolExecutor(max_workers=2)
ans_thpool = ThreadPoolExecutor(max_workers=2)
auth_thpool = ThreadPoolExecutor(max_workers=2)
ans_model_thpool = ThreadPoolExecutor(max_workers=2)
auth_model_thpool = ThreadPoolExecutor(max_workers=2)
All_Tasks = []


# 提取所有子标签的url
def extract_urls(tag):
    category_urls = {}
    datas = tag['data']
    for data in datas:
        category = data['tagName']
        url = data['url']
        category_urls[category] = url

    return category_urls


# 提取贴详情和帖子的回答
def extract_topicinfo(category_urls, cate_index):
    feed_sels = []
    feed_text_list = []
    topic_ids = []
    total_rep_times = []
    total_rep_counts = []
    total_browses = []
    total_categories = []
    total_urls = []

    for item in category_urls.items():
        print(item)
        category = item[0]
        url = item[1]
        res = requests.get(url)
        html = res.text
        sel = Selector(text=html)

        feed_urls = sel.xpath("//div[@class='textBox m-bottom']/a[@class='item-desc-wrap']/@href | //a[@href and (@class='long-text-title')]/@href").extract()
        rep_times = sel.xpath("//span[@class='cop-p']/text()").extract()
        browses = sel.xpath("//div[@class='handle-item item-scan']//span[@class='num ']/text()").extract()
        rep_counts = sel.xpath("//div[@class='handle-item comments item-report']//span[@class='num ']/text()").extract()
        assert len(feed_urls) == len(rep_counts) == len(rep_times) == len(browses)

        for feed_url in feed_urls:
            index = feed_urls.index(feed_url)
            feed_id = int(feed_url.split('/')[-1])
            feed_detail = requests.get(feed_url).text
            feed_text_list.append(feed_detail)
            topic_ids.append(feed_id)

            total_rep_times.append(rep_times[index])
            total_rep_counts.append(rep_counts[index])
            total_browses.append(browses[index])
            total_categories.append(category)

            feed_sel = Selector(text=feed_detail)
            feed_sels.append(feed_sel)
            total_urls.append(feed_url)

    #提交解析每篇帖的回答的任务
    # task = ans_thpool.submit(extract_feed_answers, feed_text_list, topic_ids, index)
    # All_Tasks.append(task)


    # 抽取帖子信息并存储
    # print("抽取帖子信息 {}".format(cate_index))
    for feed_sel in feed_sels:
        index = feed_sels.index(feed_sel)
        #print("topic {}".format(topic_ids[index]))
        titles = feed_sel.xpath("//div[@class='item-title']//h1")
        feed_title = ''
        feed_content = ''

        if len(titles) > 0:
            feed_title = feed_sel.xpath("//div[@class='item-title']//h1/text()").extract()[0]
            feed_contents = feed_sel.xpath("//div[@id='blogDetail2']/p/text() | //div[@id='blogDetail2']/p/img/@src").extract()
        else:
            feed_contents = feed_sel.xpath("//div[@class='item-title']/span[@class='item-desc']/text()").extract()


        feed_content = ' '.join(feed_contents)
        try:
            author_name = feed_sel.xpath("//div[@class='user-title flex align-center']//span[@class='name']/text()").extract()[0]
        except: print(total_urls[feed_sels.index(feed_sel)])
        #create_time = feed_sel.xpath("//div[@class='user-title flex align-center']//span[@class='cop-p']/text()").extract()[0]

        # topic = Topic.create(id=topic_ids[index], category = total_categories[index],  title=feed_title, content=feed_content, author=author_name,
        #                      answer_nums=int(0 if total_rep_counts[index] == '回复' else total_rep_counts[index]),
        #                      browse_nums=int(total_browses[index]))
        #
        # topic.answer_time = dtime.strftime(parse_timestr(total_rep_times[index]), '%Y-%m-%d')  # 赋str类型
        # topic.create_time = create_time  # 赋str类型
        # topic.save()
        #print("存储topic {}".format(topic_ids[index]))

    extract_feed_answers(feed_text_list, topic_ids, cate_index)




# 只提取一级回复, 不提取次级及以下回复.
def extract_feed_answers(feed_text_list, topic_ids, cate_index):
    # print("抽取回答信息 {}".format(cate_index))
    feed_sels = []
    author_urls = []

    for feed_text in feed_text_list:
        feed_sel = Selector(text=feed_text)
        feed_sels.append(feed_sel)
        feed_author = feed_sel.xpath("//div[@class='user-card']/div[1]/a[@href]/@href").extract()[0]
        author_urls.append(feed_author)

    #提交提取作者信息任务
    # task = auth_thpool.submit(extract_authorinfo, author_urls, index)
    # All_Tasks.append(task)

    #将提取到的回复放入queue
    for feed_sel in feed_sels:
        raw_contents = feed_sel.xpath(
            "//div[@class='comment-main']//div[@class='comment-msg']//span[@id and @class='text rich-text blog-content-box htmledit_views markdown_views']")

        answer_contents = []
        answer_ids = feed_sel.xpath("//div[@class='comment-item']//span[@id and @class='text rich-text blog-content-box htmledit_views markdown_views']/@id").extract()             # 'text-value(id)'
        answer_ids = [id[5:] for id in answer_ids]
        answer_times = feed_sel.xpath("//div[@class='Comment']/div[@class='comment-box']/div[@class='commentMsg']/div/div[@class='comment-item']/div[@class='comment-box']/div[@class='comment-main']/div[@class='user-msg']//span[@class='time']/text()").extract()
        answer_authors = feed_sel.xpath("//div[@class='Comment']/div[@class='comment-box']/div[@class='commentMsg']/div/div[@class='comment-item']/div[@class='comment-box']/div[@class='comment-main']/div[@class='user-msg']//span[@class='name']/a[@class='name']/text()").extract()
        answer_praisednums = feed_sel.xpath("//div[@class='Comment']/div[@class='comment-box']/div[@class='commentMsg']/div/div[@class='comment-item']/div[@class='comment-box']/div[@class='comment-main']/div[@class='comment-msg']/div[contains(@class, 'user-operate')]/span[contains(@class, 'love')]/span/text()").extract()

        for content_sel in raw_contents:
            contents = content_sel.xpath("./p/text() | ./text()").extract()
            answer_contents.append(''.join(contents))


        assert len(answer_ids) == len(answer_times) == len(answer_authors) == len(answer_praisednums) == len(answer_contents)

        for i in range(len(answer_ids)):
            ans_dict = {}
            ans_dict['id'] = int(answer_ids[i])
            ans_dict['topicid'] = topic_ids[feed_sels.index(feed_sel)]
            ans_dict['content'] = answer_contents[i]
            ans_dict['author'] = answer_authors[i]
            ans_dict['create_time'] = dtime.strftime(parse_timestr(answer_times[i]), '%Y-%m-%d %H-%M-%S')
            ans_dict['praise'] = int(answer_praisednums[i]) if answer_praisednums[i] != '赞' else 0
            answer_queue.put(ans_dict)


    answers_ext[cate_index] = True
    extract_authorinfo(author_urls, cate_index)




# 将'x天前', 'xx小时前', 'xx分钟前' 'MM-DD', 'YYYY-MM-DD' 转换成 'YYYY-MM-DD'格式, return datetime.date类型
def parse_timestr(timestr):
    if('前' in timestr):
        days = 0
        if '天' in timestr:
            days = int(timestr[0:len(timestr) - 2])

        now = datetime.date.today()
        prev = now - datetime.timedelta(days)
        # pstr = str(prev.year)+'-'+ \
        #        (str(prev.month) if prev.month > 10 else '0'+str(prev.month)) +'-' \
        #        + (str(prev.day) if prev.day > 10 else '0'+str(prev.day))
        return prev

    else:
        ymd = timestr.split('-')
        today = datetime.date.today()

        #time = datetime.datetime.strptime('', '%Y-%m-%d')
        # time = datetime.datetime.today()
        if len(ymd) == 3:
            # tstr = ymd[0] + '-' + (ymd[1] if len(ymd[1]) == 2 else '0' + ymd[1]) + '-' + \
            #        (ymd[2] if len(ymd[2]) == 2 else '0' + ymd[2])
            time = datetime.datetime.strptime(ymd[0] +'-'
                                              + (ymd[1] if len(ymd[1]) == 2 else '0' + ymd[1]) + '-' + \
                                               (ymd[2] if len(ymd[2]) == 2 else '0' + ymd[2]),
                                              '%Y-%m-%d')
        elif len(ymd) == 2:
            # now = datetime.datetime.now()
            # tstr = str(now.year)+'-' + (ymd[0] if len(ymd[0]) == 2 else '0'+ymd[0]) +'-' + \
            #        (ymd[1] if len(ymd[1]) == 2 else '0' + ymd[1])
            time = datetime.datetime.strptime('2020-' +
                                              (ymd[0] if len(ymd[0]) == 2 else '0'+ymd[0]) +'-' + \
                                            (ymd[1] if len(ymd[1]) == 2 else '0' + ymd[1]),
                                              '%Y-%m-%d')

        return time




# 提取作者信息
def extract_authorinfo(author_urls, cate_index):
    #print("抽取作者信息 {}".format(index))
    for url in author_urls:

        author_detail = httpx.Client(http2=True).get(url).text
        author_sel = Selector(text=author_detail)
        id = url.split('/')[-1]
        try:
            name = author_sel.xpath("//div[@class='user-profile-head-name']/div[1]/text()").extract()[0]
        except:
            name = id
            print(url)
        try:
            avatar = author_sel.xpath("//div[@class='user-profile-avatar']/img/@src").extract()[0]
        except:
            avatar = ''
        try:
            desc = author_sel.xpath("//div[@class='user-profile-head-introduction']/p/text()").extract()[0]
        except:
            desc = ''
        try:
            click_num = author_sel.xpath("//div[@class='user-profile-head-info-b']/ul/li[1]//div[contains(@class, 'user-profile-statistics-num')]/text()").extract()[0]
        except: click_num = 0
        try:
            origin_num = author_sel.xpath("//div[@class='user-profile-head-info-b']/ul/li[2]//div[contains(@class, 'user-profile-statistics-num')]/text()").extract()[0]
        except: origin_num = 0
        try:
            rank = author_sel.xpath("//div[@class='user-profile-head-info-b']/ul/li[3]//div[contains(@class, 'user-profile-statistics-num')]/text()").extract()[0]
        except: rank = '暂无'
        try:
            fans_num = author_sel.xpath("//div[@class='user-profile-head-info-b']/ul/li[4]//div[contains(@class, 'user-profile-statistics-num')]/text()").extract()[0]
        except: fans_num = 0
        try:
            praised_num = author_sel.xpath("//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[1]/div/span/text()").extract()[0]
        except: praised_num = 0
        try:
            comment_num = author_sel.xpath("//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[2]/div/span/text()").extract()[0]
        except: comment_num = 0
        try:
            favor_num = author_sel.xpath("//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[3]/div/span/text()").extract()[0]
        except: favor_num = 0


        auth_dic ={}
        auth_dic['id'] = id
        auth_dic['name'] = name
        auth_dic['avatar'] = avatar
        auth_dic['desc'] = desc
        auth_dic['click'] = click_num
        auth_dic['origin'] = origin_num
        auth_dic['rank'] = rank
        auth_dic['fans'] = fans_num
        auth_dic['praised'] = praised_num
        auth_dic['comment'] = comment_num
        auth_dic['favor'] = favor_num

        author_queue.put(auth_dic)

    author_ext[cate_index] = True


saving_thpool = ThreadPoolExecutor(max_workers=2)
def save_authors(author_queue):
    while True:
        if not author_queue.empty():
            auth_dict = author_queue.get()
            author = Author.create()
            author.id = auth_dict['id']
            author.name = auth_dict['name']
            author.avatar = auth_dict['avatar']
            author.desc = auth_dict['desc']

            author.click_num = parse_string_int(auth_dict['click'])
            author.original_num = auth_dict['origin']
            author.rank = auth_dict['rank']
            author.fans_num = parse_string_int(auth_dict['fans'])
            author.praised_num = parse_string_int(auth_dict['praised'])
            author.comment_num = parse_string_int(auth_dict['comment'])
            author.favor_num = parse_string_int(auth_dict['favor'])

        else:
            if (author_ext[index] == True for index in range(len(taglist))):
                break

    print("SAVE AUTHORS END")


def save_answers(answer_queue):
    while True:
        if not answer_queue.empty():
            ans_dict = answer_queue.get()
            answer = Answer.create()
            answer.id = ans_dict['id']
            answer.topic_id = ans_dict['topicid']
            answer.content = ans_dict['content']
            answer.author = ans_dict['author']
            answer.create_time = ans_dict['create_time']
            answer.praised_nums = ans_dict['praise']
            answer.save()
        else:
            if (answers_ext[index] == True for index in range(len(taglist))):
                break

    print("SAVE ANSWERS END")



# 存储每篇帖子的回答
def parse_string_int(str):
    parts = str.split(',')
    num = 0
    if len(parts) == 1:
        if parts[0] == '暂无':
            return 0
        return int(str)
    else:
        for part in parts:
            num += int(part)*(1000**(len(parts)-1-parts.index(part)))
    return num




if __name__ == '__main__':
    # res = requests.get('https://bbs.csdn.net/topics/600328651')
    # print(res.text)
    #extract_feed_answers(res.text, 123)

    # extract_topicinfo([all_urls[0]])
    # print(type(datetime.datetime.now()))
    # print(dtime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S'))
    # print(type(datetime.datetime.strptime('2021-07-11 16-25-53', '%Y-%m-%d %H-%M-%S')))
    # print(type(dtime.strftime(parse_timestr('2020-07-01'), '%Y-%m-%d')))


    # for tag in taglist:
    #     category_urls = extract_urls(tag)
    #     task = feed_thpool.submit(extract_topicinfo, category_urls, taglist.index(tag))
    #     All_Tasks.append(task)
    #
    # # 2个consumer
    # All_Tasks.append(saving_thpool.submit(save_answers, answer_queue))
    # All_Tasks.append(saving_thpool.submit(save_answers, answer_queue))
    #
    # All_Tasks.append(saving_thpool.submit(save_authors, author_queue))
    # All_Tasks.append(saving_thpool.submit(save_authors, author_queue))
    #
    # wait(All_Tasks, return_when=ALL_COMPLETED)
    # print("FINISH")


    for tag in taglist:
        category_urls = extract_urls(tag)
        #print(category_urls)
        extract_topicinfo(category_urls, taglist.index(tag))
    #
    # save_answers(answer_queue)
    # save_authors(author_queue)




    # HTTP2请求
    # url = 'https://blog.csdn.net/a1589205365'
    # author_detail = ''
    # with httpx.Client(http2=True) as client:
    #     r = client.get(url)
    #     author_detail = r.text
    #
    #
    # author_sel = Selector(text=author_detail)
    # id = url.split('/')[-1]
    # print(id)
    # name = author_sel.xpath("//div[@class='user-profile-head-name']/div[1]/text()").extract()[0]
    # print(name)
    #
    # avatar = author_sel.xpath("//div[@class='user-profile-avatar']/img/@src").extract()[0]
    # print(avatar)
    # try:
    #     desc = author_sel.xpath("//div[@class='user-profile-head-introduction']/p/text()").extract()[0]
    # except:
    #     desc = ''
    # print(desc)
    #
    # click_num = author_sel.xpath(
    #     "//div[@class='user-profile-head-info-b']/ul/li[1]//div[@class='user-profile-statistics-num']/text()").extract()[
    #     0]
    # print(click_num)
    #
    # origin_num = author_sel.xpath(
    #     "//div[@class='user-profile-head-info-b']/ul/li[2]//div[contains(@class,'user-profile-statistics-num')]/text()").extract()[
    #     0]
    # print(origin_num)
    #
    # rank = author_sel.xpath(
    #     "//div[@class='user-profile-head-info-b']/ul/li[3]//div[contains(@class,'user-profile-statistics-num')]/text()").extract()[
    #     0]
    # print(rank)
    #
    # fans_num = author_sel.xpath(
    #     "//div[@class='user-profile-head-info-b']/ul/li[4]//div[@class='user-profile-statistics-num']/text()").extract()[
    #     0]
    # print(fans_num)
    #
    # praised_num = author_sel.xpath(
    #     "//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[1]/div/span/text()").extract()[
    #     0]
    # print(praised_num)
    #
    # comment_num = author_sel.xpath(
    #     "//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[2]/div/span/text()").extract()[
    #     0]
    # print(comment_num)
    #
    # favor_num = author_sel.xpath(
    #     "//div[contains(@class, 'user-achievement')]//div[contains(@class, 'content')]//li[3]/div/span/text()").extract()[
    #     0]
    # print(favor_num)








