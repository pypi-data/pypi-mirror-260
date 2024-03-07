# BigZhu(z) Shell (ll)

我的 ssh 命令行辅助登录工具

记录 ssh 登录信息, 显示列表并协助登录

为了安全只支持密钥登录, 剔除记录密码并登录的功能

## install

```bash
pip install zll
```

## 使用

输入以下三种类型均可, 优先级别按顺序匹配

- a 添加要登录主机信息
- q 退出
- 输入序列直接登录
- 输入主机 hostname 或者 ip 关键字匹配搜索
