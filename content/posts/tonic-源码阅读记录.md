---
title: "tonic 源码阅读记录"
date: 2025-12-18
draft: false
tags: ['rust', 'grpc', 'tonic']
---

1. Status 的状态表示
```rust
#[derive(Clone)]
pub struct Status(Box<StatusInner>);

/// Box the contents of Status to avoid large error variants
#[derive(Clone)]
struct StatusInner {
    /// The gRPC status code, found in the `grpc-status` header.
    code: Code,
    /// A relevant error message, found in the `grpc-message` header.
    message: String,
    /// Binary opaque details, found in the `grpc-status-details-bin` header.
    details: Bytes,
    /// Custom metadata, found in the user-defined headers.
    /// If the metadata contains any headers with names reserved either by the gRPC spec
    /// or by `Status` fields above, they will be ignored.
    metadata: MetadataMap,
    /// Optional underlying error.
    source: Option<Arc<dyn Error + Send + Sync + 'static>>,
}

```

这里用一个 Box 包住是为了节省内存,主要原因是如果返回 成功,后面的各种错误信息,就会迫使成功的时候的占用大小也会需要跟这个带有错误的状态一样大





