---
title: "protobuf3"
date: 2025-11-15
draft: false
tags: ['grpc', 'protobuf']
---

# protobuf

## 一些杂碎



protobuf 主要用于编写一些



### 关键字

1. option
option 就是给 protobuf 定义（消息、字段、服务、方法等）添加"配置元数据"，用来控制代码生成行为或提供运行时信息。主要定义场景:

- 文件级别：影响整个 proto 文件的代码生成（如包名、优化策略）
- 消息/字段级别：标记废弃、自定义序列化行为
- 服务/方法级别：HTTP 映射、权限控制、限流等元信息
```yaml
.proto 中定义 option
    ↓
protoc 编译器解析 w
    ↓
┌─────────────────┬──────────────────┐
│ 编译时处理      │ 运行时处理        │
│ (硬编码到代码)  │ (存入描述符反射)  │
├─────────────────┼──────────────────┤
│ deprecated      │ HTTP 映射         │
│ → #[deprecated] │ → 网关路由        │
│                 │                  │
│ java_package    │ 自定义 option     │
│ → 包名          │ → 拦截器逻辑      │
└─────────────────┴──────────────────┘
```

如果使用 option 定义了一个不存在的,编译器在生成的时候会告警, 比如

```protobuf
// route_guide.proto
syntax = "proto3";

service RouteGuide {
  rpc GetFeature(Point) returns (Feature) {
    option (some_random_option) = true;  // 这个 option 根本不存在
  }
}
```

编译会产生如下告警:

```protobuf
$ cargo build

warning: Option "(some_random_option)" unknown. Ensure that your proto
         definition file imports the proto which defines the option.
# ⚠️ 只是警告，不是错误！
# ✅ 代码会正常生成
```



1. stream 关键字,生成带有 tokio 的Stream 的方法,返回一个 future
比如这个:

```protobuf
rpc BidirectionalStreamingEcho(stream EchoRequest) returns (stream EchoResponse) {}
```

 生成的 rust 代码如下:

```rust
pub async fn bidirectional_streaming_echo(
            &mut self,
            request: impl tonic::IntoStreamingRequest<Message = super::EchoRequest>,
        ) -> std::result::Result<
            tonic::Response<tonic::codec::Streaming<super::EchoResponse>>,
            tonic::Status,
        > 
```



