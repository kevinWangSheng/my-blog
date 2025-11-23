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



### streaming 

这里实现一个例子,理解对应的 streaming 的作用和效果

这里的 stream 可以理解为一个迭代器,iterator, 只不是是异步 async 的, 异步相对于同步来说,异步是 每一次 next 的时候会挂起 yield

例子: streaming server: 客户端发起请求，服务端持续每秒推送一次当前的 CPU 占用率（模拟） 
• 学习点：如何生成异步流，mpsc 通道的使用。

Bidirectional Streaming (RemoteShell): 客户端发送指令流，服务端执行并实时返回输出流
• 学习点：如何同时处理输入流和输出流，所有权的转移。

这里使用了 async-stream 的 try_stream! 宏模仿数据一段段返回. 主要模仿数据没返回的收到的时候,这个任务会挂起,让 cpu 去执行其他任务,数据准备好了操作系统会通知 tokio,然后在由 tokio 唤醒这个任务继续执行



1. 首先编写 proto 文件内容,注意对应的返回需要 stream 表示支持 streaming
```protobuf
syntax = "proto3";

package monitor;

message CpuRequest{
    string host_id = 1;
}

message CpuResponse{
    float usage = 1;
    int64 timestamp = 2;
}


message CommandRequest{
    string command = 1;
}

message CommandResponse{
    string output = 1;
}

service MonitorService {
    rpc WatchCpu(CpuRequest) returns ( stream CpuResponse);
    
    rpc ExecuteCommand(CommandRequest) returns (stream CommandResponse);
}

```



1. server.rs 模拟一个简单的 cpu 使用率进行断断续续返回
```rust
use std::{pin::Pin, time::Duration};

use async_stream::try_stream;
use tokio::io::AsyncBufReadExt;
use tokio_stream::Stream;
use tonic::{Request, Response, Status, transport::Server};

use crate::monitor::{
    CommandRequest, CommandResponse, CpuRequest, CpuResponse,
    monitor_service_server::{MonitorService, MonitorServiceServer},
};

mod monitor {
    // include!("generate/monitor.rs");
    tonic::include_proto!("monitor");
}

#[derive(Debug, Default)]
pub struct MyMonitor;

#[tonic::async_trait]
impl MonitorService for MyMonitor {
    type WatchCpuStream = Pin<Box<dyn Stream<Item = Result<CpuResponse, Status>> + Send>>;
    type ExecuteCommandStream = Pin<Box<dyn Stream<Item = Result<CommandResponse, Status>> + Send>>;

    async fn watch_cpu(
        &self,
        request: Request<CpuRequest>,
    ) -> Result<Response<Self::WatchCpuStream>, Status> {
        let host_ip = request.into_inner();

        println!("start to monitor the host :{:?}", host_ip);

        // try stream and send the stream message to the client
        let output_stream = try_stream! {
            let mut i = 0;
            loop {
                if i >= 10 {
                    break;
                }
                tokio::time::sleep(Duration::from_secs(1)).await;
                let usage_precent = 10.0 +(i as f32);
                let timestamp = 1234567+i;

                let response = CpuResponse {
                    usage:usage_precent,
                    timestamp
                };
                // send the message back to the client
                yield response;
                i += 1;
            }
        };
        Ok(Response::new(
            Box::pin(output_stream) as Self::WatchCpuStream
        ))
    }

    async fn execute_command(
        &self,
        request: Request<CommandRequest>,
    ) -> Result<Response<Self::ExecuteCommandStream>, Status> {
        let cmd = request.into_inner().command;

        // execute the command with sh enviroment, and return the output
        let output_stream = try_stream! {
            use tokio::process::Command;
            use std::process::Stdio;
            use tokio::io::BufReader;
            // start a sub processor the execute the command
            let mut child = Command::new("sh").arg("-c").arg(&cmd).stdout(Stdio::piped()).spawn().map_err(|e| Status::internal(format!("启动失败:{}",e)))?;

            // execute the child process
            let stdout = child.stdout.take().unwrap();
            let mut reader = BufReader::new(stdout).lines();

            while let Ok(Some(line)) = reader.next_line().await{
                yield CommandResponse{
                    output: line
                }
            }
        };

        Ok(Response::new(
            Box::pin(output_stream) as Self::ExecuteCommandStream
        ))
    }
}

#[tokio::main]
pub async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50052".parse()?;

    let monitor_service = MyMonitor::default();
    
    // let server = MonitorServiceServer::new(monitor_service);

    println!("the monitor server listing on addr :{}", addr);

    Server::builder()
        .add_service(MonitorServiceServer::new(monitor_service))
        .serve(addr)
        .await?;

    Ok(())
}

```

1. client.rs  简单的绑定,然后使用流的方式进行输出,观察返回
```rust
use tonic::Request;

use crate::monitor::{CpuRequest, monitor_service_client::MonitorServiceClient};


mod monitor{
    tonic::include_proto!("monitor");
}

#[tokio::main]
pub async fn main() -> Result<(), Box<dyn std::error::Error>>{
    let mut client = MonitorServiceClient::connect("http://127.0.0.1:50052").await?;
    println!("the client was connected");
    let mut response_stream = client.watch_cpu(Request::new(CpuRequest{host_id:"server-1".into()})).await?.into_inner();
    
    while let Some(msg) = response_stream.message().await?{
        println!("receive the cpu usage of :{:?}",msg);
    }
    Ok(())
}
```



### 进阶streaming



主要实现一个交互式的 shell, 及 client 发送命令,server 进行回应, 主要是实现一个双向流



