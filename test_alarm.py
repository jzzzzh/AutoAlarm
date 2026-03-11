"""Test script for auto-alarm package."""

from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

from auto_alarm import init_from_config, notify_on_failure, Config


def main():
    # 从环境变量加载配置
    config = Config.from_env()
    init_from_config(config)

    # 测试失败通知
    @notify_on_failure('1499765600@qq.com')  # 改成你的收件人邮箱
    def test_failure():
        raise ValueError("测试错误：这是一个故意的失败")

    # 测试成功通知（可选）
    @notify_on_failure(
        to_emails='1499765600@qq.com',
        notify_on_success=True,
        success_message="任务执行成功！"
    )
    def test_success():
        return "任务完成"

    # 运行失败测试
    print("=" * 50)
    print("测试 1: 失败通知")
    print("=" * 50)
    try:
        test_failure()
    except ValueError as e:
        print(f"预期错误: {e}")

    # 运行成功测试
    print("\n" + "=" * 50)
    print("测试 2: 成功通知")
    print("=" * 50)
    result = test_success()
    print(f"返回结果: {result}")


if __name__ == '__main__':
    main()
