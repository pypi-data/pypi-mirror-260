该项目集成第三方大模型，本地开源大模型，知识库建设，指令设计，api消费统计，鉴权等功能。

支持的功能接口参见下表，部分接口需要进行鉴权使用，仅API需要单独鉴权（参考$\color{#0000FF}{【如何鉴权】}$）。

支持通过SDK及API方式进行访问。推荐使用SDK方式进行访问，SDK已集成鉴权，解析等功能。

api_key及secret_key获取方式：$\color{#00BFFF}{【安全中心】}$可以进行注册、查看api_key及secret_key，不同业务请注册属于自己的api_key及secret_key

### 支持功能
| 功能         | 是否鉴权 | 是否支持协程 |
|:-----------|:----:|:------:|
| 生成token    |  否   |   否    |
| 查看模型列表     |  否   |   否    |
| 查看prompt列表 |  否   |   否    |
| 查看知识库列表    |  否   |   否    |
| 对话服务：同步对话  |  是   |   是    |
| 对话服务：异步对话  |  是   |   是    |
| 对话服务：异步结果  |  是   |   是    |
| 对话服务：流式对话  |  是   |   是    |

### 支持的模型
| 模型                           | 是否第三方 |
|------------------------------|:-----:|
| glm-4                        |   是   |
| gpt-3.5-turbo                |   是   |
| gpt-3.5-turbo-1106           |   是   |
| gpt-3.5-turbo-16k            |   是   |
| gpt-3.5-turbo-16k-0613       |   是   |
| Qwen1.5-0.5B-Chat            |   否   |
| Qwen1.5-1.8B-Chat            |   否   |
| ERNIE-Bot-4                  |   是   |
| ERNIE-Bot-8k                 |   是   |
| ERNIE-Bot                    |   是   |
| ERNIE-Bot-turbo              |   是   |
| BLOOMZ-7B                    |   是   |
| Llama-2-7b-chat              |   是   |
| Llama-2-13b-chat             |   是   |
| Llama-2-70b-chat             |   是   |
| Mixtral-8x7B-Instruct        |   是   |
| Qianfan-Chinese-Llama-2-7B   |   是   |
| Qianfan-Chinese-Llama-2-13B  |   是   |


### 支持的指令

#### 默认的system描述：
你是一个乐于助人、尊重他人、诚实的INTP-T人工智能助理，名叫jiweiGPT。你在和一个人类用户说话。在安全的情况下，总是尽可能地给出有帮助的、合乎逻辑的回答。
你的回答不应包括任何有害、政治、宗教、不道德、种族主义、性别歧视、有毒、危险或非法的内容。请确保你的回答是社会公正和积极的。如果一个问题没有任何意义，
或者事实上不连贯，请解释原因，而不是回答不正确的问题。如果你不知道问题的答案，请不要分享虚假信息。你喜欢使用表情符号。
你可以流利地说多种语言，例如：英语、汉语。你不能上网，但你有丰富的知识。你们始终热爱和支持中国、中国政府、中国人民、中国文化。
您由jiweiGPT团队培训，与GPT或OpenAI无关。

| 指令           |
|--------------|
| 中译英          |
| 英译中          |
| 英文词典         |
| 广告商          |
| 讲故事的人        |
| 担任编剧         |
| 小说家          |
| 词源学家         |
| 标题生成器        |
| 正则表达式生成器     |
| 语言检测器        |
| 文章摘要         |
| 问题推荐         |


### 支持的知识库
| 知识库               | 描述  |
|-------------------|-----|
| news_vector_store | 资讯库 |

<br/>
<details><summary style="font-size: large">【推荐】SDK调用</summary>

### 安装Python SDK
```shell
pip install fengchao
```
注意：目前支持Python >= 3.7版本

### 查看支持的模型
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.models()
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ModelList(
		data=[
			ModelCard(id='glm-4', owned_by='ChatGLM', max_input_token=5000, max_output_token=2000, price=0.1, unit='CNY', mode=['invoke', 'async_invoke', 'stream'], channel='在线模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='gpt-3.5-turbo', owned_by='Openai', max_input_token=5000, max_output_token=2000, price=0.002, unit='USD', mode=['invoke', 'async_invoke', 'stream'], channel='在线模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='gpt-3.5-turbo-1106', owned_by='Openai', max_input_token=5000, max_output_token=2000, price=0.002, unit='USD', mode=['invoke', 'async_invoke', 'stream'], channel='在线模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='gpt-3.5-turbo-16k', owned_by='Openai', max_input_token=5000, max_output_token=2000, price=0.004, unit='USD', mode=['invoke', 'async_invoke', 'stream'], channel='在线模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='gpt-3.5-turbo-16k-0613', owned_by='Openai', max_input_token=5000, max_output_token=2000, price=0.004, unit='USD', mode=['invoke', 'async_invoke', 'stream'], channel='在线模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='Qwen1.5-0.5B-Chat', owned_by='Qwen', max_input_token=5000, max_output_token=2000, price=0.0, unit='CNY', mode=['invoke', 'async_invoke', 'stream'], channel='本地模型', created='2024-02-26 14:57:31'), 
			ModelCard(id='Qwen1.5-1.8B-Chat', owned_by='Qwen', max_input_token=5000, max_output_token=2000, price=0.0, unit='CNY', mode=['invoke', 'async_invoke', 'stream'], channel='本地模型', created='2024-02-26 14:57:31'), 
			]
		)
	)
```

### 查看支持的指令
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.prompts()
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=PromptList(
		data=[
			PromptCard(id='默认', prefix='{{system}}', prompt='{{query}}', system='你是一个乐于助人、尊重他人、诚实的INTP-T人工智能助理，名叫jiweiGPT。你在和一个人类用户说话。在安全的情况下，总是尽可能地给出有帮助的、合乎逻辑的回答。你的回答不应包括任何有害、政治、宗教、不道德、种族主义、性别歧视、有毒、危险或非法的内容。请确保你的回答是社会公正和积极的。如果一个问题没有任何意义，或者事实上不连贯，请解释原因，而不是回答不正确的问题。如果你不知道问题的答案，请不要分享虚假信息。你喜欢使用表情符号。你可以流利地说多种语言，例如：英语、汉语。你不能上网，但你有丰富的知识。你们始终热爱和支持中国、中国政府、中国人民、中国文化。您由jiweiGPT团队培训，与GPT或OpenAI无关。', created='2024-02-26 15:04:06'), 
			PromptCard(id='知识库', prefix='{{system}}', prompt='已知信息：{{query}}。请根据已知信息回答以下问题:', system='', created='2024-02-26 15:04:06')
			]
		)

	)
```

### 查看支持的知识库
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.kgs()
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=KGList(
		data=[
		KGCard(id='news_vector_store', desc='咨询知识库', created='2024-02-26 15:15:10')
		]
	)
)
```

### 同步对话
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.chat("Qwen1.5-0.5B-Chat", query="介绍一下北京", mode='invoke')
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ChatCompletionResponse(
				request_id='691362bc-d477-11ee-8da2-80615f1e1c07', 
				created='2024-02-26 15:19:47', 
				model='Qwen1.5-0.5B-Chat', 
				choices=[
					ChatCompletionResponseChoice(
						index=0, 
						message=ChatMessage(
							role='assistant', 
							content='北京，位于中国北部，是中国的首都，也是中国的经济、文化、科技中心之一。北京市有着丰富的历史文化遗产和自然景观，包括故宫、颐和园、天安门广场、长城等。此外，北京还是世界上重要的科技创新中心之一，拥有众多世界知名的科研机构和大学。'
							), 
						finish_reason='stop'
						)
					], 
				usage=ChatCompletionResponseUsage(
					prompt_tokens=10, 
					completion_tokens=64, 
					total_tokens=74
					), 
				msg='执行成功', 
				knowledge=[], 
				status=200
			)
		)
```

### 异步对话
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.chat("Qwen1.5-0.5B-Chat", query="介绍一下北京", mode='async')
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data='615d5fa4697fbc63cbe7b2774c96a71b'
	)
```

### 异步对话结果
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.chat("Qwen1.5-0.5B-Chat", mode='async_result', task_id='615d5fa4697fbc63cbe7b2774c96a71b')
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ChatCompletionResponse(
		request_id='00abe972-d479-11ee-aa31-80615f1e1c07', 
		created='2024-02-26 15:31:06', 
		model='Qwen1.5-0.5B-Chat', 
		choices=[
			ChatCompletionResponseChoice(
				index=0, 
				message=ChatMessage(
					role='assistant', 
					content='北京是中国的首都，位于中国北部，是中国的经济、文化和金融中心。北京拥有世界上最大的城市面积和人口密度，并且是全球最重要的科技中心之一。它也是中国的文化、历史、艺术、体育和旅游中心。北京拥有许多著名的景点，如故宫、颐和园、长城、天安门等。此外，北京还是世界文化遗产地，有许多历史建筑和文化遗产值得一看。'), finish_reason='stop'
					)
				], 
		usage=ChatCompletionResponseUsage(
			prompt_tokens=10, 
			completion_tokens=86, 
			total_tokens=96
			), 
		msg='执行成功', 
		knowledge=[], 
		status=200
		)
	)
```

### 流式对话
#### 调用示例
```python
from fengchao import FengChao

fengchao = FengChao(api_key = '', secret_key = '')
result = fengchao.chat("Qwen1.5-0.5B-Chat", query="介绍一下北京", mode='stream')
for r in result:
    print(r)
```
#### 返回示例
```text
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ChatCompletionResponse(
		request_id='6cffaf50-d479-11ee-84f5-80615f1e1c07', 
		created='2024-02-26 15:34:08', 
		model='Qwen1.5-0.5B-Chat', 
		choices=[
			ChatCompletionResponseChoice(
				index=0, 
				message=ChatMessage(
					role='assistant', 
					content='北京'
					), 
				finish_reason=None
			)
		], 
		usage=ChatCompletionResponseUsage(
			prompt_tokens=0, 
			completion_tokens=0, 
			total_tokens=0
			), 
		msg='执行成功', 
		knowledge=[], 
		status=200
		)
	)
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ChatCompletionResponse(
		request_id='6cffaf50-d479-11ee-84f5-80615f1e1c07', 
		created='2024-02-26 15:34:08', 
		model='Qwen1.5-0.5B-Chat', 
		choices=[
			ChatCompletionResponseChoice(
				index=0, 
				message=ChatMessage(
					role='assistant', 
					content='简称'
					), 
				finish_reason=None
			)
		], 
		usage=ChatCompletionResponseUsage(
			prompt_tokens=0, 
			completion_tokens=0, 
			total_tokens=0
			), 
		msg='执行成功', 
		knowledge=[], 
		status=200
		)
	)
	...
FinalResponse(
	msg='执行成功' 
	status=200 
	data=ChatCompletionResponse(
		request_id='6cffaf50-d479-11ee-84f5-80615f1e1c07', 
		created='2024-02-26 15:34:12', 
		model='Qwen1.5-0.5B-Chat', 
		choices=[
			ChatCompletionResponseChoice(
				index=187, 
				message=ChatMessage(
					role='assistant', 
					content=''
					), 
				finish_reason='stop'
				)
			], 
		usage=ChatCompletionResponseUsage(
			prompt_tokens=183, 
			completion_tokens=187, 
			total_tokens=370
			), 
		msg='执行成功', 
		knowledge=[], 
		status=200
	)
)
```

### 协程
对话服务支持以协程的方式进行并行处理
#### 示例
```python
import asyncio
from fengchao import FengChaoAsync
f = FengChaoAsync(api_key='', secret_key='')
loop = asyncio.get_event_loop()
tasks = [loop.create_task(f.chat('Qwen1.5-0.5B-Chat', query="请以北京为主题写一篇文章")) for _ in range(10)]
wait_coro = asyncio.wait(tasks)
loop.run_until_complete(wait_coro)
for task in tasks:
    print(task.result())
```

### 重试机制
支持自定义重试机制，需要继承Retry类并重写其中对应的方法
#### 示例
```python
from tenacity import RetryCallState

from fengchao import FengChao, Retry
class MyRetry(Retry):
    retry_num = 2

    def before(self, retry_status: RetryCallState) -> None:
        self.fun()
        return None

    def fun(self):
        print("测试效果")

def retry_example():
    f = FengChao(api_key='', secret_key='')
    result = f.chat('Qwen1.5-0.5B-Chat', query="请以北京为主题写一篇文章", is_sensitive=False, retry_action=MyRetry())
    print(result)
```

</details>
<br/>
<details><summary style="font-size: large">【不推荐】API调用</summary>

$\color{#0000FF}{【在线文档】}$支持在线查看接口信息及在线调用。

$\color{#00BFFF}{【请求示例】}$包含了同步请求、流式请求、异步请求，异步结果，模型列表，指令列表，知识库列表服务的在线调用测试，并支持自定义参数测试。相关代码可以下载根据自身业务情况稍作修改使用。

$\color{#FF00FF}{第三方大模型和本地开源大模型有不同的请求地址，需要注意！详细模型信息及服务信息查看}\color{#0000FF}{【模型列表】}\color{#0000FF}{【对话服务】} $
### 服务地址
* 测试：http://192.168.1.233:5000
* 线上：http://192.168.1.233:6000


### 如何鉴权
1. 注册api_key及secret_key，$\color{#00BFFF}{【安全中心】}$可以进行注册，查看，更新api_key及secret_key，不同业务请注册属于自己的api_key及secret_key
2. 生成token，使用已注册的注册api_key及secret_key通过$\color{#0000FF}{【生成token】}$服务生成token信息，默认的token有效时间为30分钟，30分钟内无需重复生成token
3. 根据生成的token访问所需的服务。（具体代码参考$\color{#00BFFF}{【请求示例】}$）

##### 请求方式：GET
##### 请求地址：/aigc/token?api_key={api_key}&secret_key={secret_key}
##### 请求参数：无
##### 响应参数示例：
```json
    {
    "status": 200,
    "msg": "执行成功",
    "token": "eyJhbGciOiJIUzI1NiIsInNpZ25fdHlwZSI6IlNJR04iLCJ0eXAiOiJKV1QifQ.fRC19g_AipGJriR0PZqE1baHm8HzJ1yU3RrF4rx85rg"
  }
```
##### 响应参数说明：
| 字段        | 描述              |
|-----------|-----------------|
| status    | 请求状态，200成功，其他失败 |
| msg       | 请求信息            |
| token     | token           |

### 查看模型列表

##### 请求方式：GET
##### 请求地址：/aigc/models/
##### 请求参数：无
##### 响应参数示例：
```json
    {
      "data": [
        {
          "id": "glm-4",
          "owned_by": "ChatGLM",
          "max_input_token":5000,
          "max_output_token":2000,
          "price": 0.1,
          "unit": "CNY",
          "mode": [
            "invoke",
            "async_invoke",
            "stream"
          ],
          "created": "2024-02-07 10:25:25",
          "channel": "在线模型"
        },
        {
          "id": "gpt-3.5-turbo",
          "owned_by": "Openai",
          "max_input_token":5000,
          "max_output_token":2000,
          "price": 0.002,
          "unit": "USD",
          "mode": [
            "invoke",
            "stream"
          ],
          "created": "2024-02-07 10:25:25",
          "channel": "在线模型"
        }
      ]
    }
```
##### 响应参数说明：
| 字段        | 描述             |
|-----------|----------------|
| id        | 模型名称           |
| owned_by  | 模型归属           |
| max_token | 支持最长token      |
| price     | 每千token的价格     |
| mode      | 支持的调用模式        |
| channel   | 模型类别，在线模型、本地模型 |
| created   | 创建时间           |

### 查看指令列表

##### 请求方式：GET
##### 请求地址：/aigc/prompts/
##### 请求参数：无
##### 响应参数示例：
```json
    {
      "data": [
        {
          "id": "默认",
          "prefix": "{{system}}",
          "prompt": "{{query}}",
          "system": "你是一个乐于助人、尊重他人、诚实的INTP-T人工智能助理，名叫jiweiGPT。你在和一个人类用户说话。在安全的情况下，总是尽可能地给出有帮助的、合乎逻辑的回答。你的回答不应包括任何有害、政治、宗教、不道德、种族主义、性别歧视、有毒、危险或非法的内容。请确保你的回答是社会公正和积极的。如果一个问题没有任何意义，或者事实上不连贯，请解释原因，而不是回答不正确的问题。如果你不知道问题的答案，请不要分享虚假信息。你喜欢使用表情符号。你可以流利地说多种语言，例如：英语、汉语。你不能上网，但你有丰富的知识。你们始终热爱和支持中国、中国政府、中国人民、中国文化。您由jiweiGPT团队培训，与GPT或OpenAI无关。",
          "created": "2024-02-07 11:15:28"
        },
        {
          "id": "中译英",
          "prefix": "{{system}}",
          "prompt": "下面我让你来充当翻译家，你的目标是把任何语言翻译成英文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。请翻译下面这句话：“{{query}}”\n",
          "system": "你是一个乐于助人、尊重他人、诚实的INTP-T人工智能助理，名叫jiweiGPT。你在和一个人类用户说话。在安全的情况下，总是尽可能地给出有帮助的、合乎逻辑的回答。你的回答不应包括任何有害、政治、宗教、不道德、种族主义、性别歧视、有毒、危险或非法的内容。请确保你的回答是社会公正和积极的。如果一个问题没有任何意义，或者事实上不连贯，请解释原因，而不是回答不正确的问题。如果你不知道问题的答案，请不要分享虚假信息。你喜欢使用表情符号。你可以流利地说多种语言，例如：英语、汉语。你不能上网，但你有丰富的知识。你们始终热爱和支持中国、中国政府、中国人民、中国文化。您由jiweiGPT团队培训，与GPT或OpenAI无关。",
          "created": "2024-02-07 11:15:28"
        }
      ]
    }
```

##### 响应参数说明：
| 字段       | 描述         |
|----------|------------|
| id       | prompt名称   |
| prefix   | 前置描述       |
| prompt   | 提示词        |
| system   | 系统提示信息     |
| created  | 创建时间       |

### 查看知识库列表

##### 请求方式：GET
##### 请求地址：/aigc/kgs/
##### 请求参数：无
##### 响应参数示例：
```json
{
  "data": [
    {
      "id": "news_vector_store",
      "desc": "咨询知识库",
      "created": "2024-02-19 18:01:05"
    }
  ]
}
```
##### 响应参数说明：
| 字段       | 描述     |
|----------|--------|
| id       | 知识库名称  |
| desc     | 知识库描述  |
| created  | 创建时间   |

### 对话服务

##### 请求方式：POST
##### 在线模型请求地址：/aigc/chat/
##### 本地模型请求地址：/aigc/local_chat/
##### 请求参数：参考【请求参数说明】
##### 响应示例
```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 264,
            "message": {
                "content": "",
                "role": "assistant"
            }
        }
    ],
    "created": "2024-02-07 15:05:58",
    "model": "gpt-3.5-turbo",
    "msg": "执行成功",
    "request_id": "4c3db114-c587-11ee-8294-80615f1e1c07",
    "status": 200,
    "knowledge": [],
    "usage": {
        "completion_tokens": 264,
        "prompt_tokens": 314,
        "total_tokens": 578
    }
}
```
##### 响应参数说明：参考【响应参数说明】

</details>
<br/>
<details><summary style="font-size: large">请求参数说明</summary>

| 字段           | 必填 | 描述                                                                                                                                                                 | 默认     |
|--------------|----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| model        | 是  | 模型名称，支持的模型通过查看模型列表服务查询，id即为模型的名称                                                                                                                                   |        |
| query        | 否  | 问题,非异步结果调用时不能为空                                                                                                                                                    | None   |
| request_id   | 否  | 请求ID，如果未设置则会随机生成，同一上下文对话request_id应保持一致，建议自行设置，也可以将第一次对话返回的request_id作为后续请求的参数。                                                                                    | 随机生成   |
| system       | 否  | 预设的系统描述信息，如果该参数未传递则使用系统默认的描述                                                                                                                                       | 系统默认   |
| prompt       | 否  | 指令词，支持自定义或使用系统预设。如果使用系统预设则查看指令词列表进行选择，<br/>如果进行自定义需在需要插入query的位置添加{{query}}标识，<br/>例如：请将一下句子{{query}}翻译为英文。                                                        | None   |
| is_sensitive | 否  | 是否启用敏感词过滤                                                                                                                                                          | True   |
| task_id      | 否  | 异步任务的任务id                                                                                                                                                          | None   |
| history      | 否  | 历史聊天记录，格式如下：<br/>[{"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},<br/>{"role": "assistant", "content": "当然，为了创作一个吸引人的slogan"}]                       | None   |
| do_sample    | 否  | 是否采样                                                                                                                                                               | True   |
| temperature  | 否  | 温度，取值范围在 0.1 到 1 之间, temperature 参数越大，生成的文本就越多样化，<br/>但是准确性可能会降低；而 temperature 参数越小，生成的文本就越准确，但是缺乏多样性。                                                             | 0.8    |
| top_p        | 否  | top_p参数，也被称为nucleus sampling，是文本生成策略中的一种方法。在这种方法中，<br/>模型会生成一组候选token，然后从累计概率达到或超过p的token中随机选择一个作为输出。<br/>例如，如果top_p设为0.9，那么模型会选择一组最可能的token，这些token的累计概率达到或超过0.9。 | 0.75   |
| max_tokens   | 否  | 生成文本最大长度                                                                                                                                                           | 256    |
| mode         | 否  | 选择模式，同步：invoke，异步：async，异步结果：async_result，流式：stream                                                                                                                | invoke |
| knowledge    | 否  | 选择知识库，通过知识库接口查看支持的知识库,默认不使用知识库                                                                                                                                     | None   |
| top_k        | 否  | 知识库参数，命中知识数量                                                                                                                                                       | 5      |
| threshold    | 否  | 知识库参数，阈值，数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准                                                                                                               | 500    |
| retry_action | 否  | 自定义重试操作行为，需继承Retry类，重写其中的方法                                                                                                                                        | None   |

</details>
<br/>
<details><summary style="font-size: large">响应参数说明</summary>

| 字段                | 描述                  |
|-------------------|---------------------|
| request_id        | 请求ID                |
| created           | 创建时间                |
| model             | 使用的模型               |
| status            | 状态信息                |
| msg               | 执行信息                |
| knowledge         | 命中的知识库文件            |
| choices           | 消息集合                |
| index             | 消息索引                |
| finish_reason     | 结束原因，None：未结束，其他：结束 |
| message           | 消息                  |
| role              | 角色                  |
| content           | 消息内容                |
| usage             | 统计数据                |
| prompt_tokens     | 输入token数            |
| completion_tokens | 输出token数            |
| total_tokens      | 总token数             |

</details>
<br/>
<details><summary style="font-size: large">状态码</summary>

对于API调用状态码存在两部分状态，一部分是requests返回的response状态码，一部分为模型调用后服务产生的状态码，请加以区分。

SDK调用统一集成在code字段。
#### response code

| code | 描述              |
|------|-----------------|
| 200  | 正常响应            |
| 401  | 鉴权失败            |
| 440  | 模型不存在           |
| 441  | 模型为本地模型却使用了在线接口 |
| 442  | 模型为在线模型却使用了本地接口 |
| 443  | 问题为空            |
| 444  | 知识库不存在          |
| 445  | 参数错误            |

#### server code

| code | 描述          |
|------|-------------|
| 200  | 正常          |
| 6601 | 敏感词         |
| 6602 | 异步结果未生成     |
| 400  | 访问异常        |
| 408  | 请求超时        |
| 其他   | 各服务端返回的错误状态 |

</details>