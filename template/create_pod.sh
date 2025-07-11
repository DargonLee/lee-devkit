#!/bin/bash

# CocoaPods 模板生成脚本
# 使用方法: ./create_pod.sh NewModuleName

# 检查参数
if [ $# -eq 0 ]; then
    echo "错误: 请提供新模块名称"
    echo "使用方法: ./create_pod.sh NewModuleName"
    exit 1
fi

NEW_MODULE_NAME=$1
TEMPLATE_NAME="NBTemplateModule"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/$TEMPLATE_NAME"

# 检查模板目录是否存在
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "错误: 模板目录 $TEMPLATE_DIR 不存在"
    exit 1
fi

# 检查新模块目录是否已存在
if [ -d "$NEW_MODULE_NAME" ]; then
    echo "错误: 目录 $NEW_MODULE_NAME 已存在"
    exit 1
fi

echo "正在创建新的 CocoaPods 库: $NEW_MODULE_NAME"

# 复制模板目录
cp -r "$TEMPLATE_DIR" "$NEW_MODULE_NAME"

# 进入新创建的目录
cd "$NEW_MODULE_NAME"

# 函数：重命名文件和目录
rename_files() {
    local current_dir=$1
    
    # 处理当前目录下的所有文件和目录
    find "$current_dir" -depth -name "*$TEMPLATE_NAME*" | while read -r item; do
        # 获取目录名和基础名
        dir_name=$(dirname "$item")
        base_name=$(basename "$item")
        
        # 替换名称
        new_name="${base_name//$TEMPLATE_NAME/$NEW_MODULE_NAME}"
        new_path="$dir_name/$new_name"
        
        # 重命名
        if [ "$item" != "$new_path" ]; then
            mv "$item" "$new_path"
            echo "重命名: $item -> $new_path"
        fi
    done
}

# 函数：替换文件内容
replace_content() {
    local current_dir=$1
    
    # 查找所有文本文件并替换内容
    find "$current_dir" -type f \( \
        -name "*.swift" -o \
        -name "*.h" -o \
        -name "*.m" -o \
        -name "*.mm" -o \
        -name "*.podspec" -o \
        -name "*.md" -o \
        -name "Podfile" -o \
        -name "*.plist" -o \
        -name "*.pbxproj" -o \
        -name "*.xcscheme" -o \
        -name "*.json" -o \
        -name "*.txt" -o \
        -name "*.yml" -o \
        -name "*.yaml" \
    \) -exec grep -l "$TEMPLATE_NAME" {} \; | while read -r file; do
        # 使用 sed 替换文件内容
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/$TEMPLATE_NAME/$NEW_MODULE_NAME/g" "$file"
        else
            # Linux
            sed -i "s/$TEMPLATE_NAME/$NEW_MODULE_NAME/g" "$file"
        fi
        echo "替换内容: $file"
    done
}

# 执行重命名和内容替换
echo "正在重命名文件和目录..."
rename_files "."

echo "正在替换文件内容..."
replace_content "."

# 特殊处理：更新 .xcodeproj 文件中的项目名称
if [ -d "Example" ]; then
    cd Example
    
    # 重命名 xcodeproj 文件
    if [ -d "${NEW_MODULE_NAME}_Example.xcodeproj" ]; then
        # 更新 project.pbxproj 文件中的项目引用
        if [ -f "${NEW_MODULE_NAME}_Example.xcodeproj/project.pbxproj" ]; then
            echo "更新 Xcode 项目配置..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/name = ${TEMPLATE_NAME}_Example/name = ${NEW_MODULE_NAME}_Example/g" "${NEW_MODULE_NAME}_Example.xcodeproj/project.pbxproj"
                sed -i '' "s/productName = ${TEMPLATE_NAME}_Example/productName = ${NEW_MODULE_NAME}_Example/g" "${NEW_MODULE_NAME}_Example.xcodeproj/project.pbxproj"
            else
                sed -i "s/name = ${TEMPLATE_NAME}_Example/name = ${NEW_MODULE_NAME}_Example/g" "${NEW_MODULE_NAME}_Example.xcodeproj/project.pbxproj"
                sed -i "s/productName = ${TEMPLATE_NAME}_Example/productName = ${NEW_MODULE_NAME}_Example/g" "${NEW_MODULE_NAME}_Example.xcodeproj/project.pbxproj"
            fi
        fi
    fi
    
    cd ..
fi

# 更新 podspec 文件的特殊字段
if [ -f "${NEW_MODULE_NAME}.podspec" ]; then
    echo "更新 podspec 文件..."
    
    # 如果有默认的描述，可以在这里更新
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/s.name *= *'${TEMPLATE_NAME}'/s.name = '${NEW_MODULE_NAME}'/g" "${NEW_MODULE_NAME}.podspec"
        sed -i '' "s/s.name *= *\"${TEMPLATE_NAME}\"/s.name = \"${NEW_MODULE_NAME}\"/g" "${NEW_MODULE_NAME}.podspec"
    else
        sed -i "s/s.name *= *'${TEMPLATE_NAME}'/s.name = '${NEW_MODULE_NAME}'/g" "${NEW_MODULE_NAME}.podspec"
        sed -i "s/s.name *= *\"${TEMPLATE_NAME}\"/s.name = \"${NEW_MODULE_NAME}\"/g" "${NEW_MODULE_NAME}.podspec"
    fi
fi

# 清理可能的临时文件
find . -name "*.orig" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null

echo ""
echo "✅ 成功创建新的 CocoaPods 库: $NEW_MODULE_NAME"
echo ""
echo "接下来你可以："
echo "1. 进入目录: cd $NEW_MODULE_NAME"
echo "2. 编辑 ${NEW_MODULE_NAME}.podspec 文件，更新描述、版本、作者等信息"
echo "3. 进入 Example 目录安装依赖: cd Example && pod install"
echo "4. 开始开发你的库！"
echo ""
echo "注意事项："
echo "- 请检查并更新 ${NEW_MODULE_NAME}.podspec 中的 URL、描述等信息"
echo "- 如果需要，请更新 LICENSE 文件"
echo "- 建议在 Git 中初始化项目: git init"
