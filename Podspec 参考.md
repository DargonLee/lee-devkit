### 团队 CocoaPods 组件开发规范：podspec 模板与标准化指南

> 本文档目的为团队提供的 CocoaPod 库 `xx.podspec` 规范模板及详细配置说明，帮助团队统一创建和维护 Pod 库



#### 标准 `YourLibraryName.podspec` 模板

- 库名字具有语义化
- source 使用`https://git.ninebot.com/iOS`路径下的 `git 仓库`. <font color='red'>不能使用外部仓库</font>

```
Pod::Spec.new do |s|
  # ========== 基础信息 ========== 
  s.name         = "YourLibraryName"  # 库名称（使用大驼峰命名）
  s.version      = "0.1.0"            # 遵循语义化版本规范
  s.summary      = "One-line summary under 140 characters."  # 简洁摘要
  s.description  = <<-DESC
  详细描述（比摘要长 3-5 倍），说明库的功能、解决的问题和核心特性。
  例如：这是一个高效处理网络请求的轻量级库，支持自动缓存和请求重试机制。
  DESC
  
  # ========== 仓库信息 ========== 
  s.homepage     = "https://git.ninebot.com/iOS"  # 项目主页
  s.license      = { :type => "MIT", :file => "LICENSE" }    # 许可证类型
  s.author       = { "TeamName" => "team@company.com" }      # 团队统一邮箱
  s.source       = { 
    :git => "https://github.com/Company/YourLibrary.git", 
    :tag => s.version.to_s   # 必须使用版本号标签
  }
  
  # ========== 平台要求 ========== 
  s.ios.deployment_target = "13.0"  # 最低支持 iOS 版本
  s.swift_versions = ["5.0", "5.1"] # Swift 版本兼容性
  
  # ========== 源码配置 ========== 
  # 主源码目录（默认结构）
  s.source_files = "Sources/**/*.{swift,h,m}"
  
  # ========== 资源文件 ========== 
  # 方式1：独立资源包（推荐，避免冲突）
  s.resource_bundles = {
    'YourLibraryResources' => ['Resources/**/*.{png,xcassets,strings}']
  }
  
  # 方式2：直接包含资源（简单场景）
  # s.resources = "Resources/**/*"
  
  # ========== 依赖配置 ========== 
  # 系统框架依赖
  s.frameworks = "UIKit", "Foundation"
  
  # 第三方库依赖（指定版本范围）
  s.dependency "Alamofire", "~> 5.6"
  s.dependency "SnapKit", ">= 5.0.0"
  
  # ========== 模块化支持 ========== 
  # 子模块配置（可选）
  s.subspec "Networking" do |ss|
    ss.source_files = "Sources/Networking/**/*.swift"
    ss.dependency "Alamofire"
  end
  
  s.subspec "UI" do |ss|
    ss.source_files = "Sources/UI/**/*.swift"
    ss.resources = "Resources/UI/**/*.xcassets"
  end
end
```



#### 目录结构规范

```
YourLibrary/
├── README.md           # 库使用文档
├── YourLibrary.podspec # 配置文件
├── Sources/            # 主源码目录
│   ├── Core/
│   ├── Networking/
│   └── UI/
├── Resources/          # 资源文件
│   ├── Images.xcassets
│   └── Localizations/
└── Example/            # 示例工程（按需）
    ├── Podfile
    └── YourLibrary.xcworkspace
```



#### 脚本使用

```
# 给脚本执行权限
chmod +x create_pod.sh

# 使用脚本创建新的库
./create_pod.sh NetworkManager
```

