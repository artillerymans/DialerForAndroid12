# DialerForAndroid12

#### 介绍
Dialer android 12L 移植到AS中运行的项目

基于分支: android-12.1.0_r24

我修改的地方:
1.删除了定位的LocationFragment模块
2.所有的android.supper 转成了 androidx

当前存在的问题:
我没法完整测试,手上没有设备,无法push到system内部成为系统App,所以我现在看到的是部分没有权限导致闪退