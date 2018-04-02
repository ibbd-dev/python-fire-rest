# python-fire-rest
快速包装Rest API服务，参考Google的Python Fire实现

## Example01: 最简单的服务
启动一个简单的服务如下：

```python
#!/usr/bin/env python
from fireRest import API, run

class Example:
    def hello(self, name='world'):
        return 'Hello {name}!'.format(name=name)

def main():
    fireRest.API(Example)
    fireRest.run(debug=True)

if __name__ == '__main__':
    main()
```

以上代码在运行之后，就会启动一个http的服务，默认监听端口为`20920`，可以如下访问：

```sh
curl -XPOST localhost:20920/Example/hello -d '{
    name: "hello"
}'
```

其中，Example是类名，hello是函数的名字，函数的参数通过`json`的格式传递。其接口返回值就是函数的返回值。


## Example02: 以json的格式返回
很简单，基于Example01的基础上，只要使用output_json进行返回即可，如下：

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

## Example03: 多个控制器


```python
from fireRest import API, run, output_json

class Example:
    def hello(self, name='world'):
        return output_json('Hello {name} in Example!'.format(name=name))

class Example2:
    def hello(self, name='world'):
        return output_json('Hello {name} in Example2!'.format(name=name))

def main():
    API(Example)
    API(Example2)
    run(debug=True)

if __name__ == '__main__':
    main()
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

