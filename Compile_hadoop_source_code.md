# Hadoop源码编译
## jar包准备
- hadoop-3.2.1-src.tar.gz(项目需求，需要hadoop3.0以上版本)
- jdk-8u201-linux-x64.tar.gz 
- apache-ant-1.9.9-bin.tar.gz(在package中已包括)
- apache-maven-3.3.3-bin.tar.gz(在package中已包括)
- protobuf-2.5.0.tar.gz(在package中已包括)
- cmake-3.11.4.tar.gz(在package中已包括)
## jar包安装(建议全程在root模式下进行)
> JDK解压、配置环境变量 JAVA_HOME和PATH，验证java-version
> 我使用的jdk包为jdk 1.8.0_201 [下载地址](https://www.oracle.com/java/technologies/javase-java-archive-javase8-downloads.html)
>
> ```
>  tar -zxf jdk-8u201-linux-x64.tar.gz 
>  vi /etc/profile 
> ```
>
> 在profile文件中末尾加入
>
> ```
> export JAVA_HOME=[jdk解压路径]/jdk1.8.0_201
> export PATH=$PATH:$JAVA_HOME/bin
> ```
>
> ```
> source /etc/profile
> ```
>
> 验证命令： java -version

> Maven 解压、配置 MAVEN_HOME和PATH 
>
> 我使用的Maven包为3.3.3版本
>
> ```
> wget https://archive.apache.org/dist/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
> tar -zxvf apache-maven-3.3.3-bin.tar.gz
> vi /etc/profile
> ```
>
> 在profile文件中末尾加入
>
> ```
> export MAVEN_HOME=[maven解压路径]/apache-maven-3.3.3
> export PATH=$PATH:$MAVEN_HOME/bin
> ```
>
> ```
> source /etc/profile
> ```
>
> 验证命令：mvn -version
>
> **在后续安装过程中，遇到多mvn找不到的情况，需要重新source /etc/profile，目前原因并不了解**

> ant 解压、配置 MAVEN_HOME和PATH 
>
> 我使用的ant包为1.9.9版本
>
> ```
> tar -zxvf apache-ant-1.9.9-bin.tar.gz
> vi /etc/profile
> ```
>
> 在profile文件中末尾加入
>
> ```
> export ANT_HOME=[ant解压路径]/apache-ant-1.9.9
> export PATH=$PATH:$ANT_HOME/bin
> ```
>
> ```
> source /etc/profile
> ```
>
> 验证命令：ant -version

> 安装glibc-headers 和 g++命令
>
> ```
> apt-get install build-essential
> apt-get install gcc g++
> ```

> 安装cmake
>
> ```
> tar xzvf cmake-3.11.4.tar.gz
> cd cmake-3.11，4
> ./bootstrap
> make
> make install
> ```
>
> 验证命令：cmake --version

> 解压protobuf
>
> **protobuf一定需要2.5.0版本，因为版本不对重新安装过一次**
>
> ```
> tar -zxvf protobuf-2.5.0.tar.gz
> cd protobuf-2.5.0
> ./configure
> make
> make check
> make install
> ldconfig
> ```
>
> 在profile文件中末尾加入
>
> ```
> export PROTO_PATH=[protobuf-2.5.0解压路径]/protobuf-2.5.0
> export PATH=$PATH:$PROTO_PATH
> ```
>
> ```
> source /etc/profile
> ```
>
> 验证命令： protoc --version

> 在Ubuntu下安装openssl库
>
> ```
> 1、下载
> wget https://www.openssl.org/source/openssl-1.0.2h.tar.gz
> 2、解压
> tar zxf openssl-1.0.2h.tar.gz
> 3、安装
> cd openssl-1.0.2h
> ./config shared zlib
> 4、
> make
> make install
> mv /usr/bin/openssl /usr/bin/openssl.bak
> mv /usr/include/openssl /usr/include/openssl.bak
> ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
> ln -s /usr/local/ssl/include/openssl /usr/include/openssl
> echo “/usr/local/ssl/lib” >> /etc/ld.so.conf
> ldconfig -v
> 5、检测安装是否成功
> openssl version -a
> ```

> 在Ubuntu下安装 Ncurses 库
>
> ```
> sudo apt-get install libncurses5-dev libncursesw5-dev
> ```

到此，编译工具基本安装完成

## 编译源码

1、解压源码

```2、进入到hadoop源码主目录
 tar -zxvf hadoop-3.2.1-src.tar.gz
```

2、进入到hadoop源码主目录

```
 cd hadoop-3.2.1-src
```

 3、通过maven执行编译命令（本步极易出现问题）

```
mvn package -Pdist,native -DskipTests -Dtar
```

需要根据ERROR内容进行合理的处理，本步等待时间月30分钟左右，最终成功时全部Success

4、成功安装的hadoop在hadoop-3.2.1-scr/hadoop-dist/target中

**参考内容**

- [编译Hadoop源码全流程讲解]( https://blog.csdn.net/qq_26442553/article/details/78695624 )
- [安装openssl和openssl-devel](https://blog.csdn.net/thanklife/article/details/55097429)
- [如何在 Linux 中安装 Ncurses 库](https://linux.cn/article-9693-1.html?pr)
- [对Hadoop源码进行编译](https://blog.csdn.net/qq_42694416/article/details/84668711#ProtocolBuffer_250_31)

