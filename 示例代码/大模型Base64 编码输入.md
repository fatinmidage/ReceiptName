如果你要传入的图片/视频在本地, 你可以将这个其转化为 Base64 编码, 然后提交给大模型。下面是一个简单的示例代码。

> **注意**
>
> 传入 Base64 编码格式时, 请遵循以下规则:
>
> *   传入的是图片:
>     *   格式遵循 `data:image/<图片格式>;base64,<Base64编码>` , 其中, 图片格式详细见图片格式说明。
>     *   图片格式: `jpeg` 、 `png` 、 `gif` 等, 支持的图片格式详细见图片格式说明。
>     *   Base64 编码: 图片的 Base64 编码。
> *   转入的是视频:
>     *   格式遵循 `data:video/<视频格式>;base64,<Base64编码>` , 其中, 视频格式详细见视频格式说明。
>     *   视频格式: `MP4` 、 `AVI` 等, 支持的视频格式详细见视频格式说明。
>     *   Base64 编码: 视频的 Base64 编码。

```python
import base64
import os
# 通过 pip install volcengine-python-sdk[ark] 安装方舟SDK
from volcenginesdkarkruntime import Ark

# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(
    api_key=os.getenv('ARK_API_KEY'),
    )

# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 需要传给大模型的图片
image_path = "path_to_your_image.jpg"

# 将图片转为Base64编码
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  # 替换 <MODEL> 为模型的Model ID
  model="<MODEL>",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
          # 需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
          # PNG图片："url":  f"data:image/png;base64,{base64_image}"
          # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
          # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
            "url":  f"data:image/<IMAGE_FORMAT>;base64,{base64_image}"
          },         
        },
        {
          "type": "text",
          "text": "图片里讲了什么?",
        },
      ],
    }
  ],
)

print(response.choices[0])
```

# 控制视觉理解的精细度

控制图片理解的精细度 (指对画面的精细): `image_pixel_limit` 、 `detail` 字段, 2个字段若同时配置, 则生效逻辑如下:

*   生效优先级: `image_pixel_limit` 高于 `detail` 字段, 即同时配置 `image_pixel_limit` 与 `detail` 字段时, 生效 `image_pixel_limit` 字段配置**。**
*   缺省时逻辑: `image_pixel_limit` 字段未设置, 则使用 `detail` (默认值为 `low` ) 设置配置。此时 `image_pixel_limit` 字段的值对应的 `min_pixels` 值 `3136` **** / `max_pixels` 值 `1048576` 。

下面分别介绍如何通过 `detail` 、 `image_pixel_limit` 控制视觉理解的精度。

## 通过 `detail` 字段 (图片理解)

你可以通过 `detail` 参数来控制模型理解图片的精细度, 以及返回速度, 计费公式请参见token 用量说明。

*   `low` : “低分辨率”模式, 处理速度会提高, 适合图片本身细节较少或者只需要模型理解图片大致信息或者对速度有要求的场景。此时 `min_pixels` 取值 `3136` 、 `max_pixels` 取值 `1048576` , 超出此像素范围且小于3600w px的图片 (超出3600w px 会直接报错) 将会等比例缩放至范围内。
*   `high` : “高分辨率”模式, 这代表模型会理解图片更多的细节, 图像细节丰富, 需要关注图片细节的场景。此时 `min_pixels` 取值 `3136` 、 `max_pixels` 取值 `4014080` , 超出此像素范围且小于3600w px的图片 (超出3600w px 会直接报错) 的图片将会等比例缩放至范围内。
*   `auto` : 采用“低分辨率”模式。
*   新版模型 ( `doubao-1.5-vision-pro-32k-250115` 及以后版本): 采用 `low` 模式。
*   旧版模型 ( `doubao-vision-pro-32k-241028` 、 `doubao-vision-lite-32k-241025` ): 根据图片分辨率, 自行选择模式。

```python
import os
# 可通过 pip install volcengine-python-sdk[ark] 安装方舟SDK 
from volcenginesdkarkruntime import Ark

# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(
    api_key=os.getenv('ARK_API_KEY'),
    )

# 调用 Ark 客户端的 chat.completions.create 方法创建聊天补全请求
response = client.chat.completions.create(
    # 替换 <MODEL> 为模型的Model ID
    model="<MODEL>",
    messages=[
        {
            # 消息角色为用户
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 第一张图片链接及细节设置为 high
                    "image_url": {
                        # 您可以替换图片链接为您的实际图片链接
                        "url":  "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png",
                        "detail": "high"
                    }
                },
                # 文本类型的消息内容，询问图片里有什么
                {"type": "text", "text": "图片里有什么？"},
            ],
        }
    ],
)

print(response.choices[0])
```

## 通过 `image_pixel_limit` 结构体

控制传入给方舟的图像像素大小范围, 如果不在此范围, 则会等比例放大或者缩小至该范围内, 后传给模型进行理解。您可以通过 `image_pixel_limit` 结构体, 精细控制模型可理解的图片像素多少。对应结构体如下:

Bash
```bash
"image_pixel_limit": {
    "max_pixels": 3014080,   # 图片最大像素
    "min_pixels": 3136       # 图片最小像素
}
```

示例代码如下:

```python
import os
# 可通过 pip install volcengine-python-sdk[ark] 安装方舟SDK 
from volcenginesdkarkruntime import Ark

# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(
    api_key=os.getenv('ARK_API_KEY'),
    )

# 调用 Ark 客户端的 chat.completions.create 方法创建聊天补全请求
response = client.chat.completions.create(
    # 替换 <MODEL> 为模型的Model ID
    model="<MODEL>",
    messages=[
        {
            # 消息角色为用户
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 第一张图片链接及细节设置为 high
                    "image_url": {
                        # 您可以替换图片链接为您的实际图片链接
                        "url":  "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png",
                        "image_pixel_limit": {
                            "max_pixels": 3014080,
                            "min_pixels": 3136,
                        },
                    }
                },
                # 文本类型的消息内容，询问图片里有什么
                {"type": "text", "text": "图片里有什么？"},
            ],
        }
    ],
)

print(response.choices[0])
```