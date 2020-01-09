# python-fire-rest
快速将多个函数或者类包装Rest API服务，参考[Google的Python Fire](https://github.com/google/python-fire)实现

说明：在Python3.6下测试通过。

## Install

方式一：

```sh
# 安装依赖
pip3 install -r https://github.com/ibbd-dev/python-fire-rest/raw/master/requirements.txt

# 安装
pip3 install git+https://github.com/ibbd-dev/python-fire-rest.git
```

方式二：

```sh
git clone https://github.com/ibbd-dev/python-fire-rest
cd python-fire-rest

# 安装依赖
pip3 install -r requirements.txt

# 源码安装
python setup.py install
```

## Usage
完整的使用案例：[api_test.py](/examples/api_test.py)


假设你实现的函数名是：`func_name`，将它封装成http服务如下：

```python
# app其实就是Flask对象
from fireRest import API, app

API(func_name)            # 将func_name这个函数包装成服务
app.run(port=20920)
```

这样就启动了一个http服务，默认端口号为`20920`，访问地址为：`localhost:20920/func_name`，接口参数使用post方式提交，json格式。例如如下：

```sh
curl -XPOST localhost:20920/func_name -d '{
    "name": "hello"
}'
```

如果需要改用其他的端口，可以使用run函数的port参数，例如：`app.run(port=8080)`，这样就将端口改成了8080。

同理也可以将一个类包装成HTTP服务，例如：

```python
from fireRest import API, app

API(class_name)       # 将class_name这个类包装成服务
app.run(port=20920)
```

使用上和函数基本一样，只是访问的地址变为：`localhost:20920/class_name/action_name`，这里的`action_name`指定访问方法的名字。

另外，还可以也可以将多个函数或者多个类封装成http接口，具体可以看下面的Example。

### 接口的返回值
接口的返回值，默认是以json的格式输出，格式如下：

```json
{
  "code": 0,
  "data": "这里是接口的返回内容，可以是字符串，整数，列表，字典等格式。", 
  "messages": null
}
```

其中：

- code: 接口的请求状态码，0表示成功，非0表示失败
- data: 接口的返回内容，可以是各种类型
- messages: 提示信息，帮助信息等内容


## Help
服务启动之后，查看帮助文档非常简单，只需要在浏览器访问：`localhost:20920`，将会看到如下格式的内容：

```
API Version v1.0

Support Functions:
	/Example/hello	这是Example的hello帮助文档
	/Example2/hello	这是Example2的hello帮助文档

The help of functions:
	/Example/hello?help=true
	/Example2/hello?help=true
```

可以看到接口的版本号，支持的函数列表，以及怎么查看函数的帮助内容等。

## Example01: 最简单的服务
把一个函数包装成HTTP Restful API服务：

```python
from fireRest import API, app

def hello(name='world'):
    """这是帮助函数
    Args:
        name str: 参数

    Returns:
        str
    """
    return 'Hello {name} in func!'.format(name=name)

if __name__ == '__main__':
    API(hello)        # 将hello这个函数包装成服务
    app.run(port=20920)
```

以上代码在运行之后，就会启动一个http的服务，默认监听端口为`20920`，可以如下访问：

```sh
curl -XPOST localhost:20920/hello -d '{
    "name": "hello"
}'
```

其中，hello是函数的名字，函数的参数通过`json`的格式传递。其接口返回值就是函数的返回值。

### 查看函数的帮助文档
对于上面的函数hello，如果想查询其帮助文档，只需要在请求的url上增加`help=true`参数即可，例如可以在浏览器上直接打开该地址：`localhost:20920/hello?help=true`

其输出如下：

```
这是帮助函数
    Args:
        name str: 参数

    Returns:
        str
```

其实输出的就是函数的注释部分

## Example02: 把类包装成服务
除了函数，类也可以包装成API服务:

```python
from fireRest import API, app

class Example:
    def hello(self, name='world'):
        return 'Hello {name}!'.format(name=name)

if __name__ == '__main__':
    API(Example)
    app.run(port=20920)
```

访问也类似，只需要加上相应的类名：

```sh
curl -XPOST localhost:20920/Example/hello -d '{
    "name": "hello"
}'
```

这样就能访问到Example类的hello方法了。

说明：查询帮助文档的方式也是类似。

## Example03: 以json的格式返回
很简单，基于Example02的基础上，只要使用output_json进行返回即可，如下：

```python
from fireRest import API, app, output_json

class Example:
    def hello(self, name='world'):
        return 'Hello {name}!'.format(name=name)
```

返回格式如下：

```json
{
  "code": 0, 
  "data": "Hello world!", 
  "messages": null
}
```

## Example04: 多个控制器


```python
from fireRest import API, app, output_json

class Example:
    def hello(self, name='world'):
        return 'Hello {name} in Example!'.format(name=name)

class Example2:
    def hello(self, name='world'):
        return 'Hello {name} in Example2!'.format(name=name)

if __name__ == '__main__':
    API(Example)
    API(Example2)
    app.run(debug=True)
```

分别执行以下两个命令就能看到不同的输出：

```sh
# 执行Example中的方法
curl -XPOST localhost:20920/Example/hello -d '{
    "name": "hello"
}'

# 执行Example2中的方法
curl -XPOST localhost:20920/Example2/hello -d '{
    "name": "hello"
}'
```

## 异常处理

```python
from fireRest import API, app, APIException, ErrCodeBase

def hello(name='world'):
    if name == 'exception':
        raise APIException('演示错误处理的使用方式',
                           code=ErrCodeBase.err_param)
    return 'Hello {name} in func!'.format(name=name)

if __name__ == '__main__':
    API(hello)
    app.run(debug=True)
```

使用非常简单，只要引入`APIException`类即可。上例演示只要输入的name参数值为`exception`就会触发异常返回，如下：

```sh
curl -XPOST localhost:5000/hello -d '{"name": "exception"}'
{
  "code": 100, 
  "data": null, 
  "messages": "演示错误处理的使用方式"
}
```

说明：实际使用的时候，可以直接使用[`APIException`](/fireRest/exception.py)类，允许自定义错误码。

在异常处理的时候，也可以直接使用内置的Exception，如：

```python
from fireRest import API, app

def hello(name='world'):
    if name == 'exception':
        raise Exception('演示错误处理的使用方式')
    return 'Hello {name} in func!'.format(name=name)

if __name__ == '__main__':
    API(hello)
    app.run(debug=True)
```

返回值：

```sh
curl -XPOST localhost:5000/hello -d '{"name": "exception"}'
{
  "code": 1, 
  "data": null, 
  "messages": "演示错误处理的使用方式"
}
```

## 上传文件
需要上传文件时，可以如下使用

```python
from flask import request

def upload():
    """上传文件
    注意：上传文件时，不能在函数名upload增加参数，否则会报错
    测试：
    files = {'file': open('/path/to/filename', 'rb')}
    res = requests.post(url, files=files).json()
    """
    ufile = request.files.get('file')
    # 你的处理代码在这里。。。
    # ufile就是文件对象，对应表单域中的file
    # 如果需要可以同时传多个文件对象
    print(type(ufile))   # 对象类型：werkzeug.datastructures.FileStorage

    # ufile.stream 获取文件流对象
    img = Image.open(ufile.stream)

    # 保存文件
    ufile.save('/tmp/' + secure_filename('hello.png'))
    ufile.close()
    return {
        "file": ufile.filename,   # 这里只是一个样例返回
        "size": img.size,
        "mode": img.mode,
    }
```

接口请求样例：

```sh
curl -XPOST localhost:5000/upload -F 'file=@README.md'

## 返回值
{
  "code": 0,
  "data": {
    "file": "README.md"
  },
  "messages": null
```

如果需要设置上传文件的大小，可以使用下面的方法：

```python
from fireRest import set_upload_size

set_upload_size(1024*1024*10)     # 10MB
```

## 心跳服务
用于判断服务是否正常运行，用于在外部监控服务是否正常。

```sh
curl localhost:5000/heartbeat
{
  "code": 0,         # 该值为0则表示服务正常
  "messages": ""
}
```

## 图像格式转换函数库
在涉及到图像处理的接口中，经常需要在各种格式之间转换，主要是3种格式之间：

- base64格式
- PIL格式
- cv2格式

例如接口输入输出通常是base64格式，而对图像进行处理时通常是cv2格式或者PIL格式，所以经常需要进行转换。

```python
# PIL格式如base64格式的转换
from fireRest.image import base64_pil, pil_base64

# cv2格式与base64格式的转换
from fireRest.image import base64_cv2, cv2_base64

# cv2格式与PIL格式
from fireRest.image import pil_cv2, cv2_pil
```

还有其他一些图像相关的功能：

- GIF格式转JPG格式
- 计算两个矩形的重叠面积

## 其他功能

- 设置跨域
- 设置上传文件或者请求体的大小
- 设置其他的flask参数

```python
from fireRest import set_cors, set_upload_size, set_param
```


## TODO

- [x] 帮助文档完善
- [x] API版本信息
- [x] 统一的异常处理
- [x] 设置上传大小: set_upload_size(size)
- [x] 设置跨域: set_cors
- [ ] 接口缓存
- [ ] 函数参数类型校验
- [x] 服务心跳服务
- [x] 图像格式转换函数库
