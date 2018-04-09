# python-fire-rest
快速包装Rest API服务，参考Google的Python Fire实现

说明：在Python3.5下测试通过。

## Install

```sh
python setup.py install
```

## Usage
假设你实现的函数名是：`func_name`，将它封装成http服务如下：

```python
from fireRest import API, run

API(func_name)        # 将func_name这个函数包装成服务
run(debug=True)       # 启动
```

这样就启动了一个http服务，默认端口号为`20920`，访问地址为：`localhost:20920/func_name`，接口参数使用post方式提交，json格式。例如如下：

```sh
curl -XPOST localhost:20920/func_name -d '{
    name: "hello"
}'
```

如果需要改用其他的端口，可以使用run函数的port参数，例如：`run(port=8080)`，这样就将端口改成了8080。

同理也可以将一个类包装成HTTP服务，例如：

```python
from fireRest import API, run

API(class_name)       # 将class_name这个类包装成服务
run(debug=True)       # 启动
```

使用上和函数基本一样，只是访问的地址变为：`localhost:20920/class_name/action_name`，这里的`action_name`指定访问方法的名字。

另外，还可以也可以将多个函数或者多个类封装成http接口，具体可以看下面的Example。

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
#!/usr/bin/env python
from fireRest import API, run

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
    run(debug=True)   # 启动
```

以上代码在运行之后，就会启动一个http的服务，默认监听端口为`20920`，可以如下访问：

```sh
curl -XPOST localhost:20920/hello -d '{
    name: "hello"
}'
```

其中，hello是函数的名字，函数的参数通过`json`的格式传递。其接口返回值就是函数的返回值。

### 查看函数的帮助文档
对于上面的函数hello，如果想查询其帮助文档，只需要在请求的url上增加`help=true`参数即可，例如可以在浏览器上直接打开该地址：`localhost:20920/hello?help=true`

其输入如下：

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
from fireRest import API, run

class Example:
    def hello(self, name='world'):
        return 'Hello {name}!'.format(name=name)

if __name__ == '__main__':
    API(Example)
    run(debug=True)
```

访问也类似，只需要加上相应的类名：

```sh
curl -XPOST localhost:20920/Example/hello -d '{
    name: "hello"
}'
```

这样就能访问到Example类的hello方法了。

说明：查询帮助文档的方式也是类似。

## Example03: 以json的格式返回
很简单，基于Example02的基础上，只要使用output_json进行返回即可，如下：

```python
from fireRest import API, run, output_json

class Example:
    def hello(self, name='world'):
        return output_json('Hello {name}!'.format(name=name))
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
from fireRest import API, run, output_json

class Example:
    def hello(self, name='world'):
        return output_json('Hello {name} in Example!'.format(name=name))

class Example2:
    def hello(self, name='world'):
        return output_json('Hello {name} in Example2!'.format(name=name))

if __name__ == '__main__':
    API(Example)
    API(Example2)
    run(debug=True)
```

分别执行以下两个命令就能看到不同的输出：

```sh
# 执行Example中的方法
curl -XPOST localhost:20920/Example/hello -d '{
    name: "hello"
}'

# 执行Example2中的方法
curl -XPOST localhost:20920/Example2/hello -d '{
    name: "hello"
}'
```

## TODO

- [x] 帮助文档完善
- [ ] 函数参数类型校验
- [x] API版本信息
